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
    def _change_data_format(self, rows: List[Any]) -> List[Reminder]:
        reminder_list: List[Reminder] = []
        for row in rows:
            reminder_list.append(Reminder._make(row))

        return reminder_list

    @connect_db
    def create_table(self, cursor: Optional[sqlite3.Cursor] = None) -> None:
        """Create the reminders table if it doesn't exist."""
        if cursor is None:
            raise RuntimeError()

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
        """Get all reminders that have elapsed with the given time."""
        if cursor is None:
            raise RuntimeError("missing database connection")

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
        """Store the reminder to the database"""
        if cursor is None:
            raise RuntimeError("missing database connection")

        cursor.execute(
            "insert into reminders (user_id, reminder_time, message, jump_url) values (?, ?, ?, ?)",
            (user_id, reminder_time, message, jump_url),
        )

    @connect_db
    def delete_reminder(self, rem_id: int, cursor: Optional[sqlite3.Cursor] = None):
        if cursor is None:
            raise RuntimeError("missing database connection")

        cursor.execute("delete from reminders where id = ?", (rem_id,))
