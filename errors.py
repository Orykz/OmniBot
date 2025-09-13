from typing import Dict

(
    SUCCESS,
    FILE_404_ERROR,
    DB_TRANSACT_ERROR,
    DB_INTERNAL_ERROR,
    DB_PROGRAM_ERROR,
    DB_DATA_ERROR,
    DIRECT_MESSAGE_ERROR,
    KEY_ERROR,
    WEATHER_API_ERROR,
    WEATHER_404_ERROR,
    MEME_API_ERROR,
    INVALID_REMINDER_ERROR,
) = range(12)


ERRORS: Dict[int, str] = {
    FILE_404_ERROR: "file does not exist",
    DB_TRANSACT_ERROR: "Problem encountered during database transaction",
    DB_INTERNAL_ERROR: "Invalid database reference used",
    DB_PROGRAM_ERROR: "Issue with the database system",
    DB_DATA_ERROR: "Invalid value has been entered in the database",
    DIRECT_MESSAGE_ERROR: "Could not send a direct message to user",
    KEY_ERROR: "issue encountered with the API keys",
    WEATHER_API_ERROR: "Something went wrong with the weather API",
    WEATHER_404_ERROR: "Weather for the location is not found",
    MEME_API_ERROR: "Could not access the meme API",
    INVALID_REMINDER_ERROR: "Invalid command has been entered",
}

CLIENT_ERRORS: Dict[int, str] = {
    FILE_404_ERROR: "I seem to be missing my limbs. Please tell someone to attach them.",
    DB_TRANSACT_ERROR: "AAHHH! something went wrong accessing my storage. Please call the medic",
    DB_INTERNAL_ERROR: "AAHHH! something went wrong accessing my storage. Please call the medic",
    DB_PROGRAM_ERROR: "AAHHH! something went wrong accessing my storage. Please call the medic",
    DB_DATA_ERROR: "AAHHH! something went wrong accessing my storage. Please call the medic",
    KEY_ERROR: "AAHHH, I am not authorized to do anything!",
    DIRECT_MESSAGE_ERROR: "Hey <user>! you told me to send you a DM but you blocked me!",
    WEATHER_API_ERROR: "I could not see the weather at the moment. Sorry...",
    WEATHER_404_ERROR: "This location does not exist for me: <location>. Please input something that exists next time :)",
    MEME_API_ERROR: "MEME-er is down :(",
    INVALID_REMINDER_ERROR: "Invalid command format. Please use `!remindme <time> note:<message>` (`!remindme 10m check the oven`). You can also use the command when replying",
}


class DBError(Exception):
    def __init__(self, error_code: int, function_name: str) -> None:
        self.message = ERRORS[error_code]
        self.code = error_code
        self.function_name = function_name
        super().__init__(
            f"error({self.code}): {self.message}; function name: {self.function_name}"
        )
