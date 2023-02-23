import nextcord
from nextcord.ext import commands
from music import Music

intents = nextcord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

cogs = [Music(client)]
for cog in cogs:
    cog.setup(client)

token_file = "token.txt"

with open(token_file, "r") as token:
    discord_token = token.read().strip()

if not discord_token:
    raise ValueError("Discord token is empty in the token file.")

client.run(discord_token)
