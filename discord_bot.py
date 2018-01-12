import os
import re
import libmarvin
import libmarvin.settingsloader as settings
import discord
import asyncio

from libmarvin.session import Session

client = discord.Client()

sessions = {}



def remove_self_mentions(content):
    return re.sub(r'<@\d+>', '', content)

def get_user_session(user):
    if not user in sessions:
        sessions[user] = Session()
    return sessions[user]

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):

    if client.user.id in message.raw_mentions:

        altered_content = remove_self_mentions(message.content)

        session = get_user_session(message.author.name)

        tmp = await client.send_message(message.channel, 'Processing...')
        result = session.query(author=message.author.name, line=altered_content)
        await client.edit_message(tmp, '{}'.format(result))

    elif message.content.startswith('!'):

        altered_content = re.sub(r'^!', '', message.content)

        session = get_user_session(message.author.name)

        tmp = await client.send_message(message.channel, 'Processing...')
        result = session.query(author=message.author.name, line=altered_content)
        await client.edit_message(tmp, '{}'.format(result))
    else:
        pass

client.run(os.environ['DISCORD_KEY'])