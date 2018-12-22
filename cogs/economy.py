import os
import json
import random
import discord
import datetime
from discord.ext import commands
class Economy:
	def __init__(self,bot):
		self.bot = bot
	@commands.command(pass_context = True,no_pm=True,aliases=["ekonomy","ekonomika","€","balance","bilance"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def economy(self,ctx,user:discord.Member = None):
		if user is None:
			user = str(ctx.message.author)
		filename = "./db/"+str(ctx.message.server.id)+".txt"
		if not os.path.isfile(filename):
			with open(filename,"w+") as file:
				pass
		with open(filename,"r+") as file:			
			try:
				d = json.load(file)				
			except:
				d ={}
			user = str(user)
			if user not in d:
				d[user]={'amount': 100,'last_daily': str(datetime.datetime.now())}
			await self.bot.say(f"{user[:-5]} má na účtě {d[user]['amount']}:dollar:")
		with open(filename,"w+") as file:
			json.dump(d,file)
	
	@commands.command(pass_context = True,no_pm=True,aliases=["denne","deni","dailyscheckel","neetbux","šekel"])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def daily(self,ctx):
		filename = "./db/"+str(ctx.message.server.id)+".txt"
		if not os.path.isfile(filename):
			return await self.bot.say("Ještě si tu nikdo nezaložil účet, použijte příkaz !economy")
		with open(filename,"r+") as file:
			try:
				d = json.load(file)
			except:
				return await self.bot.say("Na tomto serveru ještě nikdo nemá účet, založte ho pomocí !economy !")
			user = str(ctx.message.author)
			if user not in d:
				return await self.bot.say("Na tomto serveru sis ještě nezaložil účet!")
			last = datetime.datetime.strptime(d[user]['last_daily'],"%Y-%m-%d %H:%M:%S.%f")#doplnit formát
			now = datetime.datetime.now()
			time = now-last
			if time.days >= 1:
				d[user]['amount'] += 500
				d[user]['last_daily'] = str(datetime.datetime.now())
				await self.bot.say(f"500:dollar: přidáno! Nyní máš {d[user]['amount']}")
			else:
				await self.bot.say("Pro dnešek už pro tebe žádné šekely nemám, přijď zase zítra!")
		with open(filename,"w+") as file:
			json.dump(d,file)
	
	@commands.command(pass_context = True,no_pm=True,aliases=["susenka","🍪","biscuit"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def cookie(self,ctx,user:discord.Member = None):
		if user is None:
			return await self.bot.say("Nikoho jsi neoznačil!")
		filename = "./db/"+str(ctx.message.server.id)+".txt"
		if not os.path.isfile(filename):
			return await self.bot.say("Na tomto serveru si někdo musí nejdříve založit účet pomocí !economy")
		with open(filename,"r+") as file:
			user = str(user)
			d = json.load(file)
			if user not in d:
				return await self.bot.say(f"Na tomto serveru si {user[:-5]} ještě nezaložil účet!")
			if d[str(ctx.message.author)]['amount']-10 > 0:
				d[user]['amount']+=10
				d[str(ctx.message.author)]['amount'] -= 10
				await self.bot.say(f"{str(ctx.message.author)[:-5]} poslal {user[:-5]} sušenku!:cookie:")
			else:
				await self.bot.say("Promiň, ale jedna sušenka stojí 10 šekelů, a to ty jaksi nemáš :information_desk_person:")
		with open(filename,"w+") as file:
			json.dump(d,file)
	@commands.command(pass_context = True,no_pm=True,aliases=["roulete","ruleta","maty","automat"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def roulette(self,ctx,mlt,amount):
		try:
			mlt = float(mlt)
			amount = int(amount)
		except:
			return await self.bot.say("Jedna z hodnot je špatně!")		
		if not mlt>1:
			return self.bot.say("Násobitel musí být větší než jedna!")
		chance = 1/mlt
		filename = "./db/"+str(ctx.message.server.id)+".txt"
		with open(filename,"r+") as file:
			d = json.load(file)
			if d[str(ctx.message.author)]["amount"]>=amount:
				if random.random() < chance:
					won = amount * mlt
					d[str(ctx.message.author)]["amount"] += won
					chance = chance*100
					await self.bot.say(f"Gratuluji! {str(ctx.message.author)[:-5]} vyhrál {int(won)}:dollar:! Překonal tím šanci mrzkých {round(chance,3)}%")
				else:
					d[str(ctx.message.author)]["amount"]-=amount
					chance = chance*100
					await self.bot.say(f"Ojoj! Štěstěna se na {str(ctx.message.author)[:-5]} neusmála, neboť je teď o {int(amount)} šekelů lehčí!:money_with_wings: Šance na výhru byla {round(chance,3)}%")
			else:
				await self.bot.say("Ohohó! Chtěl jsi vsadit víc peněz než máš na účtě!")
			with open(filename,"w+") as file:
				json.dump(d,file)
	@commands.command(pass_context = True,no_pm=True,aliases=["thief","kradez"])
	@commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
	async def steal(self,ctx,user:discord.Member=None):
		if user is None:
			return await self.bot.say("A koho chceš teda okrást?")
		chance = random.randint(0,10)
		filename = "./db/"+str(ctx.message.server.id)+".txt"
		user = str(user)
		if user == str(ctx.message.author):
			return await self.bot.say("Proč by jsi okrádal sám sebe?")		
		try:
			with open(filename,"r+") as file:
				d = json.load(file)
				if chance>=5:
					want = random.randrange(0,501,10)
					if d[user]["amount"]-want<0:
						stolen = d[user]["amount"]
					elif d[user]["amount"]<0:
						return await self.bot.say("Přece bys neokradl někoho kdo nemá ani na sušenku, že ne?") 
					else: stolen = want
					d[user]["amount"] -= stolen
					d[str(ctx.message.author)]["amount"] += stolen
					await self.bot.say(f"{str(ctx.message.author)[:-5]} ukradl {user[:-5]} {stolen}:dollar:!")
				else:
					stolen = random.randrange(100,551,10)
					d[str(ctx.message.author)]["amount"] -= stolen
					await self.bot.say(f":oncoming_police_car:{str(ctx.message.author)[:-5]} načapala policie při činu! Pokuta činí {stolen} šekelů")
		except:
			pass
		with open(filename,"w+") as file:
			json.dump(d,file)
	@commands.command(pass_context = True,no_pm=True,aliases=["transfer","dej"])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def pay(self,ctx,amount,user:discord.Member=None):
		if user is None:
			return await self.bot.say("Musíš někoho označit!")
		filename = "./db/"+str(ctx.message.server.id)+".txt"
		amount = int(amount)
		user = str(user)
		author = str(ctx.message.author)
		with open(filename,"r+") as file:
			d = json.load(file)
			if d[author]["amount"]<amount:
				return await self.bot.say("Chtěl jsi poslat víc peněz než máš!")
			d[author]["amount"] -= amount
			d[user]["amount"]+=amount
			await self.bot.say(f"{author[:-5]} poslal {user[:-5]} {amount}:dollar:, jak štědré!")
		with open(filename,"w+") as file:
			json.dump(d,file)
			
def setup(bot):
	bot.add_cog(Economy(bot))