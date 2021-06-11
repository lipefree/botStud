import discord as disc

client = disc.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        print("Message received")
        await message.channel.send('Hello!')

    print('Message from {0.author}: {0.content}'.format(message))

client.run('ODUyMjg3OTU4MDA2NzU5NDU0.YMEpAw.ubIT1qL5RGPFhf1PpDGd8bsBp6k')
