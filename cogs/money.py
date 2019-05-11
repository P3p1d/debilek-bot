import json
import discord
import requests
import urllib.request
from discord.ext import commands
url = "https://api.coinmarketcap.com/v2/listings/"
url_logo = "https://raw.githubusercontent.com/dziungles/cryptocurrency-logos/master/coins/32x32/"
class Money(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
	@commands.command(pass_context = True, aliases = ["monies","penizky","crypto","krypto","mny"])
	#@commands.cooldown(rate=1, per=20, type=commands.BucketType.user)
	async def money(self,ctx,coin):
		try:
			r = requests.get(url)
			r=r.json()
			for crypto in r['data']:
				if (crypto['name'] == coin) or (crypto['id'] == coin) or (crypto['website_slug'] == coin) or (crypto['symbol'] == coin):
					url_speci = "https://api.coinmarketcap.com/v2/ticker/"
					url_speci = url_speci + str(crypto['id']) + '/'
					r = requests.get(url_speci)
					r = r.json()
					crypto = r["data"]
					e = discord.Embed(colour = discord.Colour.blue())
					e.set_author(name = crypto['name'])
					e.set_thumbnail(url = url_logo+crypto['website_slug']+'.png')
					e.add_field(name='Symbol',value = crypto['symbol'],inline = True)
					e.add_field(name='ID',value=crypto['id'],inline = True)
					e.add_field(name='V oběhu',value = crypto['circulating_supply'],inline=True)
					e.add_field(name='Cena USD',value = crypto["quotes"]["USD"]["price"], inline = True)
					e.add_field(name='Změna za 1h',value = str(crypto["quotes"]["USD"]["percent_change_1h"])+'%', inline = True)
					e.add_field(name='Změna za 24h',value = str(crypto["quotes"]["USD"]["percent_change_24h"])+'%', inline = True)
					e.set_footer(text="Data poskytuje coinmarketcap.com")
					return await ctx.channel.send(embed=e)
		except json.JSONDecodeError:
			return await ctx.channel.send("Chybička se vloudila")
def setup(bot):
	bot.add_cog(Money(bot))
