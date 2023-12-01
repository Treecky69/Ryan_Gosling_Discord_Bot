import discord
from discord.ext import commands
import asyncio
import sqlite3
import discord_emoji
import math

database = "sounds.db"

conn = sqlite3.connect(database)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

class sound_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Goofy sounds", description="A feature to play all your favorite sounds")
    async def sound(self, ctx: commands.Context):
        cur.execute("select * from sound")
        rows = cur.fetchall()
        reactLimit = 20 #how many reactions per message are allowed
        cur.execute("select count(*) from sound")
        count = cur.fetchone()["count(*)"] #get the number of rows

        await ctx.send("These are the sounds:")
        
        text = "" #list of emoji filename pairs
        msg_array = [] #an array of messages (for overcoming disocrd's 20 reactions per message limit)
        
        for i in range(count):
            row = rows[i]

            emoji = discord_emoji.to_unicode(row['emoji'])
            text += f"- {emoji}: {row['file']}\n"
            
            if i % reactLimit == (reactLimit - 1) or i == count - 1:
                msg_array.append(text)
                text = ""

        for i in range(count):
            row = rows[i]

            if i % reactLimit == 0:
                index = int(i / reactLimit) #index will be the result of division
                message = await ctx.send(msg_array[index]) 

            try:
                emoji = discord_emoji.to_unicode(row['emoji'])
                await message.add_reaction(emoji)
            except:
                continue

    @commands.command(brief="Join the VC", description="Tell the bot to join")
    async def join(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("JOIN A VC, NIGGA")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(brief="Disconnect from VC", description="Tell the bot to get tf out of the VC")
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(sound_commands(bot))