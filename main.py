import discord
from discord.ext import commands
import asyncio
import os
from aiohttp import web
import threading

# Configurazione
token = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('PREFIX', '/')
port = int(os.getenv('PORT', 10000))

if not token:
    print("❌ ERRORE: DISCORD_TOKEN non trovato!")
    exit(1)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

# Web server per Render
async def health_check(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Web server avviato sulla porta {port}")

@bot.event
async def on_ready():
    print(f'✅ {bot.user} è online!')
    print(f'📊 Connesso a {len(bot.guilds)} server')
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
    # Avvia il web server in background
    asyncio.create_task(start_web_server())
    
    # Carica i cog e avvia il bot
    async with bot:
        await load_cogs()
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
