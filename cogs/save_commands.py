import discord
from discord.ext import commands
import datetime
import io
import chat_exporter

class save_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #chat html
    @commands.command()
    @commands.Cog.listener()
    async def save(self, ctx: commands.Context, tz_info: str = "CET", fancy_times: bool = False):
        await ctx.send("Getting history ready") #message
        date = str(datetime.date.today())

        #channel from ctx.channel is same datatype as ctx.guild.text_channels
        channel_list = [] #list for all channels

        #there will be an if statement at some point
        #for wether to only include spesific channel or all of them
        for channel in ctx.guild.text_channels:
            channel_list.append(channel)

        #generating chat
        for channel in channel_list:
            transcript = await chat_exporter.export(
                channel=channel,
                tz_info=tz_info,
                fancy_times=fancy_times,
                bot=self.bot
            )

            if transcript is None:
                return

             #generating file
            transcript_file = discord.File(
                io.BytesIO(transcript.encode()),
                filename=f"chat-history-{channel}_{date}.html"
            )

            await ctx.send(file=transcript_file)
            print("done")

async def setup(bot):
    await bot.add_cog(save_commands(bot))