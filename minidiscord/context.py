import discord
from discord.ext import commands
import functools


class MiniContext(commands.Context):
    def __init__(self, context):
        commands.Context.__init__(self, **context.__dict__)
        self.mention = self.channel.mention if isinstance(self.channel, discord.TextChannel) else "No channel"

    async def send(self,
                   description=discord.Embed.Empty, *,
                   title=discord.Embed.Empty,
                   color=discord.Embed.Empty,
                   tts=False,
                   file=None,
                   files=None,
                   delete_after=None,
                   nonce=None):
        my_perms = self.channel.permissions_for(self.channel.guild.me) \
            if isinstance(self.channel, discord.TextChannel) else None
        if not isinstance(self.channel, discord.TextChannel) or my_perms.embed_links:
            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
            )
            return await self.channel.send(
                embed=embed,
                tts=tts,
                file=file,
                files=files,
                delete_after=delete_after,
                nonce=nonce,
            )
        else:
            return await self.channel.send(
                (f"> **{title}**" if title is not None else "") +
                (f"\n{description}" if description is not None else ""),
                tts=tts,
                file=file,
                files=files,
                delete_after=delete_after,
                nonce=nonce,
            )

    def input(self,
              title=discord.Embed.Empty,
              prompt=discord.Embed.Empty,
              required_type=str,
              timeout=60,
              check=lambda message: True,
              error="That isn't a valid message"):

        async def message_check(message):
            try:
                if self.author == message.author and self.channel == message.channel:
                    required_type(message.content)
                    if check(message):
                        return True
                    else:
                        await self.send(
                            error,
                            title="Oops"
                        )
                        return False
            except ValueError:
                await self.send(
                    error,
                    title="Oops"
                )

        self.bot.create_task(
            self.send(
                prompt,
                title=title,
            )
        )
        self.bot.wait_for(
            "message",
            check=message_check,
            timeout=timeout
        )


def minictx(*args, **kwargs):
    def deco(function):
        @functools.wraps(function)
        async def predicate(cog, ctx, *function_args, **function_kwargs):
            ctx = MiniContext(ctx)
            return await function(cog, ctx, *function_args, **function_kwargs)

        return predicate

    return deco
