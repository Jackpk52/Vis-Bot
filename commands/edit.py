import discord
from discord import app_commands
from discord.ext import commands
from colorama import Fore, Style

class EditModal(discord.ui.Modal, title='Edit Character'):
    def __init__(self, bot, name):
        super().__init__()
        self.bot = bot
        self.character_name = name
    
    textbox_url = discord.ui.TextInput(
        label='New Textbox Image URL',
        placeholder='Paste new textbox image URL...',
        max_length=500,
        required=False
    )
    
    sprite_url = discord.ui.TextInput(
        label='New Sprite Image URL',
        placeholder='Paste new sprite image URL...',
        max_length=500,
        required=False
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        if self.character_name not in self.bot.textbox_data:
            await interaction.response.send_message("❌ Character not found!", ephemeral=True)
            return
            
        if self.bot.textbox_data[self.character_name]['user_id'] != interaction.user.id:
            await interaction.response.send_message("❌ Not your character!", ephemeral=True)
            return
        
        if self.textbox_url.value:
            self.bot.textbox_data[self.character_name]['textbox_url'] = self.textbox_url.value
        if self.sprite_url.value:
            self.bot.textbox_data[self.character_name]['sprite_url'] = self.sprite_url.value
            
        self.bot.save_data(self.bot.textbox_data)
        print(f'{Fore.GREEN}✅ Updated: {self.character_name}')
        await interaction.response.send_message(f"✅ Updated **{self.character_name}**!")

class Edit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="textboxedit", description="Edit a character's images")
    @app_commands.describe(name="Character name to edit")
    async def textboxedit(self, interaction: discord.Interaction, name: str):
        """Edit a character"""
        print(f'{Fore.YELLOW}🔄 Edit attempt by {interaction.user} for character: {name}')
        
        if name not in self.bot.textbox_data:
            await interaction.response.send_message("❌ Character not found!", ephemeral=True)
            return
            
        if self.bot.textbox_data[name]['user_id'] != interaction.user.id:
            await interaction.response.send_message("❌ Not your character!", ephemeral=True)
            return

        await interaction.response.send_modal(EditModal(self.bot, name))

async def setup(bot):
    await bot.add_cog(Edit(bot))