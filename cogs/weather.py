import discord
from discord.ext import commands
import requests

from typing import Dict, Any

from config import WEATHER_API_KEY
from errors import ERRORS, CLIENT_ERRORS, WEATHER_API_ERROR, WEATHER_404_ERROR


class Weather(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.api_key = WEATHER_API_KEY
        self.base_url = "http://api.weatherapi.com/v1/current.json"

    @commands.command(
        name="weather",
        help="Get the current weather for the entered location. Usage: !weather [Location]",
    )
    async def get_weather(self, ctx: commands.Context, *, location: str) -> None:
        weather_params = {"key": self.api_key, "q": location}
        response = requests.get(self.base_url, params=weather_params)

        if response.status_code == 200:
            weather_data: Dict[str, Any] = response.json()
            location_data = weather_data["location"]
            current_weather = weather_data["current"]
            weather_cond = current_weather["condition"]

            embed = discord.Embed(
                title=f"Weather in {location_data['name']}, {location_data['region']}, {location_data['country']}",
                description=f"Feels like {current_weather['feelslike_c']:.1f}°C. {weather_cond['text'].title()}.",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="Temperature",
                value=f"{current_weather['temp_c']:.1f}°C",
                inline=True,
            )
            embed.add_field(
                name="Humidity", value=f"{current_weather['humidity']}%", inline=True
            )
            embed.add_field(
                name="Wind Speed",
                value=f"{current_weather['wind_kph']:.1f} km/h",
                inline=True,
            )
            embed.set_thumbnail(url=f"http:{weather_cond['icon']}")
            embed.set_footer(text="Powered by WeatherAPI.com")
            await ctx.send(embed=embed)

        elif response.status_code == 404:
            print(ERRORS[WEATHER_404_ERROR])
            message = CLIENT_ERRORS[WEATHER_404_ERROR].replace("<location>", location)
            await ctx.send(message)
        else:
            print(f"{ERRORS[WEATHER_API_ERROR]} http response: {response.status_code}")
            message = CLIENT_ERRORS[WEATHER_API_ERROR]
            await ctx.send(message)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Weather(bot))
