import discord
from discord.ext import commands
from cogs import permissions

class Cleanup:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    @permissions.is_owner()
    async def cleanup(self, ctx, num : int=100, content='all'):
        '''
        If content is 'all' delete everything
        If content is 'commands' delete all command related items
        '''
        if num > 100:
            self.bot.say('Max number of messages bulk deletable is 100')
            return

        channel = ctx.message.channel

        expression = lambda m: True
        if content == 'commands':
            expression = lambda m: m.author.bot or m.content.startswith('!')
        elif content not in ['all']:
            self.bot.say('Invalid deletion type.')
        
        deleted = 0
        async for m in self.bot.logs_from(channel, before=ctx.message):
            if expression(m):
                await self.bot.delete_message(m)
                deleted += 1
                if deleted >= num:
                    break

        await self.bot.say('Cleanup complete. {} message(s) were deleted'.format(deleted))

    help_str_delete = '''\
num refers to the number of messages to delete

user refers to who\'s messages are to be deleted, however you cannot use this feature unless you are mitsuru'''

    @commands.command(name='delete', help=help_str_delete, brief='Mass delete messages', pass_context=True)
    async def _delete(self, ctx, num : int=100, user : discord.Member=None):
        channel = ctx.message.channel

        calling_user = ctx.message.author

        if user is not None and calling_user.id != user.id and not permissions.is_owner_check(calling_user):
            await self.bot.say('You have insufficient permissions to delete other people\'s messages')
            return

        user = calling_user if user is None else user

        deleted = 0
        async for m in self.bot.logs_from(channel, before=ctx.message):
            if m.author.id == user.id:
                await self.bot.delete_message(m)
                deleted += 1
                if deleted >= num:
                    break
        
        await self.bot.say('Cleanup complete. {} message(s) were deleted'.format(deleted))

    @cleanup.error
    @_delete.error
    async def insufficient_permissions(self, error, ctx):
        if isinstance(error, commands.BadArgument):
            await self.bot.say('Invalid usage. Expected !delete num')
        elif isinstance(error, commands.CheckFailure):
            await self.bot.say('You have insufficient permissions faggot')
        else:
            await self.bot.say('Unhandled error:', error)


def setup(bot):
    bot.add_cog(Cleanup(bot))
