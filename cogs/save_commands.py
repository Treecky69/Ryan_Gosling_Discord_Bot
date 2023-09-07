import discord
from discord.ext import commands
from datetime import datetime
import io
import chat_exporter
from asyncio import sleep
from calendar import monthrange
import pytz
import sqlite3
from dropbox_funcs.dropbox_upload import dropbox_upload

database = "times.db"
timezone = pytz.timezone('Europe/Amsterdam')

conn = sqlite3.connect(database)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

class save_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def schedule(self, time_type: str, day: int, hour: int, minute: int, channel, cloud):
        if cloud == "cloud" or cloud == "Cloud":
            cloud = "yes"
        else:
            cloud = "no"

        #time_type is whether it repeats on a weekly or a monthly basis
        cur.execute("Insert into times(type, day, hour, minute, channel, cloud) values(?, ?, ?, ?, ?, ?)", (time_type, day, hour, minute, channel, cloud))
        conn.commit()

    async def run_times(self):
        while True:
            day_week = datetime.today().weekday() + 1
            day_month = datetime.now(timezone).day
            hour = datetime.now(timezone).hour
            minute = datetime.now().minute
            smallest_rem = 60 - minute #smallest number remaining minutes
            #until next scheduled time
            channel_list = []

            #boolean for if it is the right time to execute the save function
            #I could make it simpler but I dont want the function to repeat
            #a few hunder times a day if none of the scheduled times are today
            week_bool = {
                "day": False,
                "hour": False
            }

            month_bool = {
                "day": False,
                "hour": False
            }

            cur.execute("select * from times where type = 'week'")
            week_list = cur.fetchall()

            cur.execute("select * from times where type = 'month'")
            month_list = cur.fetchall()

            for row in week_list:
                print(f"Current time is {hour}:{minute}, scheduled time {row['hour']}:{row['minute']}")

                if day_week == row["day"]:
                    if hour == row["hour"]:
                        if minute == row["minute"]:
                            temp_array = {"channel": row["channel"], "cloud": row["cloud"]}
                            channel_list.append(temp_array)
                        else:
                            #if minute is false
                            week_bool["day"] = True
                            week_bool["hour"] = True

                            if row["minute"] > minute:
                                rem = row["minute"] - minute
                                if rem < smallest_rem:
                                    smallest_rem = rem

                    else:
                        #if hour is false
                        week_bool["day"] = True

            for row in month_list:
                print(f"Current time is {hour}:{minute}, scheduled time {row['hour']}:{row['minute']}")

                if day_month == row["day"]:
                    if hour == row["hour"]:
                        if minute == row["minute"]:
                            temp_array = {"channel": row["channel"], "cloud": row["cloud"]}
                            channel_list.append(temp_array)
                        else:
                            month_bool["day"] = True
                            month_bool["hour"] = True

                            if row["minute"] > minute:
                                rem = row["minute"] - minute
                                if rem < smallest_rem:
                                    smallest_rem = rem
                    else:
                        #if hour is false
                        month_bool["day"] = True

            for i in range(len(channel_list)):
                await self.save_func(channel_list[i]["channel"], channel_list[i]["cloud"])

            #all the new calls for minute and hour datetime
            #is so it can refresh the time after the save processes
            if week_bool["day"] or month_bool["day"]:
                if (week_bool["hour"] or month_bool["hour"]) and smallest_rem != None:
                    #here there is no if statement for minutes
                    #because if it comes to this block of code
                    #that means that not all 3 booleans are true

                    #changing the smallest_rem after the save process(it can sometimes take minutes)
                    print(f"This is smallest_rem before: {smallest_rem}")
                    smallest_rem -= (datetime.now().minute - minute)
                    print(f"This is smallest_rem: {smallest_rem}")
                    await sleep(smallest_rem * 60)
                else:
                    #remaining minute till next hour
                    rem_min = 60 - datetime.now().minute
                    print(f"This is rem_min if hour is false: {rem_min}")
                    await sleep(60 * rem_min)
            else:
                rem_hour = 24 - datetime.now(timezone).hour
                rem_min = 60 - datetime.now().minute
                if rem_min < 60:
                    rem_hour -= 1
                print(f"This is rem_min if day is false: {rem_hour}, {rem_min}")
                await sleep(rem_hour * 3600 + rem_min * 60)

    #where the file(s) is/are generated
    async def save_func(self, channel_id, cloud, onlythis = False, tz_info = "CET", fancy_times = False):
        ctx = self.bot.get_channel(channel_id)
        await ctx.send("Getting history ready") #message
        date = datetime.now(timezone) #getting date
        date_str = date.strftime("%Y.%m.%d-T%H%M")
        server = ctx.guild.name
        filelist = []

        #channel from ctx.channel is same datatype as ctx.guild.text_channels
        channel_list = [] #list for all channels

        if onlythis:
            channel_list.append(ctx)
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

            print(type(transcript))
            #array for the transcript file or for the dropbox func
            temp_array = {"channel": channel.name, "transcript": transcript}
            filelist.append(temp_array)
            #await ctx.send(transcript)

        if cloud == "yes":
            message = dropbox_upload(filelist, server, date_str)
            await ctx.send(message)
        else:
            for file in filelist:
                #generating file
                transcript_file = discord.File(
                    io.BytesIO(file["transcript"].encode()),
                    filename=f"chat-history-{server}-{file['channel']}-{date_str}.html"
                )
                await ctx.send(file=transcript_file)
                print("done")

    #chat html
    @commands.group(name="save", invoke_without_command=True, brief = "For archiving the current channel", description = "Group of subcommands used for archiving")
    @commands.Cog.listener()
    async def save(self, ctx: commands.Context):
        await self.save_func(ctx.channel.id, cloud = "no", onlythis = True)

    #save all channels, not just current
    @save.command(brief = "used to archive all the channels", description = "Sends all the archive files in current channel")
    async def all(self, ctx):
        await self.save_func(ctx.channel.id, cloud = "no")

    @save.command(brief = "Schedule a weekly save", description = "Format: +save week <weekday> <hour> <minute>")
    async def week(self, ctx, day: str = commands.parameter(default=None, description="week day (Monday - Sunday)"), hour: int = commands.parameter(default=12, description="Hour, this uses 24-hour format"), minute: int = 0, cloud: str = None):
        weekday_list = {
            "monday": 1,
            "tuesday": 2,
            "wednesday": 3,
            "thursday": 4,
            "friday": 5,
            "saturday": 6,
            "sunday": 7} #weekdays to numbers

        if day == None: 
            await ctx.send("Please provide an argument. For more info, type `+help`")
        elif day not in weekday_list or hour < 0 or hour > 23 or minute < 0 or minute > 59:
            await ctx.send("Not a valid argument. Pick a day between monday and sunday or check your time")
        else:
            day = weekday_list[day]
            await ctx.send("Got it boss. Scheduled a weekly save")
            self.schedule("week", day, hour, minute, ctx.channel.id, cloud)

    @save.command(brief = "schedule a monthly save", description = "Format: +save month <monthday> <hour> <minute>")
    async def month(self, ctx, day: int = commands.parameter(default=None, description="month day (1-31)"), hour: int = commands.parameter(default=12, description="Hour, this uses 24-hour format"), minute: int = 0, cloud: str = None):
        year = datetime.now(timezone).year
        month = datetime.now(timezone).month

        #number of days in the month
        #[1] is there because this gives 2 args
        #so im taking only the second which is the last day of the month
        num_days = monthrange(year, month)[1]

        if day == None: #no arg
            await ctx.send("Please provide an argument. For more info, type `+help`")
        elif day > 31 or day < 1 or hour < 0 or hour > 23 or minute < 0 or minute > 59: #more than 31
            await ctx.send("Not a valid argument. Pick a date between 1 and 31 or check your time")
        else:
            if day > num_days:
                day = num_days
                #await ctx.send(f"Today is day {day}")

            await ctx.send("Got it boss. Scheduled a monthly save")
            self.schedule("month", day, hour, minute, ctx.channel.id, cloud)

    @save.command(brief = "List times for this server", description = "List all the times that are scheduled for this server")
    async def list(self, ctx):
        message = ""

        cur.execute("Select * from times")
        rows = cur.fetchall()

        for row in rows:
            channel = self.bot.get_channel(row["channel"])
            server_id = channel.guild.id #server id of channel's server

            if server_id == ctx.guild.id:
                add_on = f'\n{row["id"]} {row["type"]} {row["day"]} {row["hour"]}:{row["minute"]} cloud: {row["cloud"]}'
                message += add_on
        
        if message == "":
            await ctx.send("No scheduled times in this server")
        else:
            await ctx.send(message)


    @save.command(brief = "Remove a scheduled entry", description = "Remove one entry that is shown in the list command\nFormat: +save remove <ID>")
    async def remove(self, ctx, ID: int = commands.parameter(default=None, description="ID that is used to remove the entry")):
        if ID == None:
            await ctx.send("No ID provided, please choose from one of the entries in the list command")
            return None
        
        cur.execute("select channel from times where id = ?", [ID])
        row = cur.fetchone()

        if row == None:
            await ctx.send("The ID you provided doesnt exist")
            return None

        server_id = self.bot.get_channel(row["channel"]).guild.id
        if server_id != ctx.guild.id:
            await ctx.send("This ID belongs to an entry not belonging to this server")
            return None

        cur.execute("delete from times where id = ?", [ID])
        conn.commit()

        await ctx.send("Time removed")

    @save.command(brief = "Change cloud status", description = "Remove one entry that is shown in the list command\nFormat: +save remove <ID>")
    async def cloud(self, ctx, ID: int = commands.parameter(default=None, description="ID that is used to remove the entry")):
        if ID == None:
            await ctx.send("No ID provided, please choose from one of the entries in the list command")
            return None
        
        cur.execute("select channel, cloud from times where id = ?", [ID])
        row = cur.fetchone()

        if row == None:
            await ctx.send("The ID you provided doesnt exist")
            return None

        server_id = self.bot.get_channel(row["channel"]).guild.id
        if server_id != ctx.guild.id:
            await ctx.send("This ID belongs to an entry not belonging to this server")
            return None

        #switches the option for cloud
        if row["cloud"] == "no":
            new_cloud = "yes"
        else:
            new_cloud = "no"

        cur.execute("update times set cloud = ? where id = ?", (new_cloud, ID))
        conn.commit()

        await ctx.send("Cloud status changed")


async def setup(bot):
    await bot.add_cog(save_commands(bot))