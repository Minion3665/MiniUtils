import typing
import inspect
import asyncio
import functools
import discord


def is_coroutine_function_or_partial(obj):
    while isinstance(obj, functools.partial):
        obj = obj.func
    return inspect.iscoroutinefunction(obj)


class Menu:
    def __init__(self, bot, timeout: int = 60, callbacks: bool = False,
                 timeout_callback: typing.Union[typing.Callable, typing.Coroutine] = None):
        self.__bot = bot
        self.__reactions = {}
        self.__callbacks = callbacks
        self.timeout = timeout
        self.timeout_callback = timeout_callback

    async def __call__(self, message, responding):
        async def add_reactions():
            for react in self.__reactions.keys():
                try:
                    await message.add_reaction(react)
                except discord.HTTPException as e:
                    print(e)
                    pass

        self.__bot.loop.create_task(add_reactions())

        def react_check(react, member):
            if react.message.id != message.id:
                return False
            if member == self.__bot.user:
                return False
            if not self.__reactions.get(react.emoji):
                self.__bot.loop.create_task(react.remove(member))
                return False
            if member != responding:
                self.__bot.loop.create_task(react.remove(member))
                return False
            return True

        def message_check(msg):
            if not self.__reactions.get(msg.content):
                return False
            if msg.author != responding:
                return False
            if msg.channel != message.channel:
                return False
            return True

        try:
            completed, cancelled = await asyncio.wait(
                [
                    self.__bot.wait_for("reaction_add", check=react_check, timeout=self.timeout),
                    self.__bot.wait_for("message", check=message_check, timeout=self.timeout),
                ],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in cancelled:
                task.cancel()

            completed = list(completed)[0].result()  # type: typing.Union[tuple, discord.message]

            if isinstance(completed, tuple):
                reaction = completed[0].emoji
            else:
                if message.guild:
                    perms = message.channel.permissions_for(message.guild.me)
                    # Get our permissions in the current channel
                    if isinstance(message.channel, discord.abc.GuildChannel) and perms.manage_messages:
                        await completed.delete()
                reaction = completed.content

            if not self.__callbacks:
                return reaction
            elif is_coroutine_function_or_partial(self.__reactions.get(reaction)):
                return await self.__reactions.get(reaction)()
            else:
                return self.__reactions.get(reaction)()
        except asyncio.TimeoutError as e:
            if not self.__callbacks:
                raise e
            elif not self.timeout_callback:
                return "timed out"
            elif is_coroutine_function_or_partial(self.timeout_callback):
                return await self.timeout_callback()
            else:
                return self.timeout_callback()

    def add(self, reaction, callback: typing.Union[typing.Callable, typing.Coroutine] = None):
        if self.__callbacks:
            if callback:
                self.__reactions[reaction] = callback
            else:
                return False
        else:
            self.__reactions[reaction] = "return"
        return True

    def remove(self, reaction):
        try:
            del self.__reactions[reaction]
            return True
        except KeyError:
            return False

    def list(self):
        return self.__reactions

    def callbacks(self):
        return self.__callbacks
