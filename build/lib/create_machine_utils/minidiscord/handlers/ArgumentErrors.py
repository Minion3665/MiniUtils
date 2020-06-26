from discord.ext import commands
import re


# Handles commands.TooManyArguments
async def handle_too_many_arguments(ctx, _error, _next):
    num = len(ctx.command.clean_params)
    await ctx.send_exception(
        f"That's too many arguments: this command only takes {num} arguments! if you "
        f"wanted a sub-command, check the name and try again",
        title=f"Invalid argument",
    )


# Handles (commands.BadUnionArgument, commands.BadArgument, commands.MissingRequiredArgument)
async def handle_bad_argument(ctx, _error, _next):
    error = re.sub(r'\.$', '', str(_error))
    await ctx.send_exception(
        f"Missing or incorrect argument\n(`{error}`)",
        title=f"Invalid argument",
    )


# Handles commands.ArgumentParsingError
async def handle_badly_quoted_argument(ctx, _error, _next):
    await ctx.send_exception(
        f"Try surrounding each argument in speech marks (`\"`) and placing backslashes (`\\`) before any "
        f"speech marks other than surrounding speech marks in your arguments",
        title=f"Invalid argument",
    )


def setup(handler):
    handler.handles(
        commands.TooManyArguments
    )(handle_too_many_arguments)
    handler.handles(
        (commands.BadUnionArgument, commands.BadArgument, commands.MissingRequiredArgument)
    )(handle_bad_argument)
    handler.handles(
        commands.ArgumentParsingError
    )(handle_badly_quoted_argument)
