import discord
import random
import json
import requests
from discord.ext import commands
from datetime import datetime as dt
from datetime import timedelta
class NASA(commands.Cog):
	def __init__(self,bot):
		self.bot=bot

	def getdate(self):
		startdate="19950116"
		startdate=dt.strptime(startdate, '%Y%m%d')
		nbdays=(dt.today()-startdate).days
		d=random.randint(0,nbdays)
		apodate=startdate+timedelta(days=d)
		return apodate.strftime('%Y-%m-%d')
	def converttime(self,date):
		val = dt.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y")
		return val
		
	@commands.command(pass_context=True, aliases = ["apod","space"])
	@commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
	async def nasa(self,ctx):
		await ctx.channel.trigger_typing()
		url="https://api.nasa.gov/planetary/apod"
		params={'date':self.getdate(),"api_key":"DEMO_KEY"}
		r = requests.Session().get(url=url,params = params)
		try:
			r=r.json()
		except:
			return await ctx.channel.send("Cestou se stala chybka")
		e = discord.Embed(colour = random.randint(0, 0xFFFFFF))
		e.set_author(name=r["title"])
		e.add_field(name=self.converttime(r["date"]),value=r["media_type"],inline=True)
		await ctx.channel.send(embed=e)
		await ctx.channel.send(r["url"])
def setup(bot):
	bot.add_cog(NASA(bot))
