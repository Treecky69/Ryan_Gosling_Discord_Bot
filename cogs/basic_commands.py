from discord.ext import commands

class basic_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #says hello

    @commands.command()
    @commands.Cog.listener()
    async def hello(self, ctx):
        await ctx.send("Hi there")
    
    @commands.command()
    async def test(self, ctx):
        for channel in ctx.guild.text_channels:
            print(channel)
        print(f"This is current: {ctx.channel}")
        #save(commands.Context.channel)

async def setup(bot):
    await bot.add_cog(basic_commands(bot))