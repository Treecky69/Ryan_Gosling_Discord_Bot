import discord
from discord.ext import commands
import os
import asyncio
import logging
import sys
from cogs.save_commands import save_commands
import subprocess
import traceback
import sqlite3
from discord import FFmpegPCMAudio

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
    intents.reactions = True

    bot = commands.Bot(command_prefix="+", intents=intents)

    save = save_commands(bot)

    database = "sounds.db" #sound database

    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    #for when a reaction is added or removed
    async def reaction_func(reaction, user):
        bot_id = 1133714390512832512 #ryan's discord id
        ctx = reaction.message.channel
        soundFolder = os.getcwd() + "/sounds/" #getcwd for current dir

        #if the bot reacts, do nothing
        if user.bot:
            return

        #if there are reactions to messages not sent from the bot
        #ignore them
        if reaction.message.author.id != bot_id:
            return

        cur.execute("select * from sound where emoji = ?", [reaction.emoji])
        row = cur.fetchone()

        file = soundFolder + row["file"]

        if user.voice == None:
            await ctx.send("JOIN VC NIGGA")
        else:
            #for playing audio files
            #https://www.youtube.com/watch?v=M_6_GbDc39Q
            channel = user.voice.channel

            #bot's current voice channel
            vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)

            if vc is None:
                vc = await channel.connect()
            elif vc.channel != channel:
                await ctx.send("Hey fag, we aren't in the same channels. Use the join command we can be in the same channel and I can moan in your ear.")

            #playing the file
            source = FFmpegPCMAudio(file)
            player = vc.play(source)

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
        #global running

        #if not running:
            #running = True
        await ctx.send(f"{bot.user} is now running")
        await save.run_times()
        #else:
        #    await ctx.send(f"A new instance was shutdown")
        #    quit()

    @bot.event
    async def on_reaction_add(reaction, user):
        await reaction_func(reaction, user)

    @bot.event
    async def on_reaction_remove(reaction, user):
        await reaction_func(reaction, user)
        

    #https://stackoverflow.com/questions/42680781/handling-errors-with-the-discord-api-on-error
    @bot.event
    async def on_error(event):
        ctx = bot.get_channel(1161372535229796536) #error-channel channel
        await ctx.send("Yo bitch, there is an error")
        await ctx.send(traceback.format_exc())

    asyncio.run(main())