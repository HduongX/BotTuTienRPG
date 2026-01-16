import discord
from discord.ext import commands
from discord import app_commands
import aiosqlite

DB = "data/bot.db"

class Admin(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="addmoney")
    @app_commands.checks.has_permissions(administrator=True)
    async def addmoney(self, interaction: discord.Interaction, user: discord.User, amount: int):
        async with aiosqlite.connect(DB) as db:
            await db.execute("INSERT OR IGNORE INTO users(user_id) VALUES (?)", (user.id,))
            await db.execute("UPDATE users SET xu = xu + ? WHERE user_id=?", (amount, user.id))
            await db.commit()
        await interaction.response.send_message("Đã cộng tiền")

async def setup(bot):
    await bot.add_cog(Admin(bot))