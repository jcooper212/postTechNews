import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
print("key ",os.getenv('DISCORD_PUB_KEY'))
client.run('7c885b8be68c85dc0d40e4f2ab87a9b08c604bfdfee5be11a406ebffbc6be861')
