import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite

DB = "data/bot.db"

class Economy(commands.Cog):
    def __init__(self, bot): self.bot = bot

    async def get_user(self, uid):
        async with aiosqlite.connect(DB) as db:
            await db.execute("INSERT OR IGNORE INTO users(user_id) VALUES (?)", (uid,))
            await db.commit()

    @app_commands.command(name="balance", description="Xem số tiền")
    async def balance(self, interaction: discord.Interaction):
        await self.get_user(interaction.user.id)
        async with aiosqlite.connect(DB) as db:
            cur = await db.execute("SELECT xu FROM users WHERE user_id=?", (interaction.user.id,))
            xu = (await cur.fetchone())[0]
        await interaction.response.send_message(
            f"Xu: {xu}\nBạc: {xu//100}\nNgân: {xu//1000}\nKim: {xu//10000}")

    @app_commands.command(name="pay", description="Chuyển xu")
    async def pay(self, interaction: discord.Interaction, user: discord.User, amount: int):
        if amount <= 0:
            return await interaction.response.send_message("Số tiền không hợp lệ", ephemeral=True)
        async with aiosqlite.connect(DB) as db:
            cur = await db.execute("SELECT xu FROM users WHERE user_id=?", (interaction.user.id,))
            row = await cur.fetchone()
            if not row or row[0] < amount:
                return await interaction.response.send_message("Không đủ tiền", ephemeral=True)
            await db.execute("UPDATE users SET xu = xu - ? WHERE user_id=?", (amount, interaction.user.id))
            await db.execute("INSERT OR IGNORE INTO users(user_id) VALUES (?)", (user.id,))
            await db.execute("UPDATE users SET xu = xu + ? WHERE user_id=?", (amount, user.id))
            await db.commit()
        await interaction.response.send_message(f"Đã chuyển {amount} xu cho {user.mention}")

async def setup(bot):
    await bot.add_cog(Economy(bot))