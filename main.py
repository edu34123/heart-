import discord
from discord.ext import commands
import asyncio
import json
import os
from datetime import datetime

# Configurazione con variabili d'ambiente
token = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('PREFIX', '!')

if not token:
    print("❌ ERRORE: DISCORD_TOKEN non trovato!")
    exit(1)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} è online!')
    print(f'Connesso a {len(bot.guilds)} server')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{prefix}help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando non trovato!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Non hai i permessi necessari!")
    else:
        await ctx.send("❌ Si è verificato un errore!")
        print(f"Errore: {error}")

# Carica tutti i cog
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'✅ Caricato: {filename}')
            except Exception as e:
                print(f'❌ Errore nel caricare {filename}: {e}')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
