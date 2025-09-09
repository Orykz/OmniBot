from discord.ext import commands
import asyncio


class Reminders(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(
        name="remindme", help="Sets a reminder. Usage: !remind [time] [message]"
    )
    async def remind_me(self, ctx, time: str, *, message: str | None = None):
        reminder_content = ""
        ctx_jump_url = ""

        if ctx.message.reference and ctx.message.reference.message_id:
            replied_to_message = await ctx.fetch_message(
                ctx.message.reference.message_id
            )
            ctx_jump_url = replied_to_message.jump_url

            if message:
                reminder_content = f"your note about this message: '{message}'"
            else:
                reminder_content = "this message"

        elif message:
            reminder_content = message

        else:
            await ctx.send(
                "Invalid command format. Please use `!remindme <time><unit> <message>` (e.g., `!remindme 10m check the oven`) you can also use the command as a reply."
            )
            return

        try:
            time_unit = time[-1].lower()
            duration = int(time[:-1])

            if time_unit == "s":
                delay = duration
            elif time_unit == "m":
                delay = duration * 60
            elif time_unit == "h":
                delay = duration * 3600
            else:
                await ctx.send("Invalid time format! Please use 's', 'm', or 'h'.")
                return

            if delay > 86400:  # 24 hours
                await ctx.send(
                    "Sorry, I can only set reminders up to 24 hours in advance."
                )
                return

            await ctx.send(f"Got it! I will remind you in **{duration}{time_unit}**.")
            await asyncio.sleep(delay)

            if ctx_jump_url:
                await ctx.author.send(
                    f"**Reminder!** You asked me to remind you about {reminder_content}\n{ctx_jump_url}"
                )
            else:
                await ctx.author.send(
                    f"**Reminder!** You asked me to remind you about {reminder_content}"
                )

        except (IndexError, ValueError):
            await ctx.send(
                "Invalid command format. Please use `!remindme <time><unit> <message>` (e.g., `!remindme 10m check the oven`) you can also use the command as a reply."
            )


async def setup(bot):
    await bot.add_cog(Reminders(bot))
