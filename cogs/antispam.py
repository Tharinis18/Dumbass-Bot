import discord
from discord.ext import commands
from datetime import datetime
from collections import defaultdict, deque

class AntiSpam:

    name = 'spam'
    CACHE_LIMIT = 15

    MESSAGE_FREQ = 2
    MESSAGE_PER_FREQ = 5
    MESSAGE_SIMILAR = 5
    MESSAGE_SIMILAR_FREQ = 20

    FREQ_TIME = 10;
    SPAM_TIME = 30;

    SPAM_UNICODE_VAL = 100000

    def __init__(self, bot):
        # Cache of messages recorded
        self.cache = defaultdict(lambda: deque(maxlen=AntiSpam.CACHE_LIMIT)) 
        # If bot has issued a warning recently
        self.warnings = defaultdict(bool)
        # Reference to bot
        self._bot = bot

    async def spam_detected(self, message : discord.Message):
        spammed = False

        currtime = message.timestamp

        if message.author.id in self.cache:

            num_messages = 0
            message_oldest = None
            num_repetition = 0
            spam_oldest = None

            for m in reversed(self.cache[message.author.id]):
                seconds_elapsed = int((currtime - m.timestamp).total_seconds())
                # Check spam
                if seconds_elapsed < AntiSpam.FREQ_TIME:
                    num_messages += 1
                    message_oldest = seconds_elapsed
                if seconds_elapsed < AntiSpam.SPAM_TIME and m.content == message.content:
                    num_repetition += 1
                    spam_oldest = seconds_elapsed
                if seconds_elapsed > max(AntiSpam.FREQ_TIME, AntiSpam.SPAM_TIME):
                    break
            print('Repeat: {}, Messaged: {}, Rate: {}'.format(num_repetition, num_messages,\
                    message_oldest / num_messages if message_oldest is not None else -1))
            
            emojis = 0
            for c in message.clean_content:
                if ord(c) > AntiSpam.SPAM_UNICODE_VAL:
                    emojis += 1

            remove = False
            if num_repetition > 4:
                remove = True
                action = 'spamming'
            elif num_messages > 5 and message_oldest / num_messages < 1.0:
                remove = True 
                action = 'flooding'
            elif emojis > 5:
                remove = True
                action = 'shitposting'
            elif message.clean_content.count('\n') > 25:
                remove = True
                action = 'flooding'
            else:
                self.warnings[message.author.id] = False
            if remove:
                spammed = True
                print('Deleting')
                await self._bot.delete_message(message)
                if not self.warnings[message.author.id]:
                    await self._bot.send_message(message.channel, '{0.author.mention} please stop {1}'.format(message, action))
                    self.warnings[message.author.id] = True

        print('Caching: {}'.format(message.content))
        self.cache[message.author.id].append(message)

        return spammed
