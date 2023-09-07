import discord
from discord.ext import commands
import os
import asyncio
import logging
import sys
from cogs.save_commands import save_commands

#since with the line bot.start(token) errors are no longer outputed
#i use this
#https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file/14058475#14058475
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

textfile = "info.txt"

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
        print(f"{bot.user} is now running")
        await save.run_times()

    #this needs some work
    #this is for error handling
    #https://stackoverflow.com/questions/42680781/handling-errors-with-the-discord-api-on-error
    #@bot.event
    #async def on_error(ctx: commands.Context):
    #    await ctx.send("Yo bitch, there is an error")
        #print(traceback.format_exc())

    asyncio.run(main())