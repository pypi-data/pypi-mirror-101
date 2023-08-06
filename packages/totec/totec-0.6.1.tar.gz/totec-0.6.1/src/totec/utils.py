def select_keys(m, *keys):
    return {k: m[k] for k in keys if k in m}
