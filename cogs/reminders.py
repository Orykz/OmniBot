import discord
from discord.ext import commands, tasks
import parsedatetime
from datetime import datetime, timezone
from database import DatabaseHandler, Reminder
from config import REM_LOOP_SEC, REM_NOTE_IND
from errors import (
    DBError,
    ERRORS,
    CLIENT_ERRORS,
    INVALID_REMINDER_ERROR,
    DIRECT_MESSAGE_ERROR,
)


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

        split_data = text.split(REM_NOTE_IND)
        time_set = split_data[0]
        message = split_data[1].strip() if len(split_data) > 1 else None
        parsed = self.cal.parseDT(time_set)  # returns a tuple (result, flag)
        parsed_time: datetime = parsed[0]
        parse_status = parsed[1]

        try:
            if not parse_status:
                raise ValueError

            if ctx.message.reference and ctx.message.reference.message_id:
                replied_to_message = await ctx.fetch_message(
                    ctx.message.reference.message_id
                )
                jump_url = replied_to_message.jump_url

            if message is not None:
                reminder_content = f"\nNote: {message}"

            time_data_utc = parsed_time.astimezone(timezone.utc)
            self.db_handler.set_reminder(
                ctx.author.id, time_data_utc, reminder_content, jump_url
            )
            await ctx.send("Got it! I will remind you in the designated time.")

        except ValueError:
            print(ERRORS[INVALID_REMINDER_ERROR])
            error = CLIENT_ERRORS[INVALID_REMINDER_ERROR]
            await ctx.send(error)
        except DBError as e:
            print(e)
            error = CLIENT_ERRORS[e.code]
            await ctx.send(error)

    async def send_reminder(self, reminder: Reminder) -> None:
        """Function for the bot to send reminder to the user.

        Args:
            reminder (Reminder): Reminder object.

        Raises:
            discord.Forbidden: If user does not allow direct messages.
        """
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

    @tasks.loop(seconds=REM_LOOP_SEC)
    async def check_reminders(self):
        """This will check all reminders in database that have their time elapsed, follows the UTC timezone. (Default loop: 30s)"""
        await self.bot.wait_until_ready()
        now_utc = datetime.now(timezone.utc)
        reminders_to_send = self.db_handler.get_reminders(now_utc)

        for reminder in reminders_to_send:
            try:
                print(f"set a reminder to user(id): {reminder.user_id}")
                self.db_handler.delete_reminder(reminder.id)
                await self.send_reminder(reminder)
            except DBError as e:
                print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(Reminders(bot))
