import traceback
import sys
import discord
from discord.ext import commands
from discord import errors
"""
If you are not using this inside a cog, add the event decorator e.g:
@bot.event
async def on_command_error(ctx, error)
For examples of cogs see:
Rewrite:
https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
Async:
https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5
This example uses @rewrite version of the lib. For the async version of the lib, simply swap the places of ctx, and error.
e.g: on_command_error(self, error, ctx)
For a list of exceptions:
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#errors
"""


class CommandErrorHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.Cog.listener()
	async def on_command_error(self,ctx,error):
		channel = ctx.message.channel
		if isinstance(error,commands.CommandOnCooldown):
			return await ctx.channel.send(f"{ctx.message.author.mention} v klidu bejku! Ještě musíš {error.retry_after:.1f} sekund vychladnout.")
		elif isinstance(error,commands.CommandNotFound):
			return await ctx.channel.send("Tenhle příkaz neznám :disappointed_relieved: \nZkus §help")
		elif isinstance(error,commands.BadArgument):
			return await ctx.channel.send("Asi překlep?")
		elif isinstance(error,commands.MissingRequiredArgument):
			return await ctx.channel.send("Něco mi tam chybí")
		elif isinstance(error,commands.TooManyArguments):
			return await ctx.channel.send("To je na mě trochu moc věcí, zkus to zkrátit")
		elif isinstance(error,ValueError):
			return await ctx.channel.send("Se zadanou hodnotou je něco špatně :/")
		elif isinstance(error,commands.NoPrivateMessage):
			return await ctx.channel.send("Hele, tady v intimču DMs tyhle příkazy používat nemůžeš...")
		elif isinstance(error,errors.HTTPException):
			return await ctx.channel.send("Odehrála se chyba v matrixu. Nebo prostě někdo cestou zakopl o kabel.")
		elif isinstance(error,errors.Forbidden):
			return await ctx.channel.send("Někdo mi odepřel přístup na internet... hmmm")
		"""elif isinstance(error,commands.CommandInvokeError):
			return await ctx.channel.send(channel,"Něco je špatně...")"""
		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
def setup(bot):
	bot.add_cog(CommandErrorHandler(bot))
