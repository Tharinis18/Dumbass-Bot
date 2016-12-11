#!/usr/bin/env python3

import discord
from discord.ext import commands
from cogs.antispam import AntiSpam
from cogs import permissions
import logging
import random
import sys

description = '''Dumbass Bot'''

extensions = [
    'cogs.dice',
    'cogs.admin',
    'cogs.misc',
    'cogs.uptime',
    'cogs.cleanup',
    'cogs.shitpost'
]

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord_bot.log', encoding='utf-8', mode='w')
log.addHandler(handler)

help_attrs = dict(hidden=True)
bot = commands.Bot(command_prefix='!', description=description, pm_help=None, help_attrs=help_attrs)

spam = AntiSpam(bot)

@bot.event
async def on_command_error(error, ctx):
    print('{0.command.qualified_name} was issued.'.format(ctx), error)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if permissions.is_owner_check(message.author) or not await spam.spam_detected(message):
        await bot.process_commands(message)

@bot.event
async def on_command(command, ctx):
    message = ctx.message
    destination = '#{0.channel.name} ({0.server.name})'.format(message)
    log.info('{0.timestamp}: {0.author.name} in {1}: {0.content}'.format(message, destination))

@bot.event
async def on_ready():
    print('Successfully logged in')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('--- El Psy Kongroo ---')

if __name__ == '__main__':
    with open('PRIVATE_API_KEYS.txt', 'r+') as f:
        key = f.readline().strip()

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    if key:
        bot.run(key)
    else:
        print('Key not found in PRIVATE_API_KEYS.txt')

    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
