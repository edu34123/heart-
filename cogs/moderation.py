import discord
from discord.ext import commands
import asyncio
import json

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Cancella un numero specificato di messaggi"""
        if amount > 100:
            await ctx.send("❌ Non puoi cancellare più di 100 messaggi alla volta!")
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🗑️ Cancellati {len(deleted) - 1} messaggi!", delete_after=5)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Nessuna ragione specificata"):
        """Espelli un membro dal server"""
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="👢 Membro Espulso",
                description=f"{member.mention} è stato espulso",
                color=discord.Color.orange()
            )
            embed.add_field(name="Ragione", value=reason)
            embed.add_field(name="Moderatore", value=ctx.author.mention)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Errore nell'espellere il membro: {e}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Nessuna ragione specificata"):
        """Banna un membro dal server"""
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="🔨 Membro Bannato",
                description=f"{member.mention} è stato bannato",
                color=discord.Color.red()
            )
            embed.add_field(name="Ragione", value=reason)
            embed.add_field(name="Moderatore", value=ctx.author.mention)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Errore nel bannare il membro: {e}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """Sbanna un membro"""
        banned_users = await ctx.guild.bans()
        
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name == member or str(user.id) == member:
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title="✅ Membro Sbannato",
                    description=f"{user.mention} è stato sbannato",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
                return
        
        await ctx.send("❌ Membro non trovato nella lista dei ban!")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
