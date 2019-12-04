import discord
from discord.ext import commands
import time
import asyncio

class MyClient(discord.Client):
    async def on_ready(self):
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="porno"))
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content ==  '$neger wanus':
            await message.channel.send("wanus is gay and is the worst mid player ever")
        elif message.content.count('koekje') > 0:
            await message.channel.send("<:hondekoekje:615167466259087370>")
        elif message.content == '$neger hallo':
            await message.channel.send('jij bent @{0.author}'.format(message))
        elif message.content.startswith('$neger'):
            await message.channel.send("wannes is een kutmongool")

        forbidden_words = [ "stront", 'racist' ]
        for word in forbidden_words:
            if message.content.count(word) > 0:
                await message.channel.purge(limit=1)
                await message.channel.send("{0.author} is een grote stront".format(message))

        print('Message from {0.author}: {0.content}'.format(message))
    
    async def on_member_join(self, member):
        for channel in member.guild.channels:
            if channel == 'pandabeer':
                await channel.sendmessage(f"""league suckt speel dota { member.mention }""")


client = MyClient()
client.run('NjM0NDYyNDMwMjUxOTc0NjU3.Xai3uA.wglHP9yyWHJEM4d-Y2OjjWPRc9k')