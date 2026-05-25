### IMPORTTATION DES MODULES
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()

##INITIALIASTION DU BOT

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.tree.command(name="play_music", description="joue la musique demander par l'utilisateur")
async def play_music(interraction: discord.Interaction):
    await interraction.response.launch_activity()

##LANCEMENT DU BOT
bot.run(os.getenv('DISCORD_TOKEN'))