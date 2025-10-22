# -------------------- Imports --------------------
import discord
from discord import app_commands # '/' commands
from discord.ext import commands # basic commands
import json # for data
from dotenv import load_dotenv # for token
import os

# -------------------- Load Token --------------------
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # Load token from .env

# -------------------- Intents --------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------- JSON Utilities --------------------
def load_data(load_profile=False):
    path = 'data/profiles.json' if load_profile else 'data/data.json' # toggle between loading data & profiles
    with open(path, 'r') as i:
        data = json.load(i)
    return data

def save_data(data, save_profile=False):
    path = 'data/profiles.json' if save_profile else 'data/data.json' # toggle between saving in data & profiles
    with open(path, 'w') as i:
        json.dump(data, i, indent=4)

user_data = load_data()
profile_data = load_data(load_profile=True)

# -------------------- Startup Event --------------------
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord')
    try:
        sync = await bot.tree.sync()
        print(f"synced {len(sync)} command(s)")
    except Exception as e: print(e)

# -------------------- Main Async Entry Point --------------------

async def main():
    async with bot:

        await bot.load_extension('cogs.test')
        await bot.load_extension('cogs.profile')

        await bot.start(TOKEN)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())


