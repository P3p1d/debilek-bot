import os
import random
import discord
import datetime
from pymongo import *
from collections import Counter
from discord.ext import commands

class Economy:
	def __init__(self,bot):
		self.bot = bot
		self.col=MongoClient(os.environ["MONGOURI"])
		self.d=self.col.debilek
	@commands.command(pass_context = True,no_pm=True,aliases=["ekonomy","ekonomika","€","balance","bilance"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def economy(self,ctx,user:discord.Member = None):
		await self.bot.send_typing(ctx.message.channel)
		server = str(ctx.message.server.id)
		if user is None:
			user = ctx.message.author
		acc = self.d[server].find_one({"name":str(user)})
		if acc is None:
			self.d[server].insert_one({"name":str(user),"amount":500})
			return await self.bot.say(f"`Účet pro {user.display_name} byl založen!`")
		
		if "pers" in acc:
			t = (datetime.datetime.utcnow()-acc["last_check"]).total_seconds()
			acc["amount"] += t*acc["pers"]
			self.d[server].update_one({"name":str(user)},{"$set":{"last_check":datetime.datetime.utcnow(),"amount":acc["amount"]}})
			return await self.bot.say(f"`{user.display_name} má na účtě {round(acc['amount'],2)} penízků a vydělává {round(acc['pers'],2)} za vteřinu`")
		await self.bot.say(f"`{user.display_name} má na účtě {acc['amount']} penízků`")
	
	@commands.command(pass_context = True,no_pm=True,aliases=["denne","deni","dailyscheckel","neetbux","šekel"])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def daily(self,ctx):
		await self.bot.send_typing(ctx.message.channel)
		user = ctx.message.author
		server = str(ctx.message.server.id)
		acc = self.d[server].find_one({"name":str(user)})
		if acc is None:
			self.d[server].insert_one({"name":str(user),"amount":750,"last_daily":datetime.datetime.utcnow()})
			return await self.bot.say("250:dollar: přidáno!")
		elif "last_daily" not in acc:
			self.d[server].update_one({"name":str(user)},{"$set":{"last_daily":datetime.datetime.utcnow(),"amount":acc["amount"]+250}})
			return await self.bot.say("250:dollar: přidáno!")
		t = (datetime.datetime.utcnow()-acc["last_daily"]).days
		if t < 0:
			return await self.bot.say("`Dnešní příděl šekelů už jsi dostal, přijď zas příště!`")
		self.d[server].update_one({"name":str(user)},{"$set":{"last_daily":datetime.datetime.utcnow(),"amount":acc["amount"]+250}})
		await self.bot.say("250:dollar: přidáno!")

	@commands.command(pass_context = True,no_pm=True,aliases=["susenka","🍪","biscuit"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def cookie(self,ctx,user:discord.Member = None):
		await self.bot.send_typing(ctx.message.channel)
		if user is None:
			return await self.bot.say("Nikoho jsi neoznačil!")
		server = str(ctx.message.server.id)
		acc = self.d[server].find_one({"name":str(user)})
		aut=self.d[server].find_one({"name":str(ctx.message.author)})
		if acc is None:
			return await self.bot.say(f"`{user.display_name} si ještě nezaložil účet pomocí §economy !`")
		elif aut is None:
			return await self.bot.say("`Nemůžeš rozdávat sušenky aniž by sis založil účet pomocí §economy !`")
		if aut["amount"]<10:
			return await self.bot.say("`Jedna sušenka stojí 10 šekelů, a to ty jaksi nemáš`")
		self.d[server].update_one({"name":str(user)},{"$set":{"amount":acc["amount"]+10}})
		self.d[server].update_one({"name":str(ctx.message.author)},{"$set":{"amount":aut["amount"]-10}})
		await self.bot.say(f"`{ctx.message.author.display_name} poslal {user.display_name} sušenku!`")

	@commands.command(pass_context = True,no_pm=True,aliases=["thief","kradez"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def steal(self,ctx,user:discord.Member=None):
		await self.bot.send_typing(ctx.message.channel)
		if user is None:
			return await self.bot.say("A koho chceš teda okrást?")
		if user == str(ctx.message.author):
			return await self.bot.say("Proč by jsi okrádal sám sebe?")
		chance = random.randint(0,10)
		server = str(ctx.message.server.id)
		acc = self.d[server].find_one({"name":str(user)})
		aut=self.d[server].find_one({"name":str(ctx.message.author)})
		if acc is None or aut is None:
			return await self.bot.say("Jeden z vás si ještě nezaložil účet")
		
		if chance>=5:
			stolen = random.randrange(0,600,10)
			if acc["amount"]-stolen<0:
				stolen = acc["amount"]
			if acc["amount"]<=0:
				return await self.bot.say("Přece bys neokradl někoho kdo nemá ani na sušenku, že ne?") 
			self.d[server].update_one({"name":str(user)},{"$set":{"amount":acc["amount"]-stolen}})
			self.d[server].update_one({"name":str(ctx.message.author)},{"$set":{"amount":aut["amount"]+stolen}})
			await self.bot.say(f"{ctx.message.author.display_name} ukradl {user.display_name} {stolen}:dollar:!")
		else:
			stolen = random.randrange(50,550,10)
			self.d[server].update_one({"name":str(ctx.message.author)},{"$set":{"amount":aut["amount"]-stolen}})
			await self.bot.say(f":oncoming_police_car:{ctx.message.author.display_name} načapala policie při činu! Pokuta činí {stolen} šekelů")

	@commands.command(pass_context = True,no_pm=True,aliases=["roulete","ruleta"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def automat(self,ctx,mlt,amount):
		await self.bot.send_typing(ctx.message.channel)
		try:
			mlt = float(mlt)
			amount = int(amount)
		except:
			return await self.bot.say("Jedna z hodnot je špatně!")		
		if mlt<=1:
			return self.bot.say("Násobitel musí být větší než jedna!")
		chance = 1/mlt
		server = str(ctx.message.server.id)
		a = self.d[server].find_one({"name":str(ctx.message.author)})
		if a is None:
			return await self.bot.say("Ještě sis nezaložil účet!")
		if a["amount"]<amount:
			return await self.bot.say("Chtěl si vsadit víc peněz než máš na účtě!")
		if random.random() > chance:
			self.d[server].update_one({"name":str(ctx.message.author)},{"$set":{"amount":a["amount"]-amount}})
			return await self.bot.say(f"`{ctx.message.author.display_name} prohrál {float(amount)} šekelů!`")
		won = mlt*amount
		self.d[server].update_one({"name":str(ctx.message.author)},{"$set":{"amount":a["amount"]+won}})
		await self.bot.say(f"`{ctx.message.author.display_name} vyhrál v automatu {won} šekelů!`")
	
	@commands.command(pass_context = True,no_pm=True,aliases=["biz"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def business(self,ctx):
		await self.bot.send_typing(ctx.message.channel)
		point = self.col.biz.bizdb.find({})
		e=discord.Embed(colour=discord.Colour.green())
		for doc in point:
			e.add_field(name=doc["name"],value=f'id: {doc["id"]}\ncena: {doc["price"]}:dollar:\n{doc["des"]}',inline=False)
		e.set_author(name="Byznys")
		e.set_footer(text="Byznys si koupíš pomocí §buy <id>")
		await self.bot.say(embed=e)
	
	async def getpers(self,a):
		val = 0
		counted=Counter(a["bizs"])
		for biz,num in counted.items():
			biz=self.col.biz.bizdb.find_one({"id":biz})
			val+=biz["pers"]*num
		return val
	
	@commands.command(pass_context = True,no_pm=True,aliases=["kup"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def buy(self,ctx,bizid:int=0):
		await self.bot.send_typing(ctx.message.channel)
		server = str(ctx.message.server.id)
		if bizid==0:
			return await self.bot.say("Neřekl jsi, co si chceš koupit!")
		elif bizid<1:
			return await self.bot.say("ID musí být větší než nula")
		biz = self.col.biz.bizdb.find_one({"id":bizid})
		if biz is None:
			return await self.bot.say("Tento byznys neexistuje!")
		a = self.d[server].find_one({"name":str(ctx.message.author)})
		if a is None:
			return await self.bot.say("Ještě sis nezaložil účet!")
		elif biz["price"]>a["amount"]:
			return await self.bot.say("Na tento byznys nemáš peníze!")
		self.d[server].update_one({"name":str(ctx.message.author)},{"$push":{"bizs":bizid}})
		a = self.d[server].find_one({"name":str(ctx.message.author)})
		upers = await self.getpers(a)																							
		if "last_check" not in a:
			self.d[server].update_one({"name":str(ctx.message.author)},{"$set":{"amount":a["amount"]-float(biz["price"]),"pers":upers,"last_check":datetime.datetime.utcnow()}})
		else:
			self.d[server].update_one({"name":str(ctx.message.author)},{"$set":{"amount":a["amount"]-float(biz["price"]),"pers":upers}})
		await self.bot.say(f"Úspěšně sis koupil předmět {biz['name']}!")

	@commands.command(pass_context = True,no_pm=True,aliases=["inventář"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def inventory(self,ctx,user:discord.Member=None):
		await self.bot.send_typing(ctx.message.channel)
		server = str(ctx.message.server.id)
		if user is None:
			user=ctx.message.author
		a = self.d[server].find_one({"name":str(user)})
		if a is None:
			return await self.bot.say(f"{user.display_name} si ještě nezaložil účet")
		if "bizs" not in a:
			return await self.bot.say(f"{user.display_name} si ještě nic nekoupil!")
		counted=Counter(a["bizs"])
		e=discord.Embed(colour=discord.Colour.green())
		for biz,num in counted.items():
			biz=self.col.biz.bizdb.find_one({"id":biz})
			e.add_field(name=biz["name"],value=f"{num} krát\nVydělává {round(num*biz['pers'],2)} za vteřinu",inline = False)
		e.set_author(name=user.display_name,icon_url=user.avatar_url)
		await self.bot.say(embed=e)

def setup(bot):
	bot.add_cog(Economy(bot))
