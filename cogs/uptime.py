import discord
from discord.ext import commands
from datetime import datetime

def dhms(s):
    m = s / 60
    seconds = s % 60
    h = m / 60
    minutes = m % 60
    days = h / 24
    hours = h % 24
    return map(int, [days, hours, minutes, seconds])


class Uptime:
    
    def __init__(self, bot):
        self.bot = bot
        self.start = datetime.utcnow()

    @commands.command(name='uptime', help='Times how long the bot has been active', brief='Track the uptime of the bot')
    async def uptime(self):
        end = datetime.utcnow()
        delta = end - self.start
        d, h, m, s = dhms(delta.total_seconds())
        await self.bot.say('Uptime: {:02d}:{:02d}:{:02d}:{:02d}'.format(d, h, m, s))

def setup(bot):
    bot.add_cog(Uptime(bot))
