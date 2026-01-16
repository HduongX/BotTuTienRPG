import discord, os, asyncio
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

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run(os.getenv("BOT_TOKEN"))