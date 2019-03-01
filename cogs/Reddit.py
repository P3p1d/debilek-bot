import discord
from discord.ext import commands
import praw
import random
from cachetools import cached, TTLCache
import os

class Reddit(commands.Cog):
	cache=TTLCache(maxsize=50, ttl=1800)
	def __init__(self,bot,client_id,client_secret,user_agent):
		self.bot = bot
		self.reddit=praw.Reddit(client_id=client_id,
					 client_secret=client_secret,
					 user_agent=user_agent)

	@cached(cache)
	def getsubmission(self,subreddit,post_to_pick):
		memes_submissions = self.reddit.subreddit(subreddit).hot(limit=50)
		for i in range(0, post_to_pick):
			submission = next(x for x in memes_submissions if not x.stickied)
		return submission

	def embedbuild(self,s):
		e = discord.Embed(colour=random.randint(0,0xFFFFFF),title=s.author.name,url=s.url)
		e.set_image(url=s.url)
		#e.set_thumbnail(url=s.author.icon_img)
		e.set_author(name=s.title)
		e.add_field(name="Hodnocení",value=f"{s.upvote_ratio*100}%",inline=True)
		e.add_field(name="Komentáře",value=f"{s.num_comments} komentářů")
		e.set_footer(text="Memečka poskytuje reddit.com")
		return e

	@commands.command(pass_context = True,no_pm=True,aliases=["mem"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def meme(self,ctx):
		await ctx.channel.trigger_typing()
		post_to_pick = random.randint(1, 50)
		s=self.getsubmission("dankmemes",post_to_pick)
		e=self.embedbuild(s)
		await ctx.channel.send(embed=e)

	@commands.command(pass_context = True,no_pm=True,aliases=["agraelus"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def agrmeme(self,ctx):
		await ctx.channel.trigger_typing()
		post_to_pick = random.randint(1, 50)
		s=self.getsubmission("Agraelus",post_to_pick)
		e=self.embedbuild(s)
		await ctx.channel.send(embed=e)
def setup(bot):
	bot.add_cog(Reddit(bot,os.environ["clientid"],os.environ["clientsecret"],os.environ["useragent"]))
