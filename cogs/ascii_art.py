import random
import discord
import requests
from unidecode import unidecode
from discord.ext import commands
class ASCII:
	def __init__(self,bot):
		self.bot = bot
	def remove_non_ascii(self,text):
		return unidecode(text)
	@commands.command(pass_context = True,aliases=["ascii","aesthetic","asci"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def asciiart(self,ctx,*text):
		text = " ".join(text)
		text = self.remove_non_ascii(text)
		url = "http://artii.herokuapp.com/make?text="+str(text)
		page = requests.get(url).text
		await self.bot.say(f"```{str(page)}```")
def setup(bot):
	bot.add_cog(ASCII(bot))