"""from discord.ext import commands
class Dong:
	def __init__(self, bot):
		self.bot = bot
def setup(bot):
	bot.add_cog(Dong(bot))"""
import json
import random
with open("dongs.txt",'r') as file:
	links = json.load(file)
	dong = random.choice(links)
	print(dong)

