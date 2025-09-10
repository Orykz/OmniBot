from typing import Dict

(
    SUCCESS,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    DB_EXISTS_ERROR,
    DIRECT_MESSAGE_ERROR,
    KEY_ERROR,
    WEATHER_API_ERROR,
    WEATHER_404_ERROR,
    MEME_API_ERROR,
    INVALID_REMINDER_ERROR,
) = range(11)


ERRORS: Dict[int, str] = {
    FILE_ERROR: "cannot access the env file",
    DB_READ_ERROR: "Cannot read the database",
    DB_WRITE_ERROR: "Issue with writing to the database",
    DB_EXISTS_ERROR: "database already exists",
    DIRECT_MESSAGE_ERROR: "Could not send a direct message to user",
    KEY_ERROR: "issue encountered with the API keys",
    WEATHER_API_ERROR: "Something went wrong with the weather API",
    WEATHER_404_ERROR: "Weather for the location is not found",
    MEME_API_ERROR: "Could not access the meme API",
    INVALID_REMINDER_ERROR: "Invalid command has been entered",
}

CLIENT_ERRORS: Dict[int, str] = {
    FILE_ERROR: "I seem to be missing my limbs. Please tell someone to attach them.",
    DB_READ_ERROR: "I forgot my storage keys, please tell my dev",
    DB_WRITE_ERROR: "Hmmm, there is something wrong with my storage. HELP!",
    DB_EXISTS_ERROR: "AYAYA! my storage was not configured properly",
    KEY_ERROR: "AAHHH, I am not authorized to do anything!",
    DIRECT_MESSAGE_ERROR: "Hey <user>! you told me to send you a DM but you blocked me!",
    WEATHER_API_ERROR: "I could not see the weather at the moment. Sorry...",
    WEATHER_404_ERROR: "This location does not exist for me: <location>. Please input something that exists next time :)",
    MEME_API_ERROR: "MEME-er is down :(",
    INVALID_REMINDER_ERROR: "Invalid command format. Please use `!remindme <time> note:<message>` (`!remindme 10m check the oven`). You can also use the command when replying",
}
