import discord
from discord.ext import commands
import asyncio
import sqlite3

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

        text = "These are the sounds:\n"
        
        for row in rows:
            text += f"- {row['emoji']}: {row['file']}\n"

        message = await ctx.send(text)
        
        for row in rows:
            try:
                await message.add_reaction(row['emoji'])
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