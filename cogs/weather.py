import discord
from discord.ext import commands
import requests
import os


class Weather(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "http://api.weatherapi.com/v1/current.json"

    @commands.command(
        name="weather",
        help="Get the current weather for the entered location. Usage: !weather [Location]",
    )
    async def get_weather(self, ctx, *, location: str):
        weather_params = {"key": self.api_key, "q": location}
        response = requests.get(self.base_url, params=weather_params)

        if response.status_code == 200:
            weather_data = response.json()
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
            await ctx.send(
                f"Sorry, I couldn't find the weather for **{location}**. Please make sure the city exists."
            )
        else:
            await ctx.send(
                "Sorry, Something went wrong when I was checking the weather"
            )
            print(f"Issue Encountered. Weather API status code: {response.status_code}")


async def setup(bot):
    await bot.add_cog(Weather(bot))
