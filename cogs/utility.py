import discord
from discord.ext import commands
import datetime
import platform

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """Mostra tutti i comandi disponibili"""
        embed = discord.Embed(
            title="📚 Lista Comandi",
            description="Ecco tutti i comandi disponibili:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🛠️ Moderazione",
            value="`clear` `kick` `ban` `unban`",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Utility",
            value="`help` `userinfo` `serverinfo` `ping` `botinfo`",
            inline=False
        )
        
        embed.add_field(
            name="🎉 Divertimento",
            value="`say` `avatar` `poll`",
            inline=False
        )
        
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        """Mostra informazioni su un utente"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"👤 Informazioni su {member.display_name}",
            color=member.color
        )
        embed.set_thumbnail(url=member.avatar.url)
        
        embed.add_field(name="Nome", value=member.name, inline=True)
        embed.add_field(name="Discriminator", value=member.discriminator, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        
        embed.add_field(
            name="Account creato", 
            value=member.created_at.strftime("%d/%m/%Y %H:%M"), 
            inline=True
        )
        embed.add_field(
            name="Entrato nel server", 
            value=member.joined_at.strftime("%d/%m/%Y %H:%M"), 
            inline=True
        )
        
        embed.add_field(
            name="Ruoli", 
            value=", ".join([role.mention for role in member.roles[1:]]), 
            inline=False
        )
        
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        """Mostra informazioni sul server"""
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f"🏠 Informazioni Server: {guild.name}",
            color=discord.Color.gold()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.add_field(name="Proprietario", value=guild.owner.mention, inline=True)
        embed.add_field(name="ID Server", value=guild.id, inline=True)
        embed.add_field(name="Membri", value=guild.member_count, inline=True)
        
        embed.add_field(
            name="Creato il", 
            value=guild.created_at.strftime("%d/%m/%Y %H:%M"), 
            inline=True
        )
        embed.add_field(name="Ruoli", value=len(guild.roles), inline=True)
        embed.add_field(name="Canali", value=len(guild.channels), inline=True)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Mostra il ping del bot"""
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latenza: {round(self.bot.latency * 1000)}ms",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        """Mostra informazioni sul bot"""
        embed = discord.Embed(
            title="🤖 Informazioni Bot",
            color=discord.Color.purple()
        )
        
        embed.add_field(name="Nome", value=self.bot.user.name, inline=True)
        embed.add_field(name="ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        embed.add_field(name="Python", value=platform.python_version(), inline=True)
        embed.add_field(name="discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="Server", value=len(self.bot.guilds), inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
