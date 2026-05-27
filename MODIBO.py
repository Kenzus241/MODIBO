### IMPORTTATION DES MODULES
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
import yt_dlp
from discord.ext import tasks
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
    'ignoreerrors': True,
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

inactivity_counts = {}

queues = {}

#Déclaration des fonctions

@tasks.loop(minutes=1)

async def check_inactivity():
    '''
    la fonction qui vérifie l'inactivité du bot
    '''
    for guild in bot.guilds:
        vc = guild.voice_client

        if vc:
            if not vc.is_playing() and not vc.is_paused():
                inactivity_counts[guild.id] = inactivity_counts.get(guild.id, 0) + 1

                if inactivity_counts[guild.id] >= 6:
                    await vc.disconnect()
                    print(f"Déconnection pour inactivité {guild.name}")
                    inactivity_counts[guild.id] = 0
            else:
                inactivity_counts[guild.id] = 0

@bot.event

async def on_ready():
    '''
    la fonction qui initialise le lancement du bot
    '''
    print(f"Connecté en tant que {bot.user.name}")

    if not check_inactivity.is_running():
        check_inactivity.start()

    try:
        syncro = await bot.tree.sync()
        print(f"Synchro locale réussie : {len(syncro)} commandes.")
    except Exception as error:
        print(f"Erreur de synchro: {error}")



@bot.tree.command(name="play_music", description="Joue la musique demandée")
@app_commands.describe(recherche="Le nom de la musique ou le lien YouTube")

async def play_music(interaction: discord.Interaction, recherche: str):
    '''
    la fonction principal qui lance la recherche et initialise le lancement de la musique
        @interaction: permet l'interaction avec l'utilisateur
        @recherche: la recherche éffectuer par l'utilisateur
    '''
    if interaction.user.voice is None:
        return await interaction.response.send_message("Tu dois être dans un salon vocal pour ça !")
    await interaction.response.defer()

    channel = interaction.user.voice.channel
    if interaction.guild.voice_client is None:
        vc = await channel.connect()
    else:
        vc = interaction.guild.voice_client

    recherche_amelioree = f"ytsearch5:{recherche} audio"

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(recherche_amelioree, download=False)
            
            if 'entries' in info:
                video_choisie = None
                
                for entry in info['entries']:
                    if entry is None:
                        continue
                    est_musique = entry.get('categories') and 'Music' in entry['categories']
                    duree_valide = entry.get('duration') and entry['duration'] < 600
                    
                    if est_musique and duree_valide:
                        video_choisie = entry
                        break

                if not video_choisie:
                    for entry in info['entries']:
                        if entry is not None and entry.get('duration', 0) < 600:
                            video_choisie = entry
                            break

            url = video_choisie['url']
            titre = video_choisie['title']

        except Exception as e:
            return await interaction.followup.send(f"Erreur lors de la recherche : {e}")

    if vc.is_playing():
        vc.stop()

    audio_source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
 
    source = discord.PCMVolumeTransformer(audio_source, volume=0.5)
    source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
    vc.play(source)


    await interaction.followup.send(f"🎶 **{titre} \nduration: {info['entries'][0].get('duration', 0) / 60: .2f} min** 🎶")


0##LANCEMENT DU BOT

bot.run(os.getenv('DISCORD_TOKEN'))