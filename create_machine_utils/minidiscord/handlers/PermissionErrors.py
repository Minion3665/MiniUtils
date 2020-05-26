from discord.ext import commands
import discord


# Handles commands.NotOwner
async def handle_not_owner(ctx, _error, _next):
    if ctx.bot.owner_ids:
        owner_names = " or ".join(str(ctx.bot.get_user(user) or "Unknown User") for user in ctx.bot.owner_ids)
    else:
        owner_names = str(ctx.bot.get_user(ctx.bot.owner_id) or "Unknown User")
    return await ctx.send_exception(
        f"You must be {owner_names} to run this command!",
        title=f"No permissions",
    )


# Handles commands.BotMissingPermissions
async def handle_bot_missing_permissions(ctx, _error, _next):
    perms = [m.replace('_', ' ') for m in _error.missing_perms]
    missing_perms = '\n• '.join(perms)
    return await ctx.send_exception(
        f"I'm missing the following permissions:\n```\n• {missing_perms}\n```",
        title=f"I need more permissions",
    )


# Handles commands.BotMissingRole
async def handle_bot_missing_role(ctx, _error, _next):
    return await ctx.send_exception(
        f"I'm missing the {_error.missing_role.name} role",
        title=f"I need more roles",
    )


# Handles commands.BotMissingAnyRole
async def handle_bot_missing_any_role(ctx, _error, _next):
    return await ctx.send_exception(
        f"I need {' or '.join(role.name for role in _error.missing_roles)} to run this command",
        title=f"I need more roles",
        paginate_by="or",
    )


# Handles commands.MissingPermissions
async def handle_missing_permissions(ctx, _error, _next):
    perms = [m.replace('_', ' ') for m in _error.missing_perms]
    missing_perms = '\n• '.join(perms)
    return await ctx.send_exception(
        f"You're missing the following permissions:\n```\n• {missing_perms}\n```",
        title=f"No permissions",
    )


# Handles commands.MissingRole
async def handle_missing_role(ctx, _error, _next):
    return await ctx.send_exception(
        f"You're missing the {_error.missing_role.name} role",
        title=f"You need more roles",
        paginate_by="or",
    )


# Handles commands.MissingAnyRole
async def handle_missing_any_role(ctx, _error, _next):
    return await ctx.send_exception(
        f"You need {' or '.join(role.name for role in _error.missing_roles)} to run this command",
        title=f"You need more roles",
    )


# Handles commands.CommandInvokeError but only if it's a discord.HTTPException
async def handle_http_exceptions(ctx, _error, _next):
    if not isinstance(_error.original, discord.HTTPException):
        return _next()
    return await ctx.send_exception(
        f"Maybe I don't have enough permissions, or maybe discord just screwed up. Either way here's the full error: "
        f"{_error.original}",
        title=f"I couldn't run this command",
    )


# Handles commands.CheckFailure
async def handle_failing_checks(ctx, _error, _next):
    return await ctx.send_exception(
        f"It's possible that you don't have enough permissions to run this command, or maybe it just can't be run now. "
        f"Either way, the full error is {_error}",
        title=f"You were not in the right place at the right time",
    )


# Handles commands.DisabledCommand
async def handle_disabled_commands(ctx, _error, _next):
    return await ctx.send_exception(
        f"This command is disabled (and therefore doesn't exist). Perhaps it's still in development?",
        title=f"Command? What command? *You saw nothing*",
    )


def setup(handler):
    handler.handles(
        commands.NotOwner
    )(handle_not_owner)
    handler.handles(
        commands.BotMissingPermissions
    )(handle_bot_missing_permissions)
    handler.handles(
        commands.MissingPermissions
    )(handle_missing_permissions)
    handler.handles(
        commands.CommandInvokeError
    )(handle_http_exceptions)
    handler.handles(
        commands.CheckFailure
    )(handle_failing_checks)
    handler.handles(
        commands.DisabledCommand
    )(handle_disabled_commands)
    handler.handles(
        commands.MissingRole
    )(handle_missing_role)
    handler.handles(
        commands.BotMissingRole
    )(handle_bot_missing_role)
    handler.handles(
        commands.MissingAnyRole
    )(handle_missing_any_role)
    handler.handles(
        commands.BotMissingAnyRole
    )(handle_bot_missing_any_role)
