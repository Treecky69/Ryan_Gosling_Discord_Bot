import discord
from discord.ext import commands
import chat_exporter
import io
import datetime

def run_discord_bot():
    token = "MTEzMzcxNDM5MDUxMjgzMjUxMg.G0fhSl.qa4OWiugWQgnEe5-0I8vVcShIznmzxHdzi_Xng"
    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True
    #client = discord.Client(intents=intents)

    bot = commands.Bot(command_prefix="+", intents=intents)

    #what is printed in the shell when turned on
    @bot.event
    async def on_ready():
        print(f"{bot.user} is now running")

    @bot.command()
    async def hello(ctx):
        await ctx.send("Hi there")

    @bot.command()
    async def save(ctx: commands.Context, tz_info: str = "CET", fancy_times: bool = False):
        await ctx.send("Getting history ready") #message
        date = str(datetime.date.today())

        print("Before transcript") #generating chat
        transcript = await chat_exporter.export(
            ctx.channel,
            tz_info=tz_info,
            fancy_times=fancy_times,
            bot=bot
        )

        print("Before if")
        if transcript is None:
            return

        print("Before file") #generating file
        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"chat-history-{ctx.channel}_{date}.html"
        )

        await ctx.send(file=transcript_file)
        print("done")

    bot.run(token)