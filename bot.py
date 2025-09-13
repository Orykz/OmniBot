import discord
from discord.ext import commands
import os
import asyncio
from config import DISCORD_TOKEN


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def load_cogs() -> None:
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"loaded cog: {filename}")


async def unload_cogs() -> None:
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.unload_extension(f"cogs.{filename[:-3]}")
            print(f"unloaded cog: {filename}")


@bot.event
async def on_ready() -> None:
    if bot.user is not None:
        print(f"Logged in as {bot.user.name} ({bot.user.id})")
        print(f"{bot.user.name} is ready to go!")
    else:
        print("Bot is not connected. Exiting the application.")
        exit()


async def main() -> None:
    await load_cogs()
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
