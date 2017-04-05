# -*- coding: utf-8 -*-
"""
This module runs basically everything.

Attributes:
    VERSION = "2.0.0" (String): Version Number: release.version_num.revision_num

    # Config Variables
    EMOJI_LIST (List): List of Strings for emojis to be added to announcements
    USER_LIST (JSON): List of users in JSON format
    ADMIN (List): ["U25PPE8HH", "U262D4BT6", "U0LAMSXUM", "U3EAHHF40"] testing defaults
    TTPB (String): Config variable, sets channel for cleverbot integration
    GENERAL (Stirng): Config variable, sets channel for general's name
    LOG (boolean): Global Variable
    LOGC (boolean): Global Variable
    pbCooldown (int): Global Variable

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from slackclient import SlackClient
import threading, websocket, json, re, time, codecs, random
import scripts
from scripts import commands

class Bot(object):
    ADMIN = ["U25PPE8HH", "U118FGXFA", "U0LAMSXUM", "U3EAHHF40"]
    EMOJI_LIST = ["party-parrot", "venezuela-parrot", "star2", "fiesta-parrot", "wasfi_dust", "dab"]
    GENERAL_CHANNEL = ""
    TTPB = "talk-to-pantherbot"
    VERSION = "2.0.0"

    def __init__(self, token, bot_name=""):
        self.SC = None
        self.BOT_NAME = bot_name
        self.BOT_ICON_URL = "http://i.imgur.com/QKaLCX7.png"
        self.USER_LIST = None
        self.POLLING_LIST = dict()
        self.WEBSOCKET = None
        self.THREADS = []
        self.pb_cooldown = True
        self.create_sc(token)

    def create_sc(self, token):
    	self.SC = SlackClient(token)

    # Returns a list of channel IDs searched for by name
    def channels_to_ids(self, channel_names):
        pub_channels = self.SC.api_call(
            "channels.list",
            exclude_archived=1
        )
        pri_channels = self.SC.api_call(
            "groups.list",
            exclude_archived=1
        )
        li = []
        for channel in pub_channels["channels"]:
            for num in range(0, len(channel_names)):
                if channel["name"].lower() == channel_names[num].lower():
                    li.append(channel["id"])
        # Same as above
        for channel in pri_channels["groups"]:
            for num in range(0, len(channel_names)):
                if channel["name"].lower() == channel_names[num].lower():
                    li.append(channel["id"])
        return li

    # Send Message
    # Sends a message to the specified channel (looks up by channel name, unless is_id is True)
    def smsg(self, channel, text, is_id=False):
        if not is_id:
            channel_id = self.channels_to_ids([channel])[0]
        else:
            channel_id = channel
        self.SC.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=text,
            username=self.BOT_NAME,
            icon_url=self.BOT_ICON_URL
        )
        print "PantherBot:LOG:Message sent"

    def rreaction(self, channel, ts, emoji):
        self.SC.api_call(
            "reactions.add",
            name=emoji,
            channel=channel,
            timestamp=ts
        )
        print "PantherBot:LOG:Reaction posted"