from discord.ext import commands
import traceback
import contextlib


# Handles Exception
async def handle_all(ctx, _error, _next):
    exceptions_channel = ctx.bot.get_channel(ctx.bot.exceptions_channel)
    ctx.bot.case += 1
    case_id = str(ctx.bot.exceptions_case_prefix) + str(ctx.message.id).zfill(4)[-4:-1] + str(ctx.bot.case)

    paginator = commands.Paginator(prefix=f"```py\n")
    paginator.add_line(f"Uncaught {type(_error).__name__} with case ID {case_id}")
    paginator.add_line(f"Full type of the error is {type(_error)}")
    for index in range(0, len(str(_error)), 1950):
        paginator.add_line(str(_error)[index:index + 1950])

    full_trace = "\n- [x] " + "".join(traceback.format_exception(
        etype=type(_error), value=_error, tb=_error.__traceback__
    )).replace("\n", "\n- [x] ")
    for index in range(0, len(full_trace), 1950):
        paginator.add_line(full_trace[index:index + 1950])

    try:
        exceptions_channel = await ctx.copy_context_with(channel=exceptions_channel)

        await exceptions_channel.send_exception(
            ctx.message.content,
            title=f"Case {case_id} - Full Message"
        )

        for message in paginator.pages:
            await exceptions_channel.send_exception(
                message,
                title=f"Case {case_id} - Traceback"
            )

        exception_message = ""
        exception_message += f"Author: {ctx.author} (`{ctx.author.id}`)\n"
        exception_message += f"Command: `{ctx.command.qualified_name}`\n"

        if ctx.guild:
            exception_message += f"\n"

            my_permissions_list = []
            for (permission, value) in ctx.channel.permissions_for(ctx.me):
                if value:
                    my_permissions_list.append(permission)
            author_permissions_list = []
            for (permission, value) in ctx.channel.permissions_for(ctx.author):
                if value:
                    author_permissions_list.append(permission)

            exception_message += f"Message Link: " \
                                 f"{ctx.message.jump_url}\n"
            exception_message += f"My Permissions: `{', '.join(my_permissions_list)}`\n"
            exception_message += f"Their Permissions: `{', '.join(author_permissions_list)}`\n"

            if ctx.channel.permissions_for(ctx.me).create_instant_invite:
                try:
                    invite = await ctx.channel.create_invite(
                        unique=False,
                        max_age=0,
                        max_uses=0,
                        reason="One of my commands caused an error! I'm inviting my developers to check it out"
                    )
                    exception_message += f"Infinite Invite: `{invite.url}`"
                except Exception as e:
                    exception_message += f"Creating an invite failed"
                    await exceptions_channel.send_exception(
                        str(e),
                        title=f"Creating an invite failed in case `{case_id}`"
                    )
            else:
                exception_message += f"I don't have permissions to create an invite"
        else:
            exception_message += f"Message ID: {ctx.message.id}\n"
            exception_message += f"Channel ID: {ctx.channel.id}"

        await exceptions_channel.send_exception(
            exception_message,
            title=f"Case {case_id} - Context",
        )
    except AttributeError as e:
        print(e)
    with contextlib.suppress(Exception):
        await ctx.send_exception(
            f"I messed up, somehow. Nobody really knows how though. Try sending the case ID `{case_id}` to my "
            f"developers and see if they can sort it out."
            f"{f' My support server is {ctx.bot.support_invite}' if ctx.bot.support_invite else ''}",
            title="Oops..."
        )


def setup(handler):
    handler.handles(
        Exception
    )(handle_all)
