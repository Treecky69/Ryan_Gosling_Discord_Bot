from discord.ext import commands

class basic_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #says hello

    @commands.command(brief = "This is brief", description = "This is an example description")
    @commands.Cog.listener()
    async def hello(self, ctx):
        await ctx.send(f"Hi there {ctx.author.mention}")
    
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

async def setup(bot):
    await bot.add_cog(basic_commands(bot))