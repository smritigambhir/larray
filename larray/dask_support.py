import dask.array as da
import numpy as np

def generic_func_factory(np_func, da_func):
    def generic_func(*args, **kwargs):
        assert isinstance(args, tuple) and args
        if isinstance(args[0], da.Array):
            return da_func(*args, **kwargs)
        else:
            # args[0] will often be np.ndarray but not always (array-like)
            return np_func(*args, **kwargs)
    return generic_func

for func_name in dir(np):
    if func_name.startswith('__'):
        continue
    np_func = getattr(np, func_name, None)
    da_func = getattr(da, func_name, None)
    if hasattr(np, func_name) and hasattr(da, func_name):
        func = generic_func_factory(np_func, da_func)
    elif hasattr(np, func_name):
        func = np_func
    elif hasattr(da, func_name):
        # should not happen
        func = da_func
    else:
        print(func_name, np_func, da_func)
        raise ValueError("cannot happen")
    globals()[func_name] = func

