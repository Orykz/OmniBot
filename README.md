# OmniBot - A Multi-Purpose Discord Bot

A versatile, easy-to-use Discord bot built with Python and the discord.py library. OmniBot provides a range of useful features to enhance any Discord server.

### Features

OmniBot is packed with features, all organized into modular cogs for easy maintenance and expansion:

- **Checks Weather**: Get real-time weather updates for any location in the world, using WeatherAPI.com  
- **Sends Memes**: Fetches random memes from your chosen subreddits, using meme-api.com  
- **Reminders**: Set reminders for yourself for minutes, hours, days, or even weeks. Reminders are stored in a database and will persist even if the bot restarts. You can even reply to a message to set a reminder with context!  

### Setup and Installation

To get OmniBot running on your own server, follow these steps.
#### 1. Prerequisites

- Python **[YOUR-PYTHON-VERSION, e.g., 3.12 or newer]**  
- uv package to install dependencies  
- Discord Bot Token  
- An WeatherAPI.com key  

#### 2. Clone the Repository

Clone this project to your local machine:
```
git clone [YOUR-REPOSITORY-URL-HERE]
cd [YOUR-PROJECT-FOLDER-NAME]
```

#### 3. Install Dependencies

First, create a virtual environment in your project folder with `uv venv`.  
Then, install all the required Python libraries using `uv sync`.

#### 4. Configure Environment Variables and Configurations

- To get your DISCORD_TOKEN, create an application on the Discord Developer Portal.  
- To get a WeatherAPI.com API key, sign up on their website [WeatherAPI.com](https://www.weatherapi.com/).
  
Create environment variables for `DISCORD_TOKEN` and `WEATHER_API_KEY`. Place your keys in their respective variables.  

If you do not want to setup environment variables, you can do this instead:  
Create a data folder in your project directory.  
In that folder, create the `.env` file. This is where you will store your secret keys and tokens.
```
DISCORD_TOKEN=<token>
WEATHER_API_KEY=<weather_api_key>
```  
    
For the Configs, create a `config.json` file under your data folder. This is where you will store all your configurations.
```
{
    "database": {
        "db_path": "data/<name of your db>.db"
    },
    "memes": {
        "base_url": "https://meme-api.com/gimme",
        "subreddits": [<list of subreddits>],
        "allow_nsfw": false
    },
    "weather": {
        "base_url": "http://api.weatherapi.com/v1/",
        "current": "current.json"
    },
    "reminders": {
        "loop_sec": 30,
        "note_ind": "note:"
    }
}
```


#### 5. Run the Bot

Once everything is configured, you can start the bot with the following command (Do not forget to add your bot to the server):
```
python bot.py
```

Usage Examples

Here are some of the commands you can use with OmniBot (default prefix is !):  
- **!weather [location]**: Get the weather for a location (e.g., `!weather manila`).  
- **!meme**: receive a random meme.  
- **!remindme [time] note:[message]**: Set a reminder (e.g., `!remindme 2 days note: Check on the report`).  
Reply to a message with **!remindme [time]**: Sets a reminder for that specific message.  


### License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

Copyright (c) 2025 Jero Pardo