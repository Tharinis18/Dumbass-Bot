import discord
from discord.ext import commands
import random

class Dice:
    max_die = 20

    help_str = '''\
x refers to the number of dice to roll

x is an optional argument and when omitted will default to one

y refers to the type of dice to roll

Omitting the xdy argument defaults to rolling one d20

Max number of rollable dice is {max_die}

The available types of die are d3, d4, d5, d6, d8, d10, and d20
'''.format(max_die=max_die)

    available_die = [3, 4, 5, 6, 8, 10, 20, 100]

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', help=help_str, brief='Roll some dice', aliases=['dice', 'r'])
    async def roll(self, xdy : str = '1d20'):
        try:
            num_dice, limit = xdy.split('d')
            if not num_dice:
                num_dice = 1
            else:
                num_dice = int(num_dice)
            limit = int(limit)
        except Exception as e:
            await self.bot.say('Invalid usage. Expected !roll xdy')
        else:
            if num_dice > Dice.max_die:
                await self.bot.say('The max number of die you can roll is {max_die}'.format(max_die=Dice.max_die))
            elif limit not in Dice.available_die:
                await self.bot.say('Invalid dice type')
            else:
                rolls = [random.randint(1, limit) for r in range(num_dice)]
                await self.bot.say('`[' + ']['.join(map(str, rolls)) + '] = ' + str(sum(rolls)) + '`')

    @roll.error
    async def roll_error(self, error, ctx):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            await self.bot.say(error)

def setup(bot):
    bot.add_cog(Dice(bot))
