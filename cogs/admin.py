import discord
from discord.ext import commands
from cogs import permissions

class Admin:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load', hidden=True)
    @permissions.is_owner()
    async def _load(self, module : str):
        '''Loads a module'''
        if 'cogs' not in module:
            module = 'cogs.' + module
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('{module} successfully loaded'.format(module=module))

    @commands.command(name='unload', hidden=True)
    @permissions.is_owner()
    async def _unload(self, module : str):
        '''Unloads a module.'''
        if 'cogs' not in module:
            module = 'cogs.' + module
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('{module} successfully unloaded'.format(module=module))

    @commands.command(name='reload', hidden=True)
    @permissions.is_owner()
    async def _reload(self, module : str):
        '''Reloads a module'''
        if 'cogs' not in module:
            module = 'cogs.' + module
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('{module} successfully reloaded'.format(module=module))

    @commands.command(hidden=True)
    @permissions.is_owner()
    async def shutdown(self):
        '''Shutdown the bot'''
        await self.bot.say('Shutting down')
        await self.bot.logout()

    @_load.error
    @_unload.error
    @_reload.error
    async def insufficient_permissions(self, error, ctx):
        await self.bot.say('You have insufficient permissions faggot')
            
def setup(bot):
    bot.add_cog(Admin(bot))
