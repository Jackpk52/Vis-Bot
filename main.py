import discord
from discord.ext import commands
import json
import os
from colorama import init, Fore, Style
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize colorama
init(autoreset=True)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

DATA_FILE = "textbox_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Global data storage
bot.textbox_data = load_data()
bot.save_data = save_data

@bot.event
async def on_ready():
    print(f'{Fore.GREEN}{Style.BRIGHT}🤖 {bot.user} is ready!')
    print(f'{Fore.CYAN}📊 Currently registered characters: {len(bot.textbox_data)}')
    
    try:
        synced = await bot.tree.sync()
        print(f'{Fore.GREEN}✅ Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'{Fore.RED}❌ Failed to sync commands: {e}')

# Load command cogs
async def load_cogs():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'commands.{filename[:-3]}')
            print(f'{Fore.GREEN}✅ Loaded: {filename}')

@bot.event
async def on_command_error(ctx, error):
    print(f'{Fore.RED}🚨 Command Error: {error}')

@bot.event
async def on_app_command_error(interaction, error):
    print(f'{Fore.RED}🚨 Slash Command Error: {error}')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    print(f'{Fore.CYAN}{Style.BRIGHT}🚀 Starting Sprite Bot...')
    import asyncio
    asyncio.run(main())