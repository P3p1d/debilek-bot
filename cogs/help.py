import discord
from discord.ext import commands
class Help(commands.Cog):
	"""docstring for Help"""
	def __init__(self, bot):
		self.bot = bot
	@commands.command(pass_context = True,aliases = ['pomoc','prikazy',''])
	async def help(self,ctx):
		await ctx.channel.send("https://debilekbot.glitch.me/") 
def setup(bot):
	bot.add_cog(Help(bot))
