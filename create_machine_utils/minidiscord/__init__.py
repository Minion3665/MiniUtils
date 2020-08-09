from . import context as _context
from . import errors as _errors
from . import input
from . import menus
import discord

try:
    discord.AllowedMentions()
except AttributeError:
    raise ImportError("MiniDiscord requires discord.py v1.4.0 or greater (we need AllowedMentions). "
                      "Please install that before using minidiscord. "
                      "(At current time this can only be installed from git+https://github.com/Rapptz/discord.py)")

Context = _context.MiniContext
Bot = _context.MiniContextBot
AutoShardedBot = _context.AutoShardedMiniContextBot
Input = input
Menus = menus

__all__ = (
    Context,
    Bot,
    AutoShardedBot,
    Input,
    Menus,
)
