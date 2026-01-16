import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from database import init_db

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await init_db()
    await bot.tree.sync()
    print(f"Bot online: {bot.user}")

async def load_cogs():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("BOT_TOKEN"))

import asyncio
asyncio.run(main())
