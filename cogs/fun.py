import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, message):
        """Ripete il messaggio dell'utente"""
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """Mostra l'avatar di un utente"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"🖼️ Avatar di {member.display_name}",
            color=member.color
        )
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def poll(self, ctx, *, question):
        """Crea un sondaggio semplice"""
        embed = discord.Embed(
            title="📊 Sondaggio",
            description=question,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Sondaggio creato da {ctx.author}")
        
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

    @commands.command()
    async def dice(self, ctx, sides: int = 6):
        """Lancia un dado"""
        if sides < 2:
            await ctx.send("❌ Il dado deve avere almeno 2 facce!")
            return
        
        result = random.randint(1, sides)
        await ctx.send(f"🎲 {ctx.author.mention} ha lanciato un dado a {sides} facce: **{result}**")

    @commands.command()
    async def choose(self, ctx, *, options):
        """Sceglie tra diverse opzioni"""
        options_list = options.split(",")
        if len(options_list) < 2:
            await ctx.send("❌ Fornisci almeno 2 opzioni separate da virgola!")
            return
        
        choice = random.choice(options_list).strip()
        await ctx.send(f"🎯 Scelgo: **{choice}**")

async def setup(bot):
    await bot.add_cog(Fun(bot))
