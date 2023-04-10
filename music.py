import discord
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @commands.command()
        async def join(self, ctx):
            if ctx.author.voice is None:
                await ctx.send("Du bist nicht in einem Sprachkanal!")
            voice_channel = ctx.author.vocie.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)

        @commands.command()
        async def leave(self, ctx):
            await ctx.voice_client.disconnect()

        @commands.command()
        async def play(self, ctx, *, search):
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.send('Du bist nicht in einem Sprachkanal!')
                return
            voice_client = get(self.bot.voice_clients, guild=ctx.guild)

            if voice_client is None:
                await channel.connect()
                voice_client = get(self.bot.voice_clients, guild=ctx.guild)

            with YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True', 'default_search': 'ytsearch'}) as ydl:
                info = ydl.extract_info(f'ytsearch:{search}', download=False)['entries'][0]
                URL = info['formats'][0]['url']

            player = voice_client.play(discord.FFmpegPCMAudio(URL))
            await ctx.send(f"Wird gerade abgespielt: {info['title']}")

        @play.before_invoke
        async def ensure_voice(self, ctx):
            if ctx.voice_client is None:
                await ctx.invoke(self.join)


def setup(bot):
    bot.add_cog(Music(bot))
