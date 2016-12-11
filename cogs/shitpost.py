import discord
from discord.ext import commands
from collections import deque
from datetime import datetime
from bs4 import BeautifulSoup
import praw
import random
import shutil
import requests
import imghdr

class Shitpost:
    subreddits = ['anime_irl', 'me_irl', '4chan']

    help_str = '''\
Retrieves and reposts a random shitpost'''

    # Description for praw
    r_desc = 'Retrieve hot submissions from specified subreddits for shitposting'
    # Version of the module
    ver = '1.0.0'
    # Number of hours before refreshing list
    # 60 seconds * 60 minutes * 6 hours
    hours = 60 * 60 * 6

    def __init__(self, bot):
        self.bot = bot
        # The last time hot submissions were retrieved. Refresh every 12 hours or so
        self.last_retrieved = None
        # The list of post ID's and their associated imgur link in a list of tuples
        # (Submission name, Submission url)
        self.submissions = []

        # Retrieve first batch of submissions
        self.__retrieve_submissions()

    @commands.command(name='shitpost', help=help_str, brief='Shitpost', aliases=['shit'])
    async def shitpost(self):
        cur_time = datetime.utcnow()
        delta = cur_time - self.last_retrieved
        if not self.submissions or delta.days > 0 or delta.seconds >= Shitpost.hours:
            self.__retrieve_submissions()

        if self.submissions:
            shitpost = self.submissions.pop()

            fdata, fname = self.__retrieve_media(shitpost)
            await self.bot.upload(fp=fdata.raw, filename=fname)
        else:
            # Retreival was not successful, either all posts have been viewed or some error occured
            await self.bot.say('There are currently no viewable shitposts. Please try again later')

    '''
    Retrieves posts from specified subreddit
    '''
    def __retrieve_submissions(self):
        # Initialize praw
        r = praw.Reddit(' '.join([Shitpost.r_desc, Shitpost.ver]))
        # Update the time of retrieval
        self.last_retrieved = datetime.utcnow()

        for current_sub in Shitpost.subreddits:
            sub = r.get_subreddit(current_sub)
            for submission in sub.get_top_from_day(limit=25):
                # Filter out stickied mod posts and self text posts
                if not submission.stickied and not submission.is_self:
                    entry = (submission.name, submission.url, submission.domain)
                    # Ensure no duplicate entries
                    if entry not in self.submissions:
                        self.submissions.append(entry)
        random.shuffle(self.submissions)

    def __retrieve_media(self, shitpost):
        print('Retrieving media')
        print('information',shitpost)
        response = requests.get(shitpost[1], stream=True)
        fname = shitpost[1].split('/')[-1]
        if shitpost[2] == 'imgur.com':
            soup = BeautifulSoup(response.text, 'html.parser')
            link = 'http:' + soup.find_all('div', class_='post-image')[0].img['src']

            print('fixed link', link)
            fname = link.split('/')[-1]
            response = requests.get(link, stream=True)
        elif shitpost[2] == 'gfycat.com':
            fname += '-size_restricted.gif'
            link = 'https://thumbs.gfycat.com/' + fname
            print('fixed link', link)
            response = requests.get(link, stream=True)
        elif shitpost[2] == 'i.reddituploads.com':
            extension = imghdr.what(file='', h=response.raw.data)
            fname += '.' + extension
        print(shitpost[0], shitpost[1], fname)
        print('Successfully retreived')
        return response, fname

    @shitpost.error
    async def err(self, error, ctx):
        await self.bot.say('An error occurred when retrieving a shitpost. Please try again')

def setup(bot):
    bot.add_cog(Shitpost(bot))
