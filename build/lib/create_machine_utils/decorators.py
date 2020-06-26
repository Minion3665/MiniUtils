import functools
import inspect
import timeit
import traceback


def debug(function):
    print(f"Setting up {function.__name__} as a debuggable function")

    @functools.wraps(function)
    def predicate(*args, **kwargs):
        print(
            f"Starting a run of {function.__name__} " +
            (
                f"with the arguments ({', '.join(str(arg) for arg in args)}) "
                if args else
                f"with no arguments "
            ) +
            (
                f"and the keyword arguments ({','.join(str(arg) + '=' + str(value) for arg, value in kwargs.items())})"
                if kwargs else
                f"and no keyword arguments"
            )
        )
        start = timeit.default_timer()
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            elapsed = timeit.default_timer() - start
            print(f"{function.__name__} failed with ({e}) in {elapsed}")
            print("- [x] " + "".join(traceback.format_exc()).replace("\n", "\n- [x] "))
            raise e
        elapsed = timeit.default_timer() - start
        print(f"{function.__name__} returned ({result}) in {elapsed}")
        return result

    @functools.wraps(function)
    async def async_predicate(*args, **kwargs):
        print(
            f"Starting a run of async {function.__name__} " +
            (
                f"with the arguments ({', '.join(str(arg) for arg in args)}) "
                if args else
                f"with no arguments "
            ) +
            (
                f"and the keyword arguments ({','.join(str(arg) + '=' + str(value) for arg, value in kwargs.items())})"
                if kwargs else
                f"and no keyword arguments"
            )
        )
        start = timeit.default_timer()
        try:
            result = await function(*args, **kwargs)
        except Exception as e:
            elapsed = timeit.default_timer() - start
            print(f"Async {function.__name__} failed with ({e}) in {elapsed}")
            print("- [x] " + "".join(traceback.format_exc()).replace("\n", "\n- [x] "))
            raise e
        elapsed = timeit.default_timer() - start
        print(f"Async {function.__name__} returned ({result}) in {elapsed}")
        return result

    return async_predicate if inspect.iscoroutinefunction(function) else predicate
