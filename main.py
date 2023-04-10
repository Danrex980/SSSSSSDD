import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from music import Music

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=".", intents=intents)
bot.add_cog(Music(bot))


@bot.event
async def on_ready():
    print("Dev Online!")


@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'{amount} Nachrichten wurden gelöscht.', delete_after=5)


@bot.command(name='userinfo')
async def user_info(ctx, member: discord.Member):
    embed = discord.Embed(title="Userinfo", description=f"Informationen zu {member.mention}", color=0x00ff00)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Name", value=member.display_name, inline=True)
    embed.add_field(name="Erstellt am", value=member.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
    embed.add_field(name="Beigetreten am", value=member.joined_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)




load_dotenv()
bot.run(os.getenv('TOKEN'))
