import discord
import responses

async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        #print(f"This is the response variable {response}")
        await message.channel.send(response)
    except Exception as e:
        print(f"This is an exception {e}")

def run_discord_bot():
    token = "MTEzMzcxNDM5MDUxMjgzMjUxMg.G0fhSl.qa4OWiugWQgnEe5-0I8vVcShIznmzxHdzi_Xng"
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: {user_message}" ({channel})')

        if user_message[0] == "?":
            user_message = user_message[1:]
            #print(f"MESSAGE RECIEVED: {user_message}")
            await send_message(message, user_message)

    client.run(token)