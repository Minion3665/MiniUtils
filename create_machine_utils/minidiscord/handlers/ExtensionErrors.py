from discord.ext import commands


# Handles commands.ExtensionAlreadyLoaded
async def handle_extension_already_loaded(ctx, _error, _next):
    await ctx.send_exception(
        f"The {_error.name} extension is already loaded",
        title="That's already here",
    )


# Handles commands.ExtensionAlreadyLoaded
async def handle_extension_not_loaded(ctx, _error, _next):
    await ctx.send_exception(
        f"The {_error.name} extension is not loaded",
        title="What? Where??",
    )


# Handles commands.ExtensionNotFound
async def handle_extension_not_found(ctx, _error, _next):
    await ctx.send_exception(
        f"The {_error.name} extension was not found",
        title="What? Where??",
    )


# Handles commands.NoEntryPointError
async def handle_no_entry_point(ctx, _error, _next):
    await ctx.send_exception(
        f"The {_error.name} extension doesn't seem to have a setup function",
        title="What? Where??",
    )


# Handles commands.ExtensionFailed
async def handle_failed_entry_point(ctx, _error, _next):
    await ctx.send_exception(
        f"The {_error.name} extension's setup function broke. Here's the full error: {_error.original}",
        title="Bonk!",
    )


def setup(handler):
    handler.handles(
        commands.ExtensionAlreadyLoaded
    )(handle_extension_already_loaded)
    handler.handles(
        commands.ExtensionNotLoaded
    )(handle_extension_not_loaded)
    handler.handles(
        commands.ExtensionNotFound
    )(handle_extension_not_found)
    handler.handles(
        commands.NoEntryPointError
    )(handle_no_entry_point)
    handler.handles(
        commands.ExtensionFailed
    )(handle_failed_entry_point)
