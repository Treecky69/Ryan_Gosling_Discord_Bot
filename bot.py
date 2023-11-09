import discord
from discord.ext import commands
import os
import asyncio
import logging
import sys
from cogs.save_commands import save_commands
import subprocess
import traceback

#since with the line bot.start(token) errors are no longer outputed
#i use this
#https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file/14058475#14058475
root = logging.getLogger()
root.setLevel(logging.DEBUG)

#log to console
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

#log to file main.log
file = logging.FileHandler("main.log")
file.setLevel(logging.DEBUG)
file.setFormatter(formatter)

#adding them to the root logger
root.addHandler(handler)
root.addHandler(file)

textfile = "info.txt"
running = False #boolean wether there is already an instance running

with open(textfile) as f:
    lines = f.readlines()

for line in lines:
    if "token = " in line:
        var, token = line.split(" = ")
        token = token[:-1] #remove \n for newline
        break

def run_discord_bot():
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(command_prefix="+", intents=intents)

    save = save_commands(bot)

    #idk stole it from here
    #https://stackoverflow.com/questions/72732135/no-errors-outputing-after-i-started-using-cogs-in-discord-py-2-0
    async def load_extensions():
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                 await bot.load_extension(f"cogs.{filename[:-3]}")
                 print(f"{filename} loaded")

    async def main():
        async with bot:
            await load_extensions()
            await bot.start(token)

    #what is printed in the shell when turned on
    @bot.event
    async def on_ready():
        ctx = bot.get_channel(1161352691440693279) #start-alert channel
        global running

        if not running:
            running = True
            await ctx.send(f"{bot.user} is now running")
            await save.run_times()
        else:
            await ctx.send(f"A new instance was shutdown")
            quit()

    #https://stackoverflow.com/questions/42680781/handling-errors-with-the-discord-api-on-error
    @bot.event
    async def on_error(event):
        ctx = bot.get_channel(1161372535229796536) #error-channel channel
        await ctx.send("Yo bitch, there is an error")
        await ctx.send(traceback.format_exc())

    asyncio.run(main())