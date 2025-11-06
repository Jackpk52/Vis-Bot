import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import io
import aiohttp
import textwrap
from colorama import Fore, Style

async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="say", description="Make a character speak")
    @app_commands.describe(name="Character name", message="What they say")
    async def say(self, interaction: discord.Interaction, name: str, message: str):
        """Make a character speak - sprite LEFT, textbox RIGHT"""
        print(f'{Fore.YELLOW}🔄 Say command by {interaction.user} for {name}: {message[:50]}...')
        
        if name not in self.bot.textbox_data:
            await interaction.response.send_message("❌ Character not found!", ephemeral=True)
            return

        char_data = self.bot.textbox_data[name]
        
        await interaction.response.defer()
        
        try:
            print(f'{Fore.BLUE}📥 Downloading images for {name}...')
            textbox_bytes = await download_image(char_data['textbox_url'])
            sprite_bytes = await download_image(char_data['sprite_url'])

            print(f'{Fore.BLUE}🎨 Creating composite image...')
            with Image.open(io.BytesIO(textbox_bytes)) as textbox_img:
                with Image.open(io.BytesIO(sprite_bytes)) as sprite_img:
                    textbox = textbox_img.convert('RGBA')
                    sprite = sprite_img.convert('RGBA')
                    
                    # Resize sprite (max height 400px)
                    sprite.thumbnail((400, 400), Image.Resampling.LANCZOS)
                    
                    # Create canvas: sprite width + textbox width
                    canvas_width = sprite.width + textbox.width
                    canvas_height = max(sprite.height, textbox.height)
                    
                    composite = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
                    
                    # Paste sprite on left
                    composite.paste(sprite, (0, 0), sprite)
                    
                    # Paste textbox on right
                    composite.paste(textbox, (sprite.width, 0), textbox)
                    
                    # Draw text on textbox
                    draw = ImageDraw.Draw(composite)
                    
                    try:
                        name_font = ImageFont.truetype("arial.ttf", 30)
                        text_font = ImageFont.truetype("arial.ttf", 24)
                    except:
                        name_font = ImageFont.load_default()
                        text_font = ImageFont.load_default()
                    
                    # Text position (on textbox area)
                    text_start_x = sprite.width + 20
                    name_y = 20
                    text_y = 60
                    
                    # Draw character name
                    draw.text((text_start_x, name_y), name, fill="white", font=name_font)
                    
                    # Draw wrapped message
                    for line in textwrap.wrap(message, width=30):
                        draw.text((text_start_x, text_y), line, fill="white", font=text_font)
                        text_y += 35
                    
                    output = io.BytesIO()
                    composite.save(output, format='PNG')
                    output.seek(0)
                    
                    file = discord.File(output, filename=f"{name}_says.png")
                    print(f'{Fore.GREEN}✅ Image created successfully for {name}')
                    await interaction.followup.send(file=file)
                    
        except Exception as e:
            print(f'{Fore.RED}❌ Error creating image: {str(e)}')
            await interaction.followup.send(f"❌ Error: {str(e)}")

async def setup(bot):
    await bot.add_cog(Say(bot))