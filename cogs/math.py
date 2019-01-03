import os
import re
import math
import asyncio
import discord
import numpy as np
import matplotlib.pyplot as plt
from discord.ext import commands

class TimedOutExc(Exception):
	pass
class Math:
	def __init__(self,bot):

		self.bot = bot
	async def getgraph(self,ctx,args):
		x=np.array(np.linspace(-100,100,1000))
		var = {'x':x,'sin':np.sin,'cos':np.cos,'sqrt':np.sqrt,'log':np.log,'abs':np.abs,'pow':np.power}
		if "**" in args:
			return await self.bot.send_message(ctx.message.channel,"Neplatný ** operátor, použij pow()")
		if "x" not in args:
			args= "x-x+"+args
		try:
			plt.plot(x, eval(args,var),"r-")
		except FloatingPointError:
			return await self.bot.send_message(ctx.message.channel,"Výpočet trval příliš dlouho")
		except OverflowError:
			return await self.bot.send_message(ctx.message.channel,"Čísla jsou moc velká")
		except NameError as e:
			print(e)
			return await self.bot.send_message(ctx.message.channel,"Zadal jsi neznámou, kterou opravdu neznám")
		except SyntaxError:
			return await self.bot.send_message(ctx.message.channel,"Někde máš překlep (možná chybějící závorka?)")
		except ZeroDivisionError:
			return await self.bot.send_message(ctx.message.channel,"`∞`")
		plt.grid(True, which='both')
		plt.axhline(y=0, color='k')
		plt.axvline(x=0, color='k')
		filename = str(ctx.message.server.id)+".jpg"
		plt.savefig(filename,bbox_inches='tight')
		plt.gcf().clear()
		await self.bot.send_file(ctx.message.channel,filename)
		os.remove(filename)

	@commands.command(pass_context=True,aliases=["y=","graf"])
	async def graph(self,ctx,*args):		
		await self.bot.send_typing(ctx.message.channel)	
		np.seterr(over="raise",divide="raise")
		args = ' '.join(args)
		await self.getgraph(ctx,args)
def setup(bot):
	bot.add_cog(Math(bot))
