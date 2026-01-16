import discord
import requests
import asyncio
import os

# Récupéré depuis Render (variable d'environnement)
TOKEN = os.getenv("DISCORD_TOKEN")

# Adresse de ton serveur RedM
SERVER_URL = "http://game07.helloserv.fr:30006"

# Slots max
MAX_PLAYERS = 64

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def update_status():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            r = requests.get(f"{SERVER_URL}/players.json", timeout=5)
            players = r.json()
            count = len(players)

            activity = discord.Game(
                name=f"🎮 RedM | {count}/{MAX_PLAYERS} joueurs"
            )
            await client.change_presence(activity=activity)

        except Exception:
            await client.change_presence(
                activity=discord.Game(name="🔴 RedM hors ligne")
            )

        await asyncio.sleep(60)

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user}")

client.loop.create_task(update_status())
client.run(TOKEN)
