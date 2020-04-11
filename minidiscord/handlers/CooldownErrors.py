from discord.ext import commands
import discord


# Handles commands.CommandOnCooldown
async def handle_command_on_cooldown(ctx, _error, _next):
    return await ctx.send_exception(
        f"Oh no! it looks like this command is on a cooldown! try again in `{_error.retry_after}` seconds!",
        title=f"Too fast!",
    )


# Handles commands.MaxConcurrencyReached
async def handle_max_concurrency_reached(ctx, _error, _next):
    buckets = {
        discord.ext.commands.BucketType.default: "This command is already running {number} time{s}",
        discord.ext.commands.BucketType.user: "You're already running this command {number} time{s}",
        discord.ext.commands.BucketType.guild: "This command is already running {number} time{s} in this server",
        discord.ext.commands.BucketType.channel: "This command is already running {number} time{s} in this channel",
        discord.ext.commands.BucketType.member: "You're already running this command {number} time{s} in this guild",
        discord.ext.commands.BucketType.category: "This command is already running {number} time{s} in this category",
        discord.ext.commands.BucketType.role: "This command is already running {number} time{s} by people with the "
                                              "same role as you",
    }
    return await ctx.send_exception(
        buckets.get(_error.per, "This command is already running {number} time{s}").format(
            number=_error.number,
            s="" if _error.number == 1 else "s"
        ),
        title=f"Not again...",
    )


def setup(handler):
    handler.handles(
        commands.CommandOnCooldown
    )(handle_command_on_cooldown)
    handler.handles(
        commands.MaxConcurrencyReached
    )(handle_max_concurrency_reached)
