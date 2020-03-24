import functools
import timeit
import inspect


def debug(function):
    print(f"Setting up {function.__name__} as a debuggable function")

    @functools.wraps(function)
    def predicate(*args, **kwargs):
        print(f"Starting a run of {function.__name__} "
              f"with the arguments ({', '.join(args)})"
              f"and the keyword arguments ({','.join(arg + '=' + value for arg, value in kwargs.items())})")
        start = timeit.default_timer()
        result = function(*args, **kwargs)
        elapsed = timeit.default_timer() - start
        print(f"{function.__name__} returned ({result}) in {elapsed}")
        return result

    @functools.wraps(function)
    async def async_predicate(*args, **kwargs):
        print(f"Starting a run of {function.__name__} "
              f"with the arguments ({', '.join(args)})"
              f"and the keyword arguments ({','.join(arg + '=' + value for arg, value in kwargs.items())})")
        start = timeit.default_timer()
        result = await function(*args, **kwargs)
        elapsed = timeit.default_timer() - start
        print(f"{function.__name__} returned ({result}) in {elapsed}")
        return result

    return async_predicate if inspect.iscoroutinefunction(function) else predicate
