import re

import discord
from discord import ChannelType

from libmarvin import Plugin
import libmarvin
import logging
import asyncio

from libmarvin.cache import Cache
from libmarvin.util import get_key_from_kwargs

@libmarvin.plugin_registry.register
class DiscordPlugin(Plugin):
    plugin_name = "discordplugin"
    args = None
    kwargs = None
    api = None

    @staticmethod
    def required_kwargs():
        return "{'api'}"

    def __init__(self, *args, api=None, **kwargs):
    # def __init__(self, api : discord.Client):
        logging.info("instantiating %s, args: %s, kwargs: %s" % (self, args, kwargs))
        self.args = args
        self.kwargs = kwargs
        self.api = Cache.get("discord_api") # type: discord.Client

    # default method to call if no double underscored method mentioned in intent name
    def default(self, *args, **kwargs):
        return "%s: unknown intent, check training" % self.plugin_name

    def help(self, *args, **kwargs):
        return "%s: manage discord stuff" % self.plugin_name


    """
    Helpers
    """

    def get_channel_by_name(self, message, channel_name):
        channel = discord.utils.get(message.server.channels, name=channel_name, type=ChannelType.voice) # type: discord.Channel
        logging.info("Found channel: %s" % channel.type)
        return channel

    def get_user_by_id(self, message, user_id):
        member = discord.utils.get(message.server.members, id=user_id)
        return member

    def get_member(self, **kwargs):
        logging.info("getting member for kwargs: %s" % kwargs)
        message_object = get_key_from_kwargs('message_object', kwargs)  # type: discord.Message
        user_id = get_key_from_kwargs('user', kwargs, get_key_from_kwargs('message_object', kwargs).author.id)
        user_id = re.sub(r'<@(\d+)\>', '\\1', user_id)
        member = discord.utils.get(message_object.server.members, id=user_id)
        logging.info("got member: %s" % member)
        return member

    """
    Do things to / in channels
    """
    async def channel(self, *args, **kwargs):
        logging.info("about this channel they say: %s, %s" % (args, kwargs))
        message_object = get_key_from_kwargs('message_object', kwargs)  # type: discord.Message
        channel = message_object.channel # type:discord.Channel

        if channel.is_private:
            return "This is a private channel, just between us, feel free to say anything. Nothing is logged"

        rename = get_key_from_kwargs("rename", kwargs, None, is_optional=True)
        if rename:
            await self.api.edit_channel(channel, name=rename)

        retopic = get_key_from_kwargs("retopic", kwargs, None, is_optional=True)
        if retopic:
            await self.api.edit_channel(channel, topic=retopic)

        return "This channel is called: '%s', and the topic is: '%s'" % (channel.name, channel.topic)


    async def deafen(self, *args, **kwargs):
        message_object = get_key_from_kwargs('message_object', kwargs)  # type: discord.Message
        member = self.get_member(**kwargs)
        await self.api.server_voice_state(member, deafen=True)
        return "%s: told me to deafen %s" % (message_object.author.name, member.name)

    async def undeafen(self, *args, **kwargs):
        message_object = get_key_from_kwargs('message_object', kwargs)  # type: discord.Message
        member = self.get_member(**kwargs)
        await self.api.server_voice_state(member, deafen=False)
        return "%s: told me to undeafen %s" % (message_object.author.name, member.name)

    async def mute(self, *args, **kwargs):
        message_object = get_key_from_kwargs('message_object', kwargs)  # type: discord.Message
        member = self.get_member(**kwargs)
        await self.api.server_voice_state(member, mute=True)
        return "%s: told me to mute %s" % (message_object.author.name, member.name)

    async def unmute(self, *args, **kwargs):
        message_object = get_key_from_kwargs('message_object', kwargs)  # type: discord.Message
        member = self.get_member(**kwargs)
        await self.api.server_voice_state(member, mute=False)
        return "%s: told me to unmute %s" % (message_object.author.name, member.name)

    async def afk(self, *args, **kwargs):
        logging.info("afk somebody they say: %s, %s" % (args, kwargs))

        message_object = get_key_from_kwargs('message_object', kwargs) # type: discord.Message

        try:
            # try get user is passed, else default back to the author
            user_id =  get_key_from_kwargs('user', kwargs, get_key_from_kwargs('message_object', kwargs).author.id )

            user_id = re.sub(r'<@(\d+)\>', '\\1', user_id)

            member = self.get_user_by_id(message_object, user_id)
            logging.info("member move for: %s " % member)

            # get target channel
            default_channel_name = "Afk"
            # default_channel = get_key_from_kwargs('message_object', kwargs).server.get_channel(default_channel_name) # type:discord.Channel

            # see if channel kwarg specified
            channel_name = get_key_from_kwargs('channel', kwargs, default_channel_name ) # type: discord.Channel

            # channel = get_key_from_kwargs('message_object', kwargs).server.get_channel(channel_name) # type:discord.Channel

            channel = self.get_channel_by_name(message_object, channel_name)

            logging.info("moving %s to %s" % (member, channel))
            logging.info("moving id: %s to name:%s" % (member.name, getattr(channel, 'type')))
            logging.info("moving %s to %s" % (type(member), type(channel)))
            # channel_obj = self.api.get_channel(channel)

            # self.api.get_user_info(used_id)

            await self.api.move_member(member, channel)
            return "moved %s to %s" % (member.name, channel.name)

            # return result

        except Exception as e:
            logging.error("error moving member: %s" % e)
            return "%s: I'm afraid I can't do that Dave..." % self.plugin_name

