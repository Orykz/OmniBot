import sqlite3
import functools
from datetime import datetime
from collections.abc import Callable
from typing import List, NamedTuple, Any, Optional, cast
from config import DB_PATH
from errors import (
    DBError,
    DB_DATA_ERROR,
    DB_INTERNAL_ERROR,
    DB_PROGRAM_ERROR,
    DB_TRANSACT_ERROR,
)


def connect_db[T, **P](func: Callable[P, T]) -> Callable[P, T]:
    """Helper for DatabaseHandler class. Wraps the method (database transaction) for database connection.

    Raises:
        DBError: custom exception DBError is raised if issues were encountered.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                kwargs["cursor"] = conn.cursor()
                result = func(*args, **kwargs)
                conn.commit()
                return result
        except sqlite3.DataError:
            raise DBError(DB_DATA_ERROR, func.__name__)
        except sqlite3.OperationalError:
            raise DBError(DB_TRANSACT_ERROR, func.__name__)
        except sqlite3.ProgrammingError:
            raise DBError(DB_PROGRAM_ERROR, func.__name__)
        except sqlite3.InternalError:
            raise DBError(DB_INTERNAL_ERROR, func.__name__)

    return cast(Callable[P, T], wrapper)


class Reminder(NamedTuple):
    id: int
    user_id: int
    reminder_time: datetime
    message: str
    jump_url: str | None


class DatabaseHandler:
    """Handles all the database access.

    Methods:
        create_table: Create the reminders table if it doesn't exist.
        get_reminders: Get all reminders that have elapsed with the given time.
        set_reminder: Store the reminder requested by the user to the database.
        delete_reminder: Delete the reminder row based on id from the database.
    """

    def _change_data_format(self, rows: List[Any]) -> List[Reminder]:
        reminder_list: List[Reminder] = []
        for row in rows:
            reminder_list.append(Reminder._make(row))

        return reminder_list

    @connect_db
    def create_table(self, cursor: Optional[sqlite3.Cursor] = None) -> None:
        """Create the reminders table if it doesn't exist."""
        if cursor is None:
            raise sqlite3.InternalError

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                reminder_time TIMESTAMP NOT NULL,
                message TEXT NOT NULL,
                jump_url TEXT
            )
        """)

    @connect_db
    def get_reminders(
        self, given_time: datetime, cursor: Optional[sqlite3.Cursor] = None
    ) -> List[Reminder]:
        """Get all reminders that have elapsed with the given time.

        Args:
            given_time (datetime): the datetime to compare if reminder time has elapsed.

        Returns:
            List[Reminder]: List of Reminder objects
        """
        if cursor is None:
            raise sqlite3.InternalError

        result = cursor.execute(
            "select * from reminders where reminder_time <= ?", (given_time,)
        )
        reminders = result.fetchall()
        return self._change_data_format(reminders)

    @connect_db
    def set_reminder(
        self,
        user_id: int,
        reminder_time: datetime,
        message: str,
        jump_url: Optional[str] = None,
        cursor: Optional[sqlite3.Cursor] = None,
    ) -> None:
        """Store the reminder requested by the user to the database.

        Args:
            user_id (int): The user that requested a reminder
            reminder_time (datetime): Datetime value for when to send out the reminder
            message (str): The provided note for the reminder, if any.
            jump_url (Optional[str]): the url of the replied message if command was triggered as a reply.
        """
        if cursor is None:
            raise sqlite3.InternalError

        cursor.execute(
            "insert into reminders (user_id, reminder_time, message, jump_url) values (?, ?, ?, ?)",
            (user_id, reminder_time, message, jump_url),
        )

    @connect_db
    def delete_reminder(
        self, rem_id: int, cursor: Optional[sqlite3.Cursor] = None
    ) -> None:
        """Delete the reminder row based on id from the database.

        Args:
            rem_id (int): The id of the reminder in the database.
        """
        if cursor is None:
            raise sqlite3.InternalError

        cursor.execute("delete from reminders where id = ?", (rem_id,))
