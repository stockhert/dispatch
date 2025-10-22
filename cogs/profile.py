from http.client import responses
import datetime

from main import load_data, user_data
from main import save_data

import json
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View

# ---------------------------------------- Confirmation View ----------------------------------------
class ConfirmDeleteView(discord.ui.View):
    def __init__(self, user_id: str):
        super().__init__(timeout=30.0)
        self.user_id = user_id
        self.value = None

    # confirmation -> yes button
    @discord.ui.button(label="Yes, Delete", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

        try:
            profiles = load_data(load_profile=True)
            if self.user_id in profiles:
                del profiles[self.user_id]
                save_data(profiles, save_profile=True)
                print(f"[{datetime.datetime.now()}]: Profile deleted for {interaction.user.name}.")
                await interaction.response.edit_message(content="Profile deleted. Run /register to create a new one.", view=None)
            else:
                await interaction.response.edit_message("I can't find your profile..", view=None)

        except Exception as e:
            await interaction.response.edit_message(content="Error deleting profile, catch n release ! ! ! ", view=None)
            print(e)

    # confirmation -> no button
    @discord.ui.button(label="No, Cancel", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Profile deletion cancelled.", view=None)
        self.value = False
        self.stop()

    # timeout catch
    async def on_timeout(self):
        #kills itself after timeout (30s default)
        self.stop()

# ---------------------------------------- Cog Class ----------------------------------------
class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------- profile --------------------
    @app_commands.command(name='profile', description='Shows character profile')  # name must be in lower case apparently
    async def profile(self, interaction: discord.Interaction):
        await interaction.response.send_message('Hello')

    # -------------------- register --------------------
    @app_commands.command(name='register', description='Register your character')
    @app_commands.describe(first_initial='Your characters first initial, ex. J',
                           surname= 'Your characters surname ex. Doe',
                           nickname= 'Your characters nickname.',
                           bio= 'Your characters bio')
    async def register(self, interaction: discord.Interaction, first_initial: str, surname: str, bio: str = "n/a", nickname: str = 'n/a'):
        user_id = str(interaction.user.id)
        profiles = load_data(load_profile=True)

        # validate inputs
        if user_id in profiles:
            view = ConfirmDeleteView(user_id)
            await interaction.response.send_message(
                "😭 You already have a profile.. do you want to delete it??",
                view=view,
                ephemeral=True,
            )

            return
        elif len(first_initial) > 1:
            await interaction.response.send_message("Your first initial is too long.. must be 1 character..", ephemeral=True)
            return
        elif not first_initial.isalpha():
            await interaction.response.send_message("Your first initial must be a letter..", ephemeral=True)
            return
        elif len(surname) > 50:
            await interaction.response.send_message("Your surname is too long.. must be 50 characters or less..", ephemeral=True)
            return

        # save profile to profiles.json
        profiles[user_id] = {
            'first_initial': first_initial,
            'surname': surname,
            'bio': bio,
            'nickname': nickname
        }

        try:
            save_data(profiles, save_profile=True)
            print(f"[{datetime.datetime.now()}]: Profile created for {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message("❌ Error saving profile. @<1074357639892455505> (you fucked up the code).")
            return

        # send confirmation message (NOT ephemeral needs testing!!)
        def generate_name():
            if nickname != 'n/a':
                return f'{first_initial}. "{nickname}" {surname}'
            else:
                return f'{first_initial}. {surname}'

        await interaction.response.send_message(
            f"You have registered as {generate_name()}"
        )
    # -------------------- deleteprofile --------------------
    @app_commands.command(name='deleteprofile', description='Delete your character profile')
    async def deleteprofile(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        profiles = load_data(load_profile=True)

        if user_id in profiles:
            view = ConfirmDeleteView(user_id)
            await interaction.response.send_message(
                "Are you sure you want to delete your profile?",
                view=view,
                ephemeral=True,
            )




async def setup(bot):
    await bot.add_cog(Profile(bot)) 