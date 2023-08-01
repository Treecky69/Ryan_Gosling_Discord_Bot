import discord
from discord.ext import commands
from datetime import datetime
import io
import chat_exporter
from asyncio import sleep
from calendar import monthrange

class save_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def save_func(self, ctx, onlythis = False, tz_info = "CET", fancy_times = False):
        await ctx.send(f"{ctx.author.mention} Getting history ready") #message
        date = datetime.now() #getting date
        date_str = date.strftime("%Y.%m.%d-T%H%M")

        #channel from ctx.channel is same datatype as ctx.guild.text_channels
        channel_list = [] #list for all channels

        if onlythis:
            channel_list.append(ctx.channel)
        else:
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
                filename=f"chat-history-{channel}-{date_str}.html"
            )

            await ctx.send(file=transcript_file)
            print("done")

    #chat html
    @commands.group(name="save", invoke_without_command=True)
    @commands.Cog.listener()
    async def save(self, ctx: commands.Context):

        await self.save_func(ctx, onlythis = True)

    @save.command()
    async def week(self, ctx, day: str = None, time: str = None, onlythis: bool = False):
        weekday_list = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day = day.lower()

        if day == None: 
            await ctx.send("Please provide an argument. For more info, type `+help`")
        elif day not in weekday_list:
            await ctx.send("Not a valid argument. Pick a day between monday and sunday")
        else:
            #await sleep(10) #this is sleep from asyncio
            await ctx.send(f"This is the weekly save command with arg {day}")
            await self.save_func(ctx, onlythis)

    @save.command()
    async def month(self, ctx, day: int = None, onlythis: bool = False):
        year = datetime.now().year
        month = datetime.now().month

        #number of days in the month
        #[1] is there because this gives 2 args
        #so im taking only the second which is the last day of the month
        num_days = monthrange(year, month)[1]

        if day == None: #no arg
            await ctx.send("Please provide an argument. For more info, type `+help`")
        elif day > 31: #more than 31
            await ctx.send("Not a valid argument. Pick a date between 1 and 31")
        else:
            if day > num_days:
                day = num_days
                await ctx.send(f"Today is day {day}")
            #await sleep(10) #this is sleep from asyncio
            await ctx.send(f"This is the month save command with argument {day}")
            await self.save_func(ctx, onlythis)

async def setup(bot):
    await bot.add_cog(save_commands(bot))