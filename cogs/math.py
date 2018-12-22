import os
import re
import math
import discord
import numpy as np
import matplotlib.pyplot as plt
from discord.ext import commands
class Math:
	def __init__(self,bot):
		self.bot = bot
	@commands.group(pass_context=True, aliases=['matika','m','='])
	async def math(self,ctx):
		pass
"""
	def dis(self,a,b,c):
		d = (b**2)-4*a*c
		return d
	@math.command(pass_context =True,aliases=['kvadra','kvadraticka','quadratic','quad','q'])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def quadra(self,ctx,a,b,c):
		try:
			a,b,c=float(a),float(b),float(c)
			if a>500 or b>500 or c>500:
				return await self.bot.say("Zadaná čísla jsou moc velká, maximum je 500")
		except:
			return await self.bot.say("To asi nejsou opravdová čísla, co?")
		d = self.dis(a,b,c)
		if d<0:
			await self.bot.say("Diskriminant je menší než nula!")
			return
		else:
			xst = (-b+math.sqrt(d))
			xnd = (-b-math.sqrt(d))
			xst = xst/2*a
			xnd = xnd/2*a
			await self.bot.say(f"X1 je {xst}\nX2 je {xnd}")
			if d == 0:
				x = np.linspace(-20*xst, 20*xst, 1000)
			else:
				x = np.linspace(xst, xnd, 1000)
			y = a*(x**2)+b*x+c
			#print(y)
			fig, ax = plt.subplots()
			ax.plot(x, y)		
			ax.grid(True, which='both')
			ax.axhline(y=0, color='k')
			ax.axvline(x=0, color='k')
			filename = str(ctx.message.server.id) + '.png'
			plt.savefig(filename,bbox_inches='tight')
			await self.bot.send_file(ctx.message.channel,filename)
			os.remove(filename)
	@math.command(pass_context =True,aliases=['='])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def solve(self,ctx,*args):
		args = ' '.join(args)
		env = {"locals": None,"globals":None,"__builtins__": None,"__name__":None,"__file__":None}
		if not re.search('[a-zA-Z]', args) and len(args)>0 and "_" not in args:
			try:	
				val = eval(args,env)
			except ZeroDivisionError:
				return await self.bot.say("Dělení nulou moc nedoporučuji")
			except TypeError:
				return await self.bot.say("S hodnotami je něco špatně...")
			except SyntaxError:
				return await self.bot.say("Vyskytla se chybka v syntaxi...")
			val = str(val)
			if val == "False": val = "Nepravda"
			elif val == "True": val = "Pravda"
			else:
				try:
					val = round(float(val),5)
				except:
					pass
			return await self.bot.say(f"`{val}`")
		else:
			return await self.bot.say("Buďto se mě zkoušíš hacknout, nebo jsi nic nezadal!")
	"""
	@commands.command(pass_context=True,aliases=["y=","graf"])
	async def graph(self,ctx,*args):
		args = ' '.join(args)
		env = {"globals":None,"__builtins__": None,"__name__":None,"__file__":None}
		if len(args)>0 and "_" not in args:
			x = np.array(np.linspace(-100,100,1000))
			y = eval(args)
			plt.plot(x, y)
			plt.grid(True, which='both')
			plt.axhline(y=0, color='k')
			plt.axvline(x=0, color='k')
			filename = str(ctx.message.server.id) + '.png'
			plt.savefig(filename,bbox_inches='tight')
			await self.bot.send_file(ctx.message.channel,filename)
			os.remove(filename)
	"""
def setup(bot):
	bot.add_cog(Math(bot))