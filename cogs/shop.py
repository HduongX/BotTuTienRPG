import discord
from discord.ext import commands
from discord import app_commands
import aiosqlite

DB = "data/bot.db"

class ShopView(discord.ui.View):
    def __init__(self, items):
        super().__init__(timeout=60)
        self.items = items

        options = [discord.SelectOption(label=i[1], description=f"Giá: {i[3]} xu") for i in items]
        self.select = discord.ui.Select(placeholder="Chọn item", options=options)
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction):
        item = self.items[self.select.values.index(self.select.values[0])]
        async with aiosqlite.connect(DB) as db:
            await db.execute("INSERT OR IGNORE INTO inventory(user_id, item_id, amount) VALUES (?,?,0)",
                             (interaction.user.id, item[0]))
            await db.execute("UPDATE inventory SET amount = amount + 1 WHERE user_id=? AND item_id=?",
                             (interaction.user.id, item[0]))
            await db.commit()
        await interaction.response.send_message(f"Đã mua {item[1]}", ephemeral=True)

class Shop(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @app_commands.command(name="shop", description="Mở shop")
    async def shop(self, interaction: discord.Interaction):
        async with aiosqlite.connect(DB) as db:
            cur = await db.execute("SELECT * FROM items")
            items = await cur.fetchall()
        if not items:
            return await interaction.response.send_message("Shop trống")
        await interaction.response.send_message("🛒 SHOP", view=ShopView(items))

async def setup(bot):
    await bot.add_cog(Shop(bot))