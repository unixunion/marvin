import discord

from libmarvin import Plugin
import libmarvin
import logging
import asyncio

from libmarvin.cache import Cache
from libmarvin.util import get_key_from_kwargs
# from discord_bot import get_client

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
        logging.info("instantiating %s, args: %s, kwargs: %s" % (self, args, kwargs))
        self.args = args
        self.kwargs = kwargs
        # self.api = get_key_from_kwargs("api", kwargs) # type: discord.Client
        self.api = Cache.get("discord_api")

    # default method to call if no double underscored method mentioned in intent name
    def default(self, *args, **kwargs):
        return "%s: unknown intent, check training" % self.plugin_name

    def help(self, *args, **kwargs):
        return "%s: manage discord stuff" % self.plugin_name

    async def afk(self, *args, **kwargs):
        logging.info("afk somebody they say")

        try:
            member = get_key_from_kwargs('member', kwargs, get_key_from_kwargs('message_object', kwargs).author ) # type: discord.Member
            logging.info("member move: %s " % member)
            channel = get_key_from_kwargs('channel', kwargs, get_key_from_kwargs('message_object', kwargs).server.afk_channel ) # type: discord.Channel
            logging.info("moving %s to %s" % (member, channel))
            logging.info("moving %s to %s" % (type(member), type(channel)))
            channel_obj = self.api.get_channel(channel)
            result = await self.api.move_member(member, channel_obj)
            return "Done: %s" % result

            # return result

        except Exception as e:
            logging.error("error moving member: %s" % e)
            return "%s: I'm afraid I can't do that Dave..." % self.plugin_name
