### IMPORTTATION DES MODULES
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
import yt_dlp
import asyncio
load_dotenv()

##INITIALIASTION DU BOT


#Déclaration des variables

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
client = discord.Client(intents=intents)

MY_GUILD = discord.Object(id=os.getenv('SERV_ID'))

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}


#Déclaration des fonctions

@bot.event

async def on_ready():
    print(f"Connecté en tant que {bot.user.name}")
    try:
        syncro = await bot.tree.sync()
        print(f"Synchro locale réussie : {len(syncro)} commandes.")
    except Exception as error:
        print(f"Erreur de synchro: {error}")



@bot.tree.command(name="play_music", description="Joue la musique demandée")
@app_commands.describe(recherche="Le nom de la musique ou le lien YouTube")

async def play_music(interaction: discord.Interaction, recherche: str):
    if interaction.user.voice is None:
        return await interaction.response.send_message("Tu dois être dans un salon vocal pour ça !")
    await interaction.response.defer()

    channel = interaction.user.voice.channel
    if interaction.guild.voice_client is None:
        vc = await channel.connect()
    else:
        vc = interaction.guild.voice_client

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(recherche, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            url = info['url']
            titre = info['title']
        except Exception as e:
            return await interaction.followup.send(f"Erreur lors de la recherche : {e}")

    if vc.is_playing():
        vc.stop()

    source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
    vc.play(source)


    await interaction.followup.send(f"🎶 **{titre}** 🎶")


0##LANCEMENT DU BOT

bot.run(os.getenv('DISCORD_TOKEN'))