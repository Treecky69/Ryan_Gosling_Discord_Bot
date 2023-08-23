import discord
from discord.ext import commands
import random

class basic_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #says hello

    @commands.command(brief = "Just saying hello", description = "This is an example description")
    @commands.Cog.listener()
    async def hello(self, ctx):
        #URL endings of gifs
        giflist = ["ryan-gosling-gif-24496241", 
        "ryan-gosling-gif-24496239", 
        "drive-nightcall-film-ryan-gosling-gif-23819304", 
        "ryan-gosling-drive2011-ryan-gosling-drive-sigma-sigma-male-gif-23598924"]

        rand = random.randrange(0, len(giflist))
        await ctx.send(f"Hi there {ctx.author.mention}")
        await ctx.send(f"https://tenor.com/view/{giflist[rand]}")
    
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
        

    # @commands.command(brief = "Surprise ;)", description = "Enter the voice channel for a surpirse :)")
    # async def surprise(self, ctx):
    #     await ctx.send("!play https://www.youtube.com/watch?v=MV_3Dpw-BRY")

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

async def setup(bot):
    await bot.add_cog(basic_commands(bot))