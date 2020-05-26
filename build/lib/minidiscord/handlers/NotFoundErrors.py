from discord.ext import commands


# Handles commands.CommandNotFound
async def handle_command_not_found(_ctx, _error, _next):
    pass


def setup(handler):
    handler.handles(
        commands.CommandNotFound
    )(handle_command_not_found)
