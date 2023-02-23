import nextcord
from nextcord.ext import commands
import yt_dlp as youtube_dl


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.queue = []

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f"An unexpected error occurred: {str(error)}")

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("This is not a voice channel!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        ctx.voice_client.stop()

        YDL_OPTIONS = {'format': 'bestaudio/best', 'verbose': True}

        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
            source = await nextcord.FFmpegOpusAudio.from_probe(url2)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused!")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("Resumed!")

    @commands.command()
    async def queue(self, ctx, url):
        self.queue.append(url)
        await ctx.send(f"Added {url} to the queue.")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipping current song.")
        else:
            await ctx.send("No song is currently playing.")

    @commands.command()
    async def clear(self, ctx):
        self.queue.clear()
        await ctx.send("Cleared queue.")

    @commands.command()
    async def view(self, ctx):
        if not self.queue:
            await ctx.send("Queue is empty.")
            return
        queued_songs = "\n".join([
            f"{index + 1}. {song.title}" for index, song in enumerate(self.queue)
        ])
        await ctx.send(f"**Queue:**\n{queued_songs}")

    def setup(self, client):
        client.add_cog(self)
