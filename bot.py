import discord
from discord.ext import commands

import os
import asyncio
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"loaded cog: {filename}")


@bot.event
async def on_ready():
    if bot.user is not None:
        print(f"Logged in as {bot.user.name} ({bot.user.id})")
        print("OmniBot is ready to go!")
    else:
        print("Bot is not connected. Exiting the application.")
        exit()


@bot.command(name="hello")
async def greet(ctx):
    await ctx.send(
        f"Hello, {ctx.author.mention}! I am OmniBot, an all purpose discord bot."
    )


async def main():
    if not load_dotenv():
        print(".env file not found. Exiting the application.")
        exit()

    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

    await load_cogs()
    await bot.start(DISCORD_TOKEN)  # type: ignore


if __name__ == "__main__":
    asyncio.run(main())
