import json
import random
import vtipek
import discord
import requests
import eightballer
import urllib.request
from io import BytesIO
from bs4 import BeautifulSoup
from unidecode import unidecode
from discord.ext import commands
from discord.ext.commands import has_permissions

class Fun(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command(pass_context = True,no_pm=True,aliases=['clean','delete','smaz','ocista'])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	@has_permissions(manage_messages=True)
	async def purge(self,ctx, number):	
		await ctx.channel.trigger_typing()
		mgs = [] #Empty list to put all the messages in the log
		number = int(number) #Converting the amount of messages to delete to an integer
		if number > 100:
			return await ctx.channel.send('V klidu s tou čistkou, limit je 100 zpráv')
		if number!=100:
			number+=1
		async for x in ctx.channel.history(limit = number):
			mgs.append(x)
		await ctx.channel.delete_messages(mgs)
		await ctx.channel.send(":put_litter_in_its_place: x"+str(number))

	@purge.error
	async def setuperror(self,error,ctx):
		if isinstance(error, MissingPermissions):
			await ctx.channel.send(ctx.message.channel, "Na tento příkaz nemáš oprávnění (správa zpráv)")

	@commands.command(pass_context=True)
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def kdojsem(self,ctx, member: discord.Member = None):
		author = ctx.message.author
		msg = "Jsi "+str(author)
		await ctx.channel.send(msg)
	
	@commands.command(pass_context=True, aliases = ["8ball","magickakoule","choose"])
	@commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
	async def eightball(self,ctx):
		msg = eightballer.eightball_pick()
		await ctx.channel.send(msg)
	@commands.command(pass_context=True)
	@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
	async def vtip(self,ctx):
		msg = vtipek.vtipek()
		await ctx.channel.send("`"+msg+"`")
	@commands.command(pass_context=True)
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def fakt(self,ctx):
		url = "http://www.faktomat.cz/fakty/nahodne"
		r = urllib.request.urlopen(url)
		soup = BeautifulSoup(r,'html.parser')
		result = soup.find("div", {"class":"lead"}).text
		await ctx.channel.send(f"`{result}`")
	@commands.command(pass_context=True,no_pm=True)
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def avatar(self,ctx,*,user:discord.Member = None):
		if user is None:
			user = ctx.message.author
		await ctx.channel.send(f" **{user.name}**\n{user.avatar_url}")

	@commands.command(pass_context = True,no_pm=True,aliases=["server"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def guild(self, ctx):
		""" Check info about current guild """
		if ctx.invoked_subcommand is None:
			findbots = sum(1 for member in ctx.message.guild.members if member.bot)

			embed = discord.Embed(colour = discord.Colour.blue())
			embed.set_thumbnail(url=ctx.message.guild.icon_url)
			embed.add_field(name="Název serveru", value=ctx.message.guild.name, inline=True)
			embed.add_field(name="ID", value=ctx.message.guild.id, inline=True)
			embed.add_field(name="Počet členů", value=ctx.message.guild.member_count, inline=True)
			embed.add_field(name="Z toho boti", value=findbots, inline=True)
			embed.add_field(name="Majitel", value=ctx.message.guild.owner, inline=True)
			embed.add_field(name="Region", value=ctx.message.guild.region, inline=True)
			embed.add_field(name="Vytvořeno", value= ctx.message.guild.created_at, inline=True)
		await ctx.channel.send(content=f"Něco málo o  **{ctx.message.guild.name}**", embed=embed)
	
	async def randomimageapi(self, ctx, url, endpoint):
		try:
			r = requests.get(url)
			r=r.json()
		except json.JSONDecodeError:
			return await ctx.channel.send("Chybička se vloudila")
		await ctx.channel.send(r[endpoint])
	
	@commands.command(pass_context = True, aliases = ["kocka","kotatko","catto"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def cat(self, ctx):
		""" Posts a random cat """
		await self.randomimageapi(ctx, 'https://nekos.life/api/v2/img/meow', 'url')

	@commands.command(pass_context = True, aliases = ["pes","pejsek","stenatko","doggo"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def dog(self, ctx):
		""" Posts a random dog """
		await self.randomimageapi(ctx, 'https://random.dog/woof.json', 'url')

	@commands.command(pass_context = True, aliases = ["kachna","kachnatko"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def duck(self, ctx):
		""" Posts a random duck """
		await self.randomimageapi(ctx, 'https://random-d.uk/api/v1/random', 'url')
	@commands.command(pass_context=True)
	async def dong(self):
		with open("dongs.txt",'r') as file:
			links = json.load(file)
			dong = random.choice(links)
			dong = dong.strip("'")
			await ctx.channel.send(dong)
	
	@commands.command(pass_context=True,aliases=["nahodnecislo","nahodne","random"])
	@commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
	async def randint(self,ctx,top):
		try:
			top = int(top)
		except:
			return await ctx.channel.send("S číslem je nějaká chyba...")
		if top>100000:
			return await ctx.channel.send("Horní limit je příliš velký, maximum je 100 000")
		chosen = random.randrange(0,top)
		await ctx.channel.send(f"`{chosen}`")

	@commands.command(pass_context = True,aliases=["pero","ukazmipero","dick","ukažmipéro"])
	@commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
	async def penis(self,ctx,user:discord.Member = None):
		if user is None:
			user = ctx.message.author
		e=discord.Embed(colour=random.randint(0, 0xFFFFFF))
		e.set_author(name="Pindik")
		e.add_field(name=f"Tímto se může chlubit {str(user)[:-5]}:",value="8"+'='*random.randrange(0,10)+"D")
		await ctx.channel.send(embed=e)
	
	@commands.command(pass_context= True,aliases=["detektor","lez","lež"])
	@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
	async def detektorlzi(self,ctx,user:discord.Member = None):
		prvni = False
		if user is None:
			user = ctx.message.author
			prvni = True
		possible_prvni = ["Lžeš","Podle mě lžeš","Pravda zní jinak...","Ty jsi nikdy nemluvil nic jiného než pravdu :slight_smile:","Máš pravdu","Ačkoliv to nerad uznávám, máš pravdu"]
		possbile_ostatni = [f"{user.display_name} lže",f"{user.display_name} lže, jako když tiskne",f"{ctx.message.author.display_name} má pravdu, {user.display_name} nikoliv",f"{user.display_name} má pravdu, {ctx.message.author.display_name} nikoliv",f"{user.display_name} vždy mluvil pravdu"]
		if prvni:
			msg = random.choice(possible_prvni)
		else:
			msg = random.choice(possbile_ostatni)
		await ctx.channel.send(f"`{msg}`")

	@commands.command(pass_context= True,aliases=["láska","<3","luv"])
	@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
	async def love(self,ctx,fuser:discord.Member=None,suser:discord.Member=None):
		if fuser is None and suser is None:
			return await ctx.channel.send("Nikoho jsi neoznačil!")
		elif suser is None:
			suser = ctx.message.author
		url = "https://www.lovecalculator.com/love.php?"
		fuser_was,suser_was=fuser.display_name,suser.display_name
		fuser,suser = unidecode(fuser.display_name.replace(" ","+")),unidecode(suser.display_name.replace(" ","+"))
		url = url+f"name1={fuser}&name2={suser}"
		r = urllib.request.urlopen(url)
		soup = BeautifulSoup(r,'html.parser')
		result = soup.find("div", {"class":"result score"}).text
		await ctx.channel.send(f"{fuser_was} a {suser_was} spolu mají šanci `{result}`:heart:")
	
	@commands.group(pass_context= True,aliases=["svátek"])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def svatek(self,ctx):
		if ctx.invoked_subcommand is None:
			r = requests.get("https://api.abalin.net/get/today").json()
			svatek_cz = r["data"]["name_cz"]
			svatek_sk = r["data"]["name_sk"]
			await ctx.channel.send(f"Dnes má svátek `{svatek_cz}` a na Slovensku `{svatek_sk}` :ribbon:")
			
	@svatek.command(aliases=["zítra"])
	async def zitra(self):
		r = requests.get("https://api.abalin.net/get/tomorrow").json()
		svatek_cz = r["data"]["name_cz"]
		svatek_sk = r["data"]["name_sk"]
		await ctx.channel.send(f"Zítra má svátek `{svatek_cz}` a na Slovensku `{svatek_sk}`:ribbon:")

def setup(bot):
	bot.add_cog(Fun(bot))
