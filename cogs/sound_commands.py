import discord
from discord.ext import commands
import asyncio
import sqlite3
from discord import FFmpegPCMAudio

database = "sounds.db"

conn = sqlite3.connect(database)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

class sound_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="sound", invoke_without_command=True, brief="Goofy sounds", description="A feature to play all your favorite sounds")
    async def sound(self, ctx: commands.Context):
        cur.execute("select * from sound")
        rows = cur.fetchall()

        message = await ctx.send("These are sounds")
        
        for row in rows:
            print(row["emoji"])
            try:
                await message.add_reaction(f"{row['emoji']}")
            except:
                continue

        #for playing audio file
        #https://www.youtube.com/watch?v=M_6_GbDc39Q
        #source = FFmpegPCMAudio("file")
        #player = voice.play(source)

async def setup(bot):
    await bot.add_cog(sound_commands(bot))