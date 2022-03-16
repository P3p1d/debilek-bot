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
		self.col=MongoClient(os.environ["MONGOURI"])
		self.d=self.col.debilek
	
	def parser(self,x):
		i = -3
		fmtd = ""
		x= str(x)
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

		acc = self.d.users.find_one({"_id":user.id})
		if acc is None:
			self.d.users.insert_one({"_id":user.id,"amount":500,"date_registered":datetime.datetime.utcnow(),"bizs":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]})
			return await ctx.channel.send(f"`Účet pro {user.display_name} byl založen!`")

		if "pers" in acc:
			t = (datetime.datetime.utcnow()-acc["last_check"]).total_seconds()
			acc["amount"] += t*acc["pers"]
			self.d.users.update_one({"_id":user.id},{"$set":{"last_check":datetime.datetime.utcnow(),"amount":acc["amount"]}})
			if acc['amount'] >= 10000:
				val = self.parser(str(int(acc['amount'])))
			else:
				val=round(acc['amount'],2)
			return await ctx.channel.send(f"`{user.display_name} má na účtě {val} penízků a vydělává {round(acc['pers'],2)} za vteřinu`")
		return await ctx.channel.send(f"`{user.display_name} má na účtě {acc['amount']} penízků`")
	'''
	@commands.command(pass_context = True,no_pm=True,aliases=["thief","kradez"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def steal(self,ctx,user:discord.Member=None):
		await ctx.channel.trigger_typing()
		if user is None:
			return await ctx.channel.send("A koho chceš teda okrást?")
		if user == str(ctx.message.author):
			return await ctx.channel.send("Proč by jsi okrádal sám sebe?")
		
		chance = random.randint(0,10)
		acc = self.d.users.find_one({"_id":user.id})
		aut=self.d.users.find_one({"_id":ctx.message.author.id})
		if acc is None or aut is None:
			return await ctx.channel.send("Jeden z vás si ještě nezaložil účet")

		if "protection" in acc:
			if (datetime.datetime.now()-acc["protection"]).days < 1:
				return await ctx.channel.send(f"{user.display_name} má zapnutou ochranu, nemůžeš ho okrást!")

		if chance>=5:
			stolen = random.randrange(0,int(0.2*acc["amount"]),10)
			if stolen > (2*aut["amount"]):
				stolen = (2*aut["amount"])     #maximalne ukradne dvojnasobek zlodejovo jmeni

			if acc["amount"]-stolen<0:
				stolen = acc["amount"]
			if acc["amount"]<=0:
				return await self.bot.say("Přece bys neokradl někoho kdo nemá ani na sušenku, že ne?") 
			self.d.users.update_one({"_id":user.id},{"$set":{"amount":acc["amount"]-stolen}})
			self.d.users.update_one({"_id":ctx.message.author.id},{"$set":{"amount":aut["amount"]+stolen}})
			await ctx.channel.send(f"{ctx.message.author.display_name} ukradl {user.display_name} {stolen}:dollar:!")
		else:
			stolen = random.randrange(int(0.005*aut["amount"]),int(0.1*aut["amount"]))
			self.d.users.update_one({"_id":ctx.message.author.id},{"$set":{"amount":aut["amount"]-stolen}})
			await ctx.channel.send(f":oncoming_police_car:{ctx.message.author.display_name} načapala policie při činu! Pokuta činí {stolen} šekelů")
	'''
	@commands.command(pass_context = True,no_pm=True,aliases=["roulete","ruleta"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def automat(self,ctx,mlt,amount):
		await ctx.channel.trigger_typing()
		try:
			mlt = float(mlt)
			amount = int(amount)
		except:
			return await ctx.channel.send("Jedna z hodnot je špatně!")		
		if mlt<2:
			return await ctx.channel.send("Násobitel musí být větší než dva!")
		chance = 1/mlt
		
		a = self.d.users.find_one({"_id":ctx.message.author.id})
		if a is None:
			return await ctx.channel.send("Ještě sis nezaložil účet!")
		if a["amount"]<amount:
			return await ctx.channel.send("Chtěl si vsadit víc peněz než máš na účtě!")
		if random.random() > chance:
			self.d.users.update_one({"_id":ctx.message.author.id},{"$set":{"amount":a["amount"]-amount}})
			return await ctx.channel.send(f"`{ctx.message.author.display_name} prohrál {float(amount)} šekelů!`")
		won = mlt*amount
		self.d.users.update_one({"_id":ctx.message.author.id},{"$set":{"amount":a["amount"]+won}})
		await ctx.channel.send(f"`{ctx.message.author.display_name} vyhrál v automatu {won} šekelů!`")

	@commands.command(pass_context = True,no_pm=True,aliases=["biz"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def business(self,ctx):
		await ctx.channel.trigger_typing()
		point = self.col.biz.bizdb.find({})
		point = sorted(point,key=lambda i: i["id"])    #seradit podle id

		e=discord.Embed(colour=discord.Colour.green())
		for doc in point:
			e.add_field(name=doc["name"],value=f'id: {doc["id"]}\ncena: {self.parser(str(doc["price"]))}:dollar:\n{doc["des"]}',inline=False)
		e.set_author(name="Byznys")
		e.set_footer(text="Byznys si koupíš pomocí §buy <id>")
		await ctx.channel.send(embed=e)
	
	async def getpers(self,a):
		val = 0
		i = 1
		for bizid in a["bizs"]:
			try:
				count=a["bizs"][i]
			except IndexError:
				break

			if count is None:
				count = 0
			biz=self.col.biz.bizdb.find_one({"id":i})

			val+=biz["pers"]*count
			i+=1
		return val
	
	@commands.command(pass_context = True,no_pm=True)
	@commands.cooldown(rate=2, per=5, type=commands.BucketType.user)
	async def buy(self,ctx,bizid:int=0,amount_to_buy:int=1):
		await ctx.channel.trigger_typing()

		if bizid==0:
			return await ctx.channel.send("Neřekl jsi, co si chceš koupit!")
		elif bizid<1:
			return await ctx.channel.send("ID musí být větší než nula")
		elif amount_to_buy<1:
			return await ctx.channel.send("Nemůžeš si koupit méně jak jeden kus")

		biz = self.col.biz.bizdb.find_one({"id":bizid})
		if biz is None:
			return await ctx.channel.send("Tento byznys neexistuje!")
		a = self.d.users.find_one({"_id":ctx.message.author.id})
		if a is None:
			return await ctx.channel.send("Ještě sis nezaložil účet!")
		elif (biz["price"]*amount_to_buy)>a["amount"]:
			return await ctx.channel.send("Na tento byznys nemáš peníze!")

		try:
			if a["bizs"][bizid] is None:
				a["bizs"]
			if (a["bizs"][bizid] + amount_to_buy) > 1000:
				return await ctx.channel.send("Už bys měl moc byznysů tohoto typu (maximum je 1000)!")
			self.d.users.update_one({"_id":ctx.message.author.id},{"$inc":{f"bizs.{str(bizid)}":amount_to_buy}})	
		
		except IndexError:
			self.d.users.update_one({"_id":ctx.message.author.id},{"$set":{f"bizs.{str(bizid)}":amount_to_buy}})		


		upers = biz["pers"]	* amount_to_buy																						
		if "last_check" not in a:
			self.d.users.update_one({"_id":ctx.message.author.id},{"$set":{"amount":a["amount"]-float(biz["price"]*amount_to_buy),"last_check":datetime.datetime.utcnow()},"$inc":{"pers":upers}})
		else:
			self.d.users.update_one({"_id":ctx.message.author.id},{"$set":{"amount":a["amount"]-float(biz["price"]*amount_to_buy)},"$inc":{"pers":upers}})
		await ctx.channel.send(f"Úspěšně sis koupil {amount_to_buy}x předmět {biz['name']}!")

	@commands.command(pass_context = True,no_pm=True,aliases=["inventář"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def inventory(self,ctx,user:discord.Member=None):
		await ctx.channel.trigger_typing()
		
		if user is None:
			user=ctx.message.author
		a = self.d.users.find_one({"_id":user.id})
		if a is None:
			return await ctx.channel.send(f"{user.display_name} si ještě nezaložil účet")
		if "bizs" not in a:
			return await ctx.channel.send(f"{user.display_name} si ještě nic nekoupil!")
		
		e=discord.Embed(colour=discord.Colour.green())

		i=1
		for biz_id in a["bizs"][1:]:		#preskoci prvni

			if biz_id is None:
				biz_id = 0
				
			biz=self.col.biz.bizdb.find_one({"id":i})

			e.add_field(name=biz["name"],value=f"{biz_id} krát\nVydělává {round(biz_id*biz['pers'],2)} za vteřinu",inline = False)
			i+=1
		e.set_author(name=user.display_name,icon_url=user.avatar_url)
		await ctx.channel.send(embed=e)	

	"""
	@commands.command(pass_context = True,no_pm=True,aliases=["stopsteal"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def ochrana(self,ctx):
		await ctx.channel.trigger_typing()
		
		user=ctx.message.author
		a = self.d.users.find_one({"_id":user.id})
		if a is None:
			return await ctx.channel.send(f"{user.display_name} ještě sis nezaložil účet")
		
		price = 0.3*a["amount"]
		if "protection" in a:
			if (datetime.datetime.now()-a["protection"]).days < 1:
				return await ctx.channel.send("Ochranu už máš")
		self.d.users.update_one({"_id":user.id},{"$inc":{"amount":-price},"$set":{"protection":datetime.datetime.now()}})
		return await ctx.channel.send(f"Úspěšně sis aktivoval ochranu na 24 hodin za {price} penízků!")		
	"""
	
	@commands.command(pass_context = True,no_pm=True,aliases=["posli","zaplat"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def pay(self,ctx,amount:int,user:discord.Member=None):				
		if user is None:
			return await ctx.channel.send("Nikoho jsi neoznačil!")
		try:
			amount = float(amount)
		except Exception as e:
			return await ctx.channel.send("Při převodu hodnoty se vyskytla chbya, možná si zadal nějaké postižené číslo...")
		if amount is None or amount <= 0:
			return await ctx.channel.send("Hodnota peněz musí být větší než nula!")		

		a = self.d.users.find_one({"_id":ctx.message.author.id})
		u = self.d.users.find_one({"_id":user.id})
		if a is None or u is None:
			return await ctx.channel.send("Jeden z vás si ještě nezaložil účet!")
		if a["amount"]<amount:
			return await ctx.channel.send("Chtěl jsi poslat víc než máš na účtě!")

		self.d.users.update_one({"_id":ctx.message.author.id},{"$inc":{"amount":-float(amount)}})
		self.d.users.update_one({"_id":user.id},{"$inc":{"amount":amount}})
		return await ctx.channel.send(f"Úspěšně jsi poslal {user.display_name} {amount} penízků!")

	@commands.command(pass_context = True,no_pm=True,aliases=["dennivyplata"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def daily(self,ctx):

		a = self.d.users.find_one({"_id":ctx.message.author.id})
		if a is None:
			return await ctx.channel.send("Ještě sis nezaložil účet")

		reward = 1000
		if reward > a["amount"]:
			reward = 1.05*a["amount"]

		if "last_daily" not in a:
			self.d.users.update_one({"_id":ctx.message.author.id},{"$set":{"last_daily":datetime.datetime.utcnow()},"$inc":{"amount":reward}})
			return await ctx.channel.send(f"Dostal jsi svůj denní příděl {reward} penízků!")

		time_difference = datetime.datetime.utcnow()-a["last_daily"]

		if int(time_difference.days) >= 1:
			self.d.users.update_one({"_id":ctx.message.author.id},{"$set":{"last_daily":datetime.datetime.utcnow()},"$inc":{"amount":reward}})
			return await ctx.channel.send(f"Dostal jsi svůj denní příděl {self.parser(reward)} penízků!")
		else:
			return await ctx.channel.send(f"Ještě musíš {24-(time_difference.seconds//3600)} hodin počkat!")

	"""
	@commands.group(pass_context = True,no_pm=True,aliases=["kup"])
	@commands.cooldown(rate=2, per=5, type=commands.BucketType.user)		
	async def gpu(self,ctx):

		a = self.d.users.find_one({"_id":ctx.message.author.id})

	@gpu.command(pass_context=True,no_pm=True)
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def buygpu(self,ctx):

		a = self.d.users.find_one({"_id":ctx.message.author.id})
		if a is None: 
			return await ctx.channel.send("Nemáš založený účet!")

	"""

def setup(bot):
	bot.add_cog(Economy(bot))	
