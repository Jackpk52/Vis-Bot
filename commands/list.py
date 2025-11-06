import discord
from discord import app_commands
from discord.ext import commands
from colorama import Fore, Style

class List(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="textboxlist", description="List all characters")
    async def textboxlist(self, interaction: discord.Interaction):
        """List all characters"""
        print(f'{Fore.YELLOW}📋 List command by {interaction.user}')
        
        if not self.bot.textbox_data:
            await interaction.response.send_message("❌ No characters registered!")
            return
        
        embed = discord.Embed(title="📋 Registered Characters", color=0x00ff00)
        for name, data in self.bot.textbox_data.items():
            owner = await self.bot.fetch_user(data['user_id'])
            embed.add_field(name=name, value=f"Owner: {owner.display_name}", inline=True)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(List(bot))