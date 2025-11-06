import discord
from discord import app_commands
from discord.ext import commands
from colorama import Fore, Style

class RegisterModal(discord.ui.Modal, title='Register Character'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    name = discord.ui.TextInput(
        label='Character Name',
        placeholder='Enter character name...',
        max_length=50
    )
    
    textbox_url = discord.ui.TextInput(
        label='Textbox Image URL',
        placeholder='Paste textbox image URL...',
        max_length=500
    )
    
    sprite_url = discord.ui.TextInput(
        label='Sprite Image URL',
        placeholder='Paste sprite image URL...',
        max_length=500
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        name = self.name.value
        
        if name in self.bot.textbox_data:
            await interaction.response.send_message("❌ Character already exists!", ephemeral=True)
            return
            
        self.bot.textbox_data[name] = {
            'textbox_url': self.textbox_url.value,
            'sprite_url': self.sprite_url.value,
            'user_id': interaction.user.id
        }
        
        self.bot.save_data(self.bot.textbox_data)
        print(f'{Fore.GREEN}✅ Registered: {name}')
        await interaction.response.send_message(f"✅ Registered **{name}**!")

class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="textboxregister", description="Register a character with textbox and sprite")
    async def textboxregister(self, interaction: discord.Interaction):
        """Register a character using URLs"""
        print(f'{Fore.YELLOW}🔄 Registration modal opened by {interaction.user}')
        await interaction.response.send_modal(RegisterModal(self.bot))

async def setup(bot):
    await bot.add_cog(Register(bot))