from http.client import responses

from main import load_data
from main import save_data

import json
import discord
from discord import app_commands
from discord.ext import commands

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='profile', description='Shows character profile')  # name must be in lower case apparently
    async def profile(self, interaction: discord.Interaction):
        await interaction.response.send_message('Hello')

    @app_commands.command(name='register', description='Register your character')
    @app_commands.describe(first_initial='Your characters first initial, ex. J',
                           surname= 'Your characters surname ex. Doe',
                           nickname= 'Your characters nickname.',
                           bio= 'Your characters bio')
    async def register(self, interaction: discord.Interaction, first_initial: str, surname: str, bio: str = "n/a", nickname: str = 'n/a'):



async def setup(bot):
    await bot.add_cog(Profile(bot))