import typing
import traceback
from discord.ext import commands
import inspect
from . import handlers


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        print("Loading MiniUtils Error Handler")
        self.bot = bot
        self._handlers = ()
        handlers.setup(self)

    def handles(self, exception):
        def decorator(func):
            if isinstance(exception, tuple) or issubclass(exception, Exception):
                self._handlers = ((exception, func),) + self._handlers
            else:
                raise TypeError(f"{str(exception)} isn't an exception or a tuple of exceptions")

            print(f"{exception} is now handled by {func.__name__}")

            return func

        if (isinstance(exception, typing.Callable) or inspect.iscoroutinefunction(exception)) \
                and not issubclass(exception, Exception):
            raise TypeError(f"Your exception is a function, did you forget to pass parameters to this decorator?")

        return decorator

    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        try:
            for handles, handler in self._handlers:
                if not isinstance(error, handles):
                    continue
                continue_handling = False

                def _next(_error=error):
                    nonlocal error
                    nonlocal continue_handling
                    error = _error
                    continue_handling = True

                if inspect.iscoroutinefunction(handler):
                    await handler(context, error, _next)
                else:
                    handler(context, error, _next)

                if not continue_handling:
                    break
            else:
                print(f"Unhandled error {error}")
                print("- [x] " + "".join(traceback.format_exception(
                    etype=type(error), value=error, tb=error.__traceback__
                )).replace("\n", "\n- [x] "))

        except Exception as e:
            print(f"Got an error in the error handler: {e}")
            print("- [x] " + "".join(traceback.format_exc()).replace("\n", "\n- [x] "))
