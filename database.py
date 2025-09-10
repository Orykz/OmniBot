import sqlite3
from datetime import datetime
from typing import List, NamedTuple


class Reminder(NamedTuple):
    id: int
    user_id: int
    reminder_time: datetime
    message: str
    jump_url: str | None


class DatabaseHandler:
    def __init__(self) -> None:
        self.open_connection()

    def open_connection(self):
        self.con = sqlite3.connect("reminders.db")
        self.cursor = self.con.cursor()

    def close_connection(self):
        self.con.close()

    def change_data_format(self, rows):
        reminder_list = []
        for row in rows:
            reminder_list.append(Reminder._make(row))

        return reminder_list

    def create_table(self):
        """Create the reminders table if it doesn't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                reminder_time TIMESTAMP NOT NULL,
                message TEXT NOT NULL,
                jump_url TEXT
            )
        """)
        self.con.commit()

    def get_reminders(self, given_time: datetime) -> List[Reminder]:
        """Get all reminders that have elapsed with the given time."""
        result = self.cursor.execute(
            "select * from reminders where reminder_time <= ?", (given_time,)
        )
        reminders = result.fetchall()
        return self.change_data_format(reminders)

    def set_reminder(
        self,
        user_id: int,
        reminder_time: datetime,
        message: str,
        jump_url: str | None = None,
    ):
        """Store the reminder to the database"""
        self.cursor.execute(
            "insert into reminders (user_id, reminder_time, message, jump_url) values (?, ?, ?, ?)",
            (user_id, reminder_time, message, jump_url),
        )
        self.con.commit()

    def delete_reminder(self, rem_id: int):
        self.cursor.execute("delete from reminders where id = ?", (rem_id,))
        self.con.commit()
