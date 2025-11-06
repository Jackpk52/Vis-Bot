import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            print(f'✅ Slash commands synced for {self.user}!')
        await self.close()

client = MyClient()
tree = app_commands.CommandTree(client)

@tree.command(name="textboxregister", description="Register a character with textbox and sprite")
async def textboxregister(interaction: discord.Interaction):
    await interaction.response.send_message("Use: /textboxregister to register a character")

@tree.command(name="textboxedit", description="Edit a character's images")
@app_commands.describe(name="Character name to edit")
async def textboxedit(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Editing {name}...")

@tree.command(name="textboxremove", description="Remove a character")
@app_commands.describe(name="Character name to remove")
async def textboxremove(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f"Removing {name}...")

@tree.command(name="say", description="Make a character speak")
@app_commands.describe(name="Character name", message="What they say")
async def say(interaction: discord.Interaction, name: str, message: str):
    await interaction.response.send_message(f"{name} says: {message}")

@tree.command(name="textboxlist", description="List all characters")
async def textboxlist(interaction: discord.Interaction):
    await interaction.response.send_message("Listing characters...")

if __name__ == "__main__":
    client.run(TOKEN)