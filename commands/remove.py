import discord
from discord import app_commands
from discord.ext import commands
from colorama import Fore, Style

class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="textboxremove", description="Remove a character")
    @app_commands.describe(name="Character name to remove")
    async def textboxremove(self, interaction: discord.Interaction, name: str):
        """Remove a character"""
        print(f'{Fore.YELLOW}🔄 Remove attempt by {interaction.user} for character: {name}')
        
        if name not in self.bot.textbox_data:
            await interaction.response.send_message("❌ Character not found!", ephemeral=True)
            return
            
        if self.bot.textbox_data[name]['user_id'] != interaction.user.id:
            await interaction.response.send_message("❌ Not your character!", ephemeral=True)
            return

        del self.bot.textbox_data[name]
        self.bot.save_data(self.bot.textbox_data)
        print(f'{Fore.GREEN}✅ Successfully removed: {name}')
        await interaction.response.send_message(f"✅ Removed **{name}**!")

async def setup(bot):
    await bot.add_cog(Remove(bot))