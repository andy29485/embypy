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


def _run_func(func, *args, **kwargs):
    if is_asyncio_context():
        return func(*args, **kwargs)
    elif inspect.iscoroutinefunction(func):
        with _loop_lock:
            loop = None
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
            return loop.run_until_complete(
                func(*args, **kwargs)
            )
    elif callable(func):
        return func(*args, **kwargs)
