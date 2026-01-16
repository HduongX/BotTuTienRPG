import discord
from discord.ext import commands
from discord import app_commands
import aiosqlite

DB = "data/bot.db"

class Inventory(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="bag", description="Túi đồ")
    async def bag(self, interaction: discord.Interaction):
        async with aiosqlite.connect(DB) as db:
            cur = await db.execute("""
                SELECT items.name, inventory.amount, items.xp_bonus
                FROM inventory JOIN items ON inventory.item_id = items.item_id
                WHERE inventory.user_id=?
            """, (interaction.user.id,))
            rows = await cur.fetchall()
        if not rows:
            return await interaction.response.send_message("Túi đồ trống")
        msg = ""
        for name, amount, xp in rows:
            msg += f"{name} x{amount} (+{xp} XP)\n"
        await interaction.response.send_message(msg)

async def setup(bot):
    await bot.add_cog(Inventory(bot))