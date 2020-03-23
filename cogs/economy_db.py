import os
import random
import discord
import datetime
from pymongo import *
from collections import Counter
from discord.ext import commands

class Economy(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.col=MongoClient("mongodb://pepid:debilekbot@cluster0-shard-00-00-xbaeu.mongodb.net:27017,cluster0-shard-00-01-xbaeu.mongodb.net:27017,cluster0-shard-00-02-xbaeu.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")#os.environ["MONGOURI"])
		self.d=self.col.debilek
	def parser(self,x):
		i = -3
		fmtd = ""
		if len(x) < 4:
			return x
		while True:
			fmtd = x[i:] + " " + fmtd
			if len(x) <= 2:
				return fmtd
			x = x[:i:]

	@commands.command(pass_context = True,no_pm=True,aliases=["ekonomy","ekonomika","€","balance","bilance"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def economy(self,ctx,user:discord.Member = None):
		await ctx.channel.trigger_typing()
		guild = str(ctx.message.guild.id)
		if user is None:
			user = ctx.message.author
		acc = self.d[guild].find_one({"name":str(user)})
		if acc is None:
			self.d[guild].insert_one({"name":str(user),"amount":500})
			return await ctx.channel.send(f"`Účet pro {user.display_name} byl založen!`")
		
		if "pers" in acc:
			t = (datetime.datetime.utcnow()-acc["last_check"]).total_seconds()
			acc["amount"] += t*acc["pers"]
			self.d[guild].update_one({"name":str(user)},{"$set":{"last_check":datetime.datetime.utcnow(),"amount":acc["amount"]}})
			if acc['amount'] >= 10000:
				val = self.parser(str(int(acc['amount'])))
			else:
				val=round(acc['amount'],2)
			return await ctx.channel.send(f"`{user.display_name} má na účtě {val} penízků a vydělává {round(acc['pers'],2)} za vteřinu`")
		await ctx.channel.send(f"`{user.display_name} má na účtě {acc['amount']} penízků`")

	@commands.command(pass_context = True,no_pm=True,aliases=["susenka","🍪","biscuit"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def cookie(self,ctx,user:discord.Member = None):
		await ctx.channel.trigger_typing()
		if user is None:
			return await ctx.channel.send("Nikoho jsi neoznačil!")
		guild = str(ctx.message.guild.id)
		acc = self.d[guild].find_one({"name":str(user)})
		aut=self.d[guild].find_one({"name":str(ctx.message.author)})
		if acc is None:
			return await ctx.channel.send(f"`{user.display_name} si ještě nezaložil účet pomocí §economy !`")
		elif aut is None:
			return await ctx.channel.send("`Nemůžeš rozdávat sušenky aniž by sis založil účet pomocí §economy !`")
		if aut["amount"]<10:
			return await ctx.channel.send("`Jedna sušenka stojí 10 šekelů, a to ty jaksi nemáš`")
		self.d[guild].update_one({"name":str(user)},{"$set":{"amount":acc["amount"]+10}})
		self.d[guild].update_one({"name":str(ctx.message.author)},{"$set":{"amount":aut["amount"]-10}})
		await ctx.channel.send(f"`{ctx.message.author.display_name} poslal {user.display_name} sušenku!`")

	@commands.command(pass_context = True,no_pm=True,aliases=["thief","kradez"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def steal(self,ctx,user:discord.Member=None):
		await ctx.channel.trigger_typing()
		if user is None:
			return await ctx.channel.send("A koho chceš teda okrást?")
		if user == str(ctx.message.author):
			return await ctx.channel.send("Proč by jsi okrádal sám sebe?")
		chance = random.randint(0,10)
		guild = str(ctx.message.guild.id)
		acc = self.d[guild].find_one({"name":str(user)})
		aut=self.d[guild].find_one({"name":str(ctx.message.author)})
		if acc is None or aut is None:
			return await ctx.channel.send("Jeden z vás si ještě nezaložil účet")

		if "protection" in acc:
			if (datetime.datetime.now()-acc["protection"]).days < 1:
				return await ctx.channel.send(f"{user.display_name} má zapnutou ochranu, nemůžeš ho okrást!")

		if chance>=5:
			stolen = random.randrange(0,int(0.2*acc["amount"]),10)
			if acc["amount"]-stolen<0:
				stolen = acc["amount"]
			if acc["amount"]<=0:
				return await self.bot.say("Přece bys neokradl někoho kdo nemá ani na sušenku, že ne?") 
			self.d[guild].update_one({"name":str(user)},{"$set":{"amount":acc["amount"]-stolen}})
			self.d[guild].update_one({"name":str(ctx.message.author)},{"$set":{"amount":aut["amount"]+stolen}})
			await ctx.channel.send(f"{ctx.message.author.display_name} ukradl {user.display_name} {stolen}:dollar:!")
		else:
			stolen = random.randrange(int(0.005*aut["amount"]),int(0.1*aut["amount"]))
			self.d[guild].update_one({"name":str(ctx.message.author)},{"$set":{"amount":aut["amount"]-stolen}})
			await ctx.channel.send(f":oncoming_police_car:{ctx.message.author.display_name} načapala policie při činu! Pokuta činí {stolen} šekelů")

	@commands.command(pass_context = True,no_pm=True,aliases=["roulete","ruleta"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def automat(self,ctx,mlt,amount):
		await ctx.channel.trigger_typing()
		try:
			mlt = float(mlt)
			amount = int(amount)
		except:
			return await ctx.channel.send("Jedna z hodnot je špatně!")		
		if mlt<=1:
			return ctx.channel.send("Násobitel musí být větší než jedna!")
		chance = 1/mlt
		guild = str(ctx.message.guild.id)
		a = self.d[guild].find_one({"name":str(ctx.message.author)})
		if a is None:
			return await ctx.channel.send("Ještě sis nezaložil účet!")
		if a["amount"]<amount:
			return await ctx.channel.send("Chtěl si vsadit víc peněz než máš na účtě!")
		if random.random() > chance:
			self.d[guild].update_one({"name":str(ctx.message.author)},{"$set":{"amount":a["amount"]-amount}})
			return await ctx.channel.send(f"`{ctx.message.author.display_name} prohrál {float(amount)} šekelů!`")
		won = mlt*amount
		self.d[guild].update_one({"name":str(ctx.message.author)},{"$set":{"amount":a["amount"]+won}})
		await ctx.channel.send(f"`{ctx.message.author.display_name} vyhrál v automatu {won} šekelů!`")
	
	@commands.command(pass_context = True,no_pm=True,aliases=["biz"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def business(self,ctx):
		await ctx.channel.trigger_typing()
		point = self.col.biz.bizdb.find({})
		e=discord.Embed(colour=discord.Colour.green())
		for doc in point:
			e.add_field(name=doc["name"],value=f'id: {doc["id"]}\ncena: {self.parser(str(doc["price"]))}:dollar:\n{doc["des"]}',inline=False)
		e.set_author(name="Byznys")
		e.set_footer(text="Byznys si koupíš pomocí §buy <id>")
		await ctx.channel.send(embed=e)
	
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
		await ctx.channel.trigger_typing()
		guild = str(ctx.message.guild.id)
		if bizid==0:
			return await ctx.channel.send("Neřekl jsi, co si chceš koupit!")
		elif bizid<1:
			return await ctx.channel.send("ID musí být větší než nula")
		biz = self.col.biz.bizdb.find_one({"id":bizid})
		if biz is None:
			return await ctx.channel.send("Tento byznys neexistuje!")
		a = self.d[guild].find_one({"name":str(ctx.message.author)})
		if a is None:
			return await ctx.channel.send("Ještě sis nezaložil účet!")
		elif biz["price"]>a["amount"]:
			return await ctx.channel.send("Na tento byznys nemáš peníze!")
		self.d[guild].update_one({"name":str(ctx.message.author)},{"$push":{"bizs":bizid}})
		a = self.d[guild].find_one({"name":str(ctx.message.author)})
		upers = await self.getpers(a)																							
		if "last_check" not in a:
			self.d[guild].update_one({"name":str(ctx.message.author)},{"$set":{"amount":a["amount"]-float(biz["price"]),"pers":upers,"last_check":datetime.datetime.utcnow()}})
		else:
			self.d[guild].update_one({"name":str(ctx.message.author)},{"$set":{"amount":a["amount"]-float(biz["price"]),"pers":upers}})
		await ctx.channel.send(f"Úspěšně sis koupil předmět {biz['name']}!")

	@commands.command(pass_context = True,no_pm=True,aliases=["inventář"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def inventory(self,ctx,user:discord.Member=None):
		await ctx.channel.trigger_typing()
		guild = str(ctx.message.guild.id)
		if user is None:
			user=ctx.message.author
		a = self.d[guild].find_one({"name":str(user)})
		if a is None:
			return await ctx.channel.send(f"{user.display_name} si ještě nezaložil účet")
		if "bizs" not in a:
			return await ctx.channel.send(f"{user.display_name} si ještě nic nekoupil!")
		counted=Counter(a["bizs"])
		e=discord.Embed(colour=discord.Colour.green())
		for biz,num in counted.items():
			biz=self.col.biz.bizdb.find_one({"id":biz})
			e.add_field(name=biz["name"],value=f"{num} krát\nVydělává {round(num*biz['pers'],2)} za vteřinu",inline = False)
		e.set_author(name=user.display_name,icon_url=user.avatar_url)
		await ctx.channel.send(embed=e)

	@commands.command(pass_context = True,no_pm=True,aliases=["stopsteal"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def ochrana(self,ctx):
		await ctx.channel.trigger_typing()
		guild = str(ctx.message.guild.id)
		user=ctx.message.author
		a = self.d[guild].find_one({"name":str(user)})
		if a is None:
			return await ctx.channel.send(f"{user.display_name} ještě sis nezaložil účet")
		#if "protects" not in a:
		#	self.d[guild].update_one({"name":str(user)},{"$push":{"protects":1}})
		#price = 20000*(a["protects"]*1.5)
		#if a["amount"] < price:
		#	return await ctx.channel.send(f"Potřebuješ {price} peněz, a to jaksi nemáš :/")
		if a["amount"] > 10000000:
			return await ctx.channel.send("Už máš moc peněz, nějaká krádež ti neuškodí ;)")
		price = 0.3*a["amount"]
		if "protection" in a:
			if (datetime.datetime.now()-a["protection"]).days < 1:
				return await ctx.channel.send("Ochranu už máš")
		self.d[guild].update_one({"name":str(user)},{"$inc":{"amount":-price},"$set":{"protection":datetime.datetime.now()}})
		return await ctx.channel.send(f"Úspěšně sis aktivoval ochranu na 24 hodin za {price} penízků!")		

def setup(bot):
	bot.add_cog(Economy(bot))
