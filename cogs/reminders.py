import discord
from discord.ext import commands, tasks
import parsedatetime

from datetime import datetime, timezone
from database import DatabaseHandler, Reminder
from errors import ERRORS, CLIENT_ERRORS, INVALID_REMINDER_ERROR, DIRECT_MESSAGE_ERROR


class Reminders(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.cal = parsedatetime.Calendar()
        self.db_handler = DatabaseHandler()
        self.db_handler.create_table()
        self.check_reminders.start()

    async def cog_unload(self):
        self.check_reminders.cancel()
        await super().cog_unload()

    @commands.command(
        name="remindme", help="Sets a reminder. Usage: !remind [time] [message]"
    )
    async def remind_me(self, ctx: commands.Context, *, text: str):
        reminder_content = ""
        jump_url = ""

        split_data = text.split("note:")
        time_set = split_data[0]
        message = split_data[1] if len(split_data) > 1 else None
        parsed_time, parse_status = self.cal.parse(time_set)

        try:
            if not parse_status:
                raise ValueError

            time_data = datetime(*parsed_time[:6])
            time_data_utc = time_data.astimezone(timezone.utc)

            if ctx.message.reference and ctx.message.reference.message_id:
                replied_to_message = await ctx.fetch_message(
                    ctx.message.reference.message_id
                )
                jump_url = replied_to_message.jump_url

            if message:
                reminder_content = message

            self.db_handler.set_reminder(
                ctx.author.id, time_data_utc, reminder_content, jump_url
            )
            await ctx.send("Got it! I will remind you in the designated time.")

        except Exception:
            print(ERRORS[INVALID_REMINDER_ERROR])
            error = CLIENT_ERRORS[INVALID_REMINDER_ERROR]
            await ctx.send(error)
            return

    async def send_reminder(self, reminder: Reminder):
        user = self.bot.get_user(reminder.user_id)

        if user:
            try:
                if reminder.jump_url:
                    await user.send(
                        f"**Reminder!** {reminder.message}\n{reminder.jump_url}"
                    )
                else:
                    await user.send(f"**Reminder!** {reminder.message}")

            except discord.Forbidden:
                print(ERRORS[DIRECT_MESSAGE_ERROR])

        self.db_handler.delete_reminder(reminder.id)

    @tasks.loop(seconds=5)
    async def check_reminders(self):
        await self.bot.wait_until_ready()
        now_utc = datetime.now(timezone.utc)
        reminders_to_send = self.db_handler.get_reminders(now_utc)

        for reminder in reminders_to_send:
            print(f"set a reminder to user(id): {reminder.user_id}")
            await self.send_reminder(reminder)


async def setup(bot: commands.Bot):
    await bot.add_cog(Reminders(bot))
