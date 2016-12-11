import discord
from discord.ext import commands

def is_owner_check(author):
    return author.id == '186313043150503936'

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message.author))
