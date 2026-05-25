### IMPORTTATION DES MODULES
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()

##INITIALIASTION DU BOT
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print("MODIBO est réveiller !!")
    print(f"Vous êtes connecter entant que: {client.user}")
    try:
        syncro = await bot.tree.sync()
        print(f"Commandes slash synchronisées: {len(syncro)}")
    except Exception as error:
        print(error)

@bot.tree.command(name="play_music", description="joue la musique demander par l'utilisateur")
async def play_music(interraction: discord.Interaction):
    await interraction.response.launch_activity()

0##LANCEMENT DU BOT
bot.run(os.getenv('DISCORD_TOKEN'))