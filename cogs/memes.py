import discord
from discord.ext import commands
import requests

import random
from typing import Dict, Any

from errors import ERRORS, CLIENT_ERRORS, MEME_API_ERROR


class Memes(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.base_url = "https://meme-api.com/gimme"
        self.subreddits = ["memes", "dankmemes", "KanalHumor"]
        self.allow_nsfw = False

    @commands.command(name="meme", help="Sends a random meme from Reddit.")
    async def get_meme(self, ctx: commands.Context) -> None:
        chosen_subreddit = random.choice(self.subreddits)
        url = f"{self.base_url}/{chosen_subreddit}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data: Dict[str, Any] = response.json()

            if not self.allow_nsfw:
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
            print(f"{ERRORS[MEME_API_ERROR]}: {e}")
            message = CLIENT_ERRORS[MEME_API_ERROR]
            await ctx.send(message)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Memes(bot))
