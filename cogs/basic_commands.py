import discord
from discord.ext import commands
import random
import yt_dlp
from asyncio import sleep

class basic_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #says hello

    @commands.command(brief = "Just saying hello", description = "This is an example description")
    @commands.Cog.listener()
    async def hello(self, ctx):
        gifFile = "gifList.txt" #ryan gosling gif list

        with open(gifFile) as f:
            giflist = f.readlines() #list of links for the gifs

        rand = random.randrange(0, len(giflist))

        await ctx.send(f"Hi there {ctx.author.mention}")
        await ctx.send(f"{giflist[rand]}")
    
    # @commands.command(brief = "This is brief test")
    # async def test(self, ctx, channel_name = None, server_name = None):
        # channel_id = ctx.channel.id
        # chnl = self.bot.get_channel(channel_id)
        # #await ctx.send(ctx.channel.id)
        # #await chnl.send("This is now the current channel")
        # #await chnl.send(chnl.guild.name)
        # message = ""

        # # for channel in chnl.guild.text_channels:
        # #     #if channel.name == "misc":
        # #     channel_id = channel.id
        # #     channel_name = channel.name
        # #     #await ctx.send("Found it")
        # #     await ctx.send(channel_name)
        # #     await ctx.send(channel_id)

        # for channel_id in channel_list:
        #     channel = self.bot.get_channel(channel_id)
        #     server_id = channel.guild.id
        #     if server_id == ctx.guild.id:
        #         add_on = f"\n{channel_id} {channel.name}"
        #         message += add_on

        # with open("info.txt") as f:
        #     lines = f.readlines()

        # for line in lines:
        #     if "token =" in line:
        #         var, token = line.split(" = ")
        #         print(var)
        #         token = token[:-1]
        #         print(token)

        #await ctx.send(message)
        

    @commands.command(brief = "Surprise ;)", description = "Enter the voice channel for a surpirse :)")
    async def surprise(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("JOIN A VC, NIGGA")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        url = "https://www.youtube.com/watch?v=MV_3Dpw-BRY"

        ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        ydl_options = {'format': 'bestaudio'}
        vc = ctx.voice_client

        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download = False)
            url2 = info['url']
            duration = info["duration"]
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
            vc.play(source)
            await sleep(duration)

        await vc.disconnect()

    @commands.command(brief="My introduction", description = "I introduce myself lmao")
    async def introduction(self, ctx):
        user = discord.utils.get(ctx.guild.members, name="_kalimero")
        for member in ctx.guild.members:
            if member.name == "_kalimero":
                user = member
                break
        else:
            return

        message = f"""For commands type '+help'

Hey guys, this is Ryan Gosling. After the Barbie success, I can finally afford a house in Gorno Dupeni. Big Skopje Sinkpissers Supporter

Sponsored by Viva. Природно, си е природно.

Profile pic by {user.mention}"""
        
        await ctx.send(message)

    @commands.command(brief="I answer question", description = "You ask questions and I answer them")
    async def answer(self, ctx):
        answerFile = "answerList.txt" #list of answers ryan can give

        with open(answerFile) as f:
            answerList = f.readlines() #list of answers

        rand = random.randrange(0, len(answerList))

        await ctx.send(f"{answerList[rand]}")

async def setup(bot):
    await bot.add_cog(basic_commands(bot))