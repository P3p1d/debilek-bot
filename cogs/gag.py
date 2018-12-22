import discord
from discord.ext import commands
import requests
import json
import random
class Imgur:
	def __init__(self,bot):
		self.bot = bot
	@commands.command(pass_context = True,aliases = ['9gag','meme'])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def Imgur(self,ctx):
		url = "https://api.imgur.com/3/gallery/hot/viral/0.json"
		try:
			r = requests.get(url)
			r=r.json()
		except json.JSONDecodeError:
			return await self.bot.say("Chybička se vloudila")
		r = r['data']
		img = random.choice(r)
		embed=discord.Embed(title=img['account_url'], url=img["link"], description=img["description"], color=0x17ec3d)
		embed.set_author(name=img["title"])
		embed.add_field(name="Like", value=img["ups"], inline=True)
		embed.add_field(name="Dislike", value=img["downs"], inline=True)
		embed.set_footer(text="Data poskytuje Imgur.com")
		await self.bot.say(embed=embed)
		await self.bot.say(img["link"])
def setup(bot):
	bot.add_cog(Imgur(bot))