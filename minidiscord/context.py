import discord
from discord.ext import commands
import copy
import typing
import asyncio
from .. import decorators


class MiniContext(commands.Context):
    def __init__(self, **kwargs):
        commands.Context.__init__(self, **kwargs)
        self.mention = self.channel.mention if isinstance(self.channel, discord.TextChannel) else "No channel"
        self._cleaner = commands.clean_content()

    def permissions_for(self, *args, **kwargs):
        return self.channel.permissions_for(*args, *kwargs)

    async def send(self,
                   content=discord.Embed.Empty, *,
                   title=discord.Embed.Empty,
                   color=discord.Embed.Empty,
                   tts=False,
                   file=None,
                   files=None,
                   delete_after=None,
                   nonce=None,
                   embed=None,
                   paginate_by: typing.Optional[str] = None):
        """
        :param content: The description of the embed
        :param title: The title of the embed
        :param color: The color of the embed
        :param tts: Should we send with TTS?
        :param file: What file should we send?
        :param files: What files should we send?
        :param delete_after: How long should we delete the message after?
        :param nonce: The value used by the discord guild and the client to verify that the message is successfully sent
        This is typically non-important.
        :param embed: A fully-formed embed to send.
        IF THIS IS SET IT IS ASSUMED YOU HAVE ALREADY DONE PERMISSION CHECKS. THE EMBED WILL BE SENT AS IS
        :param paginate_by: What character do you want to paginate by? Only the description will be paginated
        :return: Returns a discord message object
        :raises: discord.HTTPException - sending the message failed
        :raises: discord.Forbidden - you don't have permissions to do this
        :raises: discord.InvalidArgument - both files & file were specified, or files wasn't of a valid length
        """
        if paginate_by is not None:
            description_parts = content.split(paginate_by)
            merged_description_parts = []
            next_description_part = ""
            for pos, part in enumerate(description_parts):
                if part == discord.Embed.Empty:
                    next_description_part = ""
                    merged_description_parts.append(part)
                    continue
                if len(next_description_part) + len(paginate_by) + len(part) > 2000:
                    merged_description_parts.append(next_description_part)
                    next_description_part = ""
                next_description_part += (paginate_by if pos > 0 else "") + part
            if next_description_part != "":
                merged_description_parts.append(next_description_part)
        else:
            merged_description_parts = [content]

        if embed:
            return await self.channel.send(
                embed=embed
            )
        my_perms = self.permissions_for(self.channel.guild.me) \
            if isinstance(self.channel, discord.TextChannel) else None
        messages = []
        if not isinstance(self.channel, discord.TextChannel) or my_perms.embed_links:
            for part in merged_description_parts:
                embed = discord.Embed(
                    title=title,
                    description=part,
                    color=color
                )
                if file:
                    embed.set_image(url="attachment://" + file.filename)
                try:
                    messages.append(await self.channel.send(
                        embed=embed,
                        tts=tts,
                        file=file,
                        files=files,
                        delete_after=delete_after,
                        nonce=nonce,
                    ))
                except discord.HTTPException as e:
                    raise e
        else:
            for part in merged_description_parts:
                part = await self._cleaner.convert(self, part) if part != discord.Embed.Empty else part
                messages.append(
                    await self.channel.send(
                        (f"> **{title}**" if title != discord.Embed.Empty else "") +
                        (f"\n{part}" if part != discord.Embed.Empty else ""),
                        tts=tts,
                        file=file,
                        files=files,
                        delete_after=delete_after,
                        nonce=nonce
                    )
                )
        return messages[0] if paginate_by is None else messages

    async def input(self,
                    title: typing.Union[str, discord.embeds._EmptyEmbed] = discord.Embed.Empty,
                    prompt: typing.Union[str, discord.embeds._EmptyEmbed] = discord.Embed.Empty,
                    paginate_by: typing.Optional[str] = None,
                    required_type: type = str,
                    timeout: int = 60,
                    check: callable = lambda message: True,
                    error: str = "That isn't a valid message",
                    color=discord.Embed.Empty):
        """
        :param title: Set the title of the prompt embed
        :param prompt: Set the description of the prompt embed
        :param paginate_by: Same as send.paginate_by
        :param required_type: Set what type is required, for example int or bool
        :param timeout:
        :param check:
        :param error:
        :param color: Same as the send color argument
        :return: The input from the user
        :raises: Raises a TimeoutError if the timeout is exceeded
        :raises: discord.HTTPException - sending the message failed
        :raises: discord.Forbidden - you don't have permissions to do this
        """

        def message_check(message):
            try:
                if self.author == message.author and self.channel == message.channel:
                    if required_type == bool:
                        if response.content.lower().replace(" ", "") in [
                            "true",
                            "yes",
                            "y",
                            "t",
                            "1",
                            "+",
                            "accept",
                            "allow",
                            "a",
                            "✅",
                            "false",
                            "no",
                            "n",
                            "f",
                            "0",
                            "-",
                            "refuse",
                            "deny",
                            "r",
                            "d",
                            "❌"
                        ]:
                            return True
                        else:
                            asyncio.create_task(self.send(
                                error,
                                title="Oops",
                                color=discord.Color(0xf44336)
                            ))
                            return False
                    required_type(message.content)
                    if check(message):
                        return True
                    else:
                        asyncio.create_task(self.send(
                            error,
                            title="Oops",
                            color=discord.Color(0xf44336)
                        ))
            except ValueError:
                asyncio.create_task(self.send(
                    error,
                    title="Oops",
                    color=discord.Color(0xf44336)
                ))
            return False

        await self.send(
            prompt,
            title=title,
            paginate_by=paginate_by,
            color=color
        )
        response = await self.bot.wait_for(
            "message",
            check=message_check,
            timeout=timeout
        )
        if required_type == bool:
            return response.content.lower().replace(" ", "") \
                   in ["true", "yes", "y", "t", "1", "+", "accept", "allow", "a"], response
        else:
            return required_type(response.content), response

    async def copy_context_with(self, *, author=None, channel=None, **kwargs):
        """
        :param author: Set the member that the "context" was created by
        :param channel: Set the channel that the "context" occurred in
        :param kwargs: Set the arguments that the message will be updated with (such as updating the message's content)
        :return: returns the new MiniContext that was created
        """
        alt_message = copy.copy(self.message)
        alt_message._update(kwargs)

        if author is not None:
            alt_message.author = author
        if channel is not None:
            alt_message.channel = channel

        return await self.bot.get_context(alt_message, cls=MiniContext)


class MiniContextBot(commands.Bot):
    async def get_context(self, message, *, cls=MiniContext):
        return await super().get_context(message, cls=cls)

    def set(self, key, value):
        self.__dict__[key] = value


class AutoShardedMiniContextBot(commands.AutoShardedBot):
    async def get_context(self, message, *, cls=MiniContext):
        return await super().get_context(message, cls=cls)

    def set(self, key, value):
        self.__dict__[key] = value
