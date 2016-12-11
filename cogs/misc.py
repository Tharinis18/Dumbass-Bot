import discord
from discord.ext import commands
from cogs import permissions

class Misc:

    help_str_trout = '''\
target refers to the person you want to slap

Beware when slapping another bot or the creator of the bot'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='trout', help=help_str_trout, brief='Slap someone', aliases=['whale'], pass_context=True)
    async def trout(self, ctx, target : discord.User):
        called_alias = ctx.invoked_with
        triggered = False
        if permissions.is_owner_check(target) or target.bot:
            target = ctx.message.author
            triggered = True

        message = '*Slaps the shit out of {target} with a {weapon}'.format(target=target.mention, weapon=called_alias)
        
        if triggered:
            message += ' after being triggered by them.'
        message += '*'

        await self.bot.delete_message(ctx.message)
        await self.bot.say(message)

    @trout.error
    async def dumb_person(self, error, ctx):
        target = ctx.message.author.mention
        message = '*Slaps the shit out of {target} for being too stupid to use this command correctly*'.format(target=target)
        await self.bot.say(message)


def setup(bot):
    bot.add_cog(Misc(bot))
