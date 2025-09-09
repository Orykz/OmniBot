import discord
from discord.ext import commands
import requests
import random


class Memes(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.base_url = "https://meme-api.com/gimme"

    @commands.command(name="meme", help="Sends a random meme from Reddit.")
    async def get_meme(self, ctx):
        subreddits = ["memes", "dankmemes", "wholesomememes"]
        chosen_subreddit = random.choice(subreddits)
        url = f"{self.base_url}/{chosen_subreddit}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get("nsfw") or data.get("spoiler"):
                await ctx.send("Got a NSFW/spoiler meme, trying again...")
                await self.get_meme(ctx)
                return

            embed = discord.Embed(
                title=data["title"], url=data["postLink"], color=discord.Color.orange()
            )

            embed.set_image(url=data["url"])
            embed.set_footer(text=f"From r/{data['subreddit']} by u/{data['author']}")

            await ctx.send(embed=embed)

        except requests.exceptions.RequestException as e:
            await ctx.send(
                "Could not fetch a meme at this time. Please try again later."
            )
            print(f"Encountered error when fetching meme: {e}")


async def setup(bot):
    await bot.add_cog(Memes(bot))
