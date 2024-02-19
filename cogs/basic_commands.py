import discord
from discord.ext import commands
import random
import yt_dlp
from asyncio import sleep
import aiohttp

class basic_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #says hello

    @commands.command(brief = "Just saying hello", description = "This is an example description")
    #@commands.Cog.listener()
    async def hello(self, ctx):
        gifFile = "gifList.txt" #ryan gosling gif list

        with open(gifFile) as f:
            giflist = f.readlines() #list of links for the gifs

        rand = random.randrange(0, len(giflist))

        await ctx.send(f"Hi there {ctx.author.mention}")
        await ctx.send(f"{giflist[rand]}")
    
    # @commands.command(brief = "This is brief test")
    # async def test(self, ctx, channel_name = None, server_name = None):
    #     await ctx.send("Counting your shit")

    #     counter = 0 # overall sum
    #     users = {} #each user number messages
    #     channels = {} #each channel number messages

    #     for channel in ctx.guild.text_channels:
    #         async for message in channel.history(limit=9999):
    #             if message.author.name not in users.keys(): #if user not part of dictionary
    #                 users[message.author.name] = 1
    #             else:
    #                 users[message.author.name] += 1

    #             #change this for channels
    #             if channel.name not in channels.keys(): #if user not part of dictionary
    #                 channels[channel.name] = 1
    #             else:
    #                 channels[channel.name] += 1

    #             counter += 1
        
    #     #for sorting dictionaries by values and then keys
    #     #stole it from here: https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
    #     users = sorted(users.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    #     channels = sorted(channels.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    #     for user in users:
    #         await ctx.send(f"{user[0]}: {user[1]}")
    #     for channel in channels:
    #         await ctx.send(f"{channel[0]}: {channel[1]}")
    #     await ctx.send(counter)

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

    @commands.command(brief="Count how many messages have been sent", description = "The total amount of messages sent, plus each user and channel")
    async def count(self, ctx):
        await ctx.send("Counting your shit")

        message = ""

        total = 0 # overall sum
        users = {} #each user number messages
        channels = {} #each channel number messages

        for channel in ctx.guild.text_channels:
            async for message in channel.history(limit=99999):
                if message.author.name not in users.keys(): #if user not part of dictionary
                    users[message.author.name] = 1
                else:
                    users[message.author.name] += 1

                #change this for channels
                if channel.name not in channels.keys(): #if user not part of dictionary
                    channels[channel.name] = 1
                else:
                    channels[channel.name] += 1

                total += 1
        
        #for sorting dictionaries by values and then keys
        #stole it from here: https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
        users = sorted(users.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        channels = sorted(channels.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)


        await ctx.send("Here are the results\n")
        
        message = "Users:\n" #message that will be sent for the users table
        for user in users:
            message += f"{user[0]}: {user[1]}\n"
        
        await ctx.send(message) #send users table

        message = "Channels:\n" #message that will be sent for the channels table
        for channel in channels:
            message += f"{channel[0]}: {channel[1]}\n"
        
        await ctx.send(message) #send channels table

        await ctx.send(f"Total: {total}")

async def setup(bot):
    await bot.add_cog(basic_commands(bot))