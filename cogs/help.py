import discord
from discord.ext import commands
class Help():
	"""docstring for Help"""
	def __init__(self, bot):
		self.bot = bot
	@commands.command(pass_context = True,aliases = ['pomoc','prikazy',''])
	async def help(self,ctx):
		"""author = ctx.message.author
		em=discord.Embed(
			description='Seznam a popis všech možných příkazů Debílka', colour = discord.Colour.green()
			)
		em.set_author(name="Příkazy")
		em.add_field(name = "!say", value = "Bot odpoví obsahem zprávy",inline = False)
		em.add_field(name = "!eightball", value = "Bot napíše náhodnou odpověď z magické koule :8ball:",inline = False)
		em.add_field(name = "!vtip", value = "Odešle náhodný vtip z internetu",inline = False)
		em.add_field(name = "!meme", value = "Kradené memečka z Imguru jsou nejlepší memečka",inline = False)
		em.add_field(name = "!fakt", value = "Odešle náhodný fakt z databáze",inline = False)
		em.add_field(name = "!ping", value = "Odpoví přibližným pingem mezi serverem discordu a botem",inline = False)
		em.add_field(name = "!kdojsem", value = "Vypíše autorovo jméno a id. Skvělé pro existenční krizi",inline = False)
		em.add_field(name = "!play (hraj)", value = "Bot se připojí do kanálu autora a začne přehrávát audio z YouTube odkazu; např !yt https://www.youtube.com/watch?v=DLzxrzFCyOs",inline = False)
		em.add_field(name = "!stop", value = "Vypne přehrávání hudby a odpojí bota z hlasového kanálů",inline = False)
		em.add_field(name = "!pause (pauza)", value = "Pozastaví přehrávání hudby",inline = False)
		em.add_field(name = "!resume (pokracuj)", value = "Pokračuje v přehrávání hudby",inline = False)
		em.add_field(name = "!queue (fronta)", value = "Zobrazí písničky ve frontě",inline = False)
		em.add_field(name = "!skip (next, dalsi)", value = "Pozastaví přehrávání a začne hrát další audio ve frontě (pokud jste písničku přidali vy, jinak začne hlasování",inline = False)
		em.add_field(name = "!avatar", value = "Pošle avatar (profilovku) označeného člověka. Pokud nikdo označený není, odešle avatar autora zprávy",inline = False)
		em.add_field(name = "!cat (kocka,kotatko,catto)", value = "Pošle náhodnou fotky kočky/kocoura/koťátka. Aby nedošlo k příliš velké roztomilosti tak je na příkaz 5 vteřin cooldown",inline = False)
		em.add_field(name = "!dog (pes,pejsek,stenatko,doggo)", value = "To samé, ale s pejsky",inline = False)
		em.add_field(name = "!duck (kachna,kachnatko)", value = "A nakonec, kachny",inline = False)
		em.add_field(name = "!server", value = "Odešle embed s informacemi o discord serveru, na kterém je bot právě používán",inline = False)
		em.add_field(name = "!purge (ocista,clean,delete,smaz)", value = "Smaže zadaný počet zpráv (0-100). je potřeba mít oprávnění k správě zpráv",inline = False)
		em.add_field(name = "!money (crypto,krypto,monies,penizky,mny)", value = "Sledujte jak padá Bitcoin přímo na discordu! K příkazu je nutné dodat jakou kryptoměnu chcete vidět (jméno,zkratka anebo id). Data poskytuje coinmarketcap.com",inline = False)
		em.add_field(name = "!economy (€)", value = "Založí ti účet v židovské bance a zobrazí tvojí bilanci",inline = False)
		em.add_field(name = "!daily", value = "Tvůj denní příděl 500 šekelů",inline = False)
		em.add_field(name = "!steal", value = "Pokus své štěstí proti ruce zákona! Zkus ukradnout označenému uživateli peníze, ale pozor, policie vše bedlivě hlídá a může ti dát tučnou pokutu",inline = False)
		em.add_field(name = "!cookie", value = "Omluv se svému příteli za krádež tím, že mu pošleš sušenku. Jedna sušenka stojí 10 šekelů",inline = False)
		await self.bot.say("Koukni se do DMs :wink:") 
		await self.bot.send_message(author,embed=em) """
		await ctx.channel.send("https://debilekbot.glitch.me/") 
def setup(bot):
	bot.add_cog(Help(bot))