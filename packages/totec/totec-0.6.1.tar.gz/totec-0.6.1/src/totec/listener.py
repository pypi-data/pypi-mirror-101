import json
import logging
import os
from functools import wraps
from traceback import extract_tb

import requests
from requests.exceptions import HTTPError
from retry import retry

from totec.utils import select_keys
from totec import JobStatus

log = logging.getLogger(__name__)


class DataError(Exception):
    def __init__(self, message=None, cause=None):
        super().__init__(message or str(cause))
        self._cause = cause

    def to_dict(self):
        if hasattr(self._cause, "to_dict"):
            return self._cause.to_dict()
        return {"message": str(self)}


class JobListener:
    def __init__(self, backend, queue_names, outputs_encoder=None, retry_config=None):
        self._backend = backend
        self._queue_names = queue_names
        self._outputs_encoder = outputs_encoder or json.JSONEncoder
        self._retry_config = select_keys(
            retry_config or {"tries": 5, "delay": 1}, "tries", "delay"
        )

    def handle(self, dispatch):
        log.info("Listening on queues %s", self._queue_names)
        for (handle, queue_name, job) in self._backend.listen(self._queue_names):

            tag = job["tag"]
            job_type = job["type"]
            inputs = job["inputs"]

            fn = dispatch.get(job_type)
            if fn is None:
                log.warning("Unable to process job %s of type %s", tag, job_type)
                continue

            log.info("Dispatching job %s from queue %s", tag, queue_name)
            try:
                outputs = fn(inputs)
                if self._try_update_resource(job, JobStatus.SUCCES, outputs):
                    self._backend.sign_off(handle)
                    log.info("Signing off job %s", tag)
            except DataError as exc:
                log.error("Incorrect input for job %s: %s (%s)", job_type, inputs, exc)
                summary = _summarize_exception(exc)
                log.error(summary)
                self._try_update_resource(job, JobStatus.FAILED, summary)
                self._backend.sign_off(handle)
                log.info("Signing off job %s", tag)
            except Exception as exc:  # pylint: disable=broad-except
                log.error("Failed to compute job %s: %s (%s)", job_type, inputs, exc)
                summary = _summarize_exception(exc)
                log.error(summary)

    def _try_update_resource(self, job, status, data):
        body = json.dumps(
            {"status": status.name, "data": data}, cls=self._outputs_encoder
        )
        headers = {"Content-Type": "application/json"}

        @retry(HTTPError, logger=log, **self._retry_config)
        def patch(url):
            response = requests.patch(
                url, data=body, headers=headers, allow_redirects=False
            )
            if response.status_code == 404:
                response.raise_for_status()
            if response.status_code // 100 not in [2, 4]:
                response.raise_for_status()

        url = job.get("meta", {}).get("self")

        if url is None:
            log.warning("No URL for job resource")
            return False
        try:
            log.info("Updating resource %s", url)
            patch(url)
            return True
        except HTTPError as exc:
            log.warning("Failed to update resource %s: %s", url, exc)
            return exc.response.status_code in [404]
        except Exception as exc:  # pylint: disable=broad-except
            log.warning("Failed to update resource %s: %s", url, exc)
            return False


def map_exceptions(_mapping=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except (ValueError, ZeroDivisionError) as exc:
                raise DataError(cause=exc) from exc

        return wrapped

    return decorator


def _summarize_exception(exc):
    summary = {"message": str(exc), "type": str(type(exc))}
    if hasattr(exc, "__traceback__"):
        tb = []
        for frame_summary in extract_tb(exc.__traceback__):
            tb.append(
                {
                    "lineno": frame_summary.lineno,
                    "line": frame_summary.line,
                    "filename": os.path.basename(frame_summary.filename),
                }
            )
        summary["traceback"] = tb
    return summary
