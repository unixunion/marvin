import os
import re
import libmarvin
import libmarvin.settingsloader as settings
import discord
import asyncio
import logging

from libmarvin.cache import Cache
from libmarvin.session import Session

client = discord.Client()

sessions = {}

Cache.set("discord_api", client)

def remove_self_mentions(content):
    logging.info("remove_self_mentions from: %s" % content)
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

    logging.info(message.content)

    msg = message # type: discord.Channel


    if client.user.id in message.raw_mentions:

        altered_content = remove_self_mentions(message.content)

        session = get_user_session(message.author.name)

        tmp = await client.send_message(message.channel, 'Processing...')

        result = await session.query(author=message.author.name, line=altered_content, message_object=message)
        await client.edit_message(tmp, '{}'.format(result))

    elif message.content.startswith('!'):

        altered_content = re.sub(r'^!', '', message.content)

        session = get_user_session(message.author.name)

        tmp = await client.send_message(message.channel, 'Processing...')
        result = await session.query(author=message.author.name, line=altered_content, message_object=message)
        await client.edit_message(tmp, '{}'.format(result))
    else:
        pass

client.run(os.environ['DISCORD_KEY'])