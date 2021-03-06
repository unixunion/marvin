import os
import sys

import logging
logging.basicConfig(stream=sys.stdout ,format='[%(filename)s:%(lineno)s %(levelname)s %(message)s')
logging.getLogger().setLevel(logging.INFO)

import re
import libmarvin
import libmarvin.settingsloader as settings
import discord
import asyncio

from libmarvin.cache import Cache
from libmarvin.session import Session

client = discord.Client()

sessions = {}

Cache.set("discord_api", client)

min_confidence = 0.45


def remove_self_mentions(content):
    logging.info("remove_self_mentions from: %s" % content)
    return re.sub(r'<@%s>' % client.user.id, '', content).strip()


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

    #msg = message # type: discord.Channel

    if message.channel.is_private and message.author.id != client.user.id:
        altered_content = remove_self_mentions(message.content)
        session = get_user_session(message.author.name)
        result = await session.query(author=message.author.name, line=altered_content, message_object=message)
        await client.send_message(message.channel, result[0])

    elif client.user.id in message.raw_mentions:
        altered_content = remove_self_mentions(message.content)
        session = get_user_session(message.author.name)
        result = await session.query(author=message.author.name, line=altered_content, message_object=message)
        await client.send_message(message.channel, result[0])

    elif message.content.startswith('!dump_msgs'):
        tmp = await client.send_message(message.channel, 'Dumping messages to log')
        async for log in client.logs_from(message.channel, limit=65534):
            logging.info("discord_dump_msg: %s" % log.content)
        await client.edit_message(tmp, 'Done.')

    elif message.content.startswith('!'):
        altered_content = re.sub(r'^!', '', message.content)
        session = get_user_session(message.author.name)
        result = await session.query(author=message.author.name, line=altered_content, message_object=message)
        await client.send_message(message.channel, result[0])

    # elif message.author.id is not client.user.id:
    #     # tmp = await client.send_message(message.channel, 'Processing...')
    #     altered_content = re.sub(r'^!', '', message.content)
    #     session = get_user_session(message.author.name)
    #     result = await session.query(author=message.author.name, line=altered_content, message_object=message)
    #     # await client.edit_message(tmp, '{}'.format(result))
    #     if result[1] > min_confidence:
    #         await client.send_message(message.channel, result[0])
    elif message.author.id != client.user.id:
        logging.info("message %s author: %s" % (message.content, message.author.name))
        pass
    else:
        logging.info("ignoring message from myself")
        pass


client.run(os.environ['DISCORD_KEY'])
