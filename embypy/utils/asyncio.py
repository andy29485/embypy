import asyncio
import inspect
import threading


_loop_lock = threading.RLock()


def is_asyncio_context() -> bool:
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False
    except AttributeError:
        try:
            return asyncio._get_running_loop() is not None
        except AttributeError:
            return False


def async_func(func):
    def tmp_func(*args, **kargs):
        return _run_func(func, *args, **kargs)
    return tmp_func


def _get_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        return asyncio.new_event_loop()


def iter_over_async(ait, loop):
    ait = ait.__aiter__()
    async def get_next():
        try:
            obj = await ait.__anext__()
            return False, obj
        except StopAsyncIteration:
            return True, None
    while True:
        done, obj = loop.run_until_complete(get_next())
        if done:
            break
        yield obj


def _run_func(func, *args, **kwargs):
    out = None
    if callable(func):
        out = func(*args, **kwargs)
    if is_asyncio_context():
        return out
    elif inspect.isasyncgen(out):
        with _loop_lock:
            return iter_over_async(out, _get_loop())
    elif inspect.iscoroutinefunction(func):
        with _loop_lock:
            return _get_loop().run_until_complete(out)
    return out
