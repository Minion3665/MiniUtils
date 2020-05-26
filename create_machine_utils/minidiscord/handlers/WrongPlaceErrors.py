from discord.ext import commands
import discord


# Handles commands.PrivateMessageOnly
async def handle_private_message_only(ctx, _error, _next):
    return await ctx.send_exception(
        f"This command only works in private messages!",
        title=f"Wrong place",
    )


# Handles commands.NoPrivateMessage
async def handle_no_private_message(ctx, _error, _next):
    return await ctx.send_exception(
        f"This command doesn't work in private messages!",
        title=f"Wrong place",
    )


# Handles commands.NSFWChannelRequired
async def handle_nsfw_channel_required(ctx, _error, _next):
    return await ctx.send_exception(
        f"This command doesn't work in non-nsfw channels!",
        title=f"Wrong place",
    )


def setup(handler):
    handler.handles(
        commands.PrivateMessageOnly
    )(handle_private_message_only)
    handler.handles(
        commands.NoPrivateMessage
    )(handle_no_private_message)
    handler.handles(
        commands.NSFWChannelRequired
    )(handle_nsfw_channel_required)
