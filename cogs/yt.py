import discord
import youtube_dl
from datetime import timedelta
from discord.ext import commands
players = {}
queued = {}
vid_infos = {}
ytdl_opts ={'ignoreerrors' : True, 'quiet' : True,}
volume = 0.5
# TODO: obsolete
class YT:
	def __init__(self,bot):
		self.bot = bot

	@commands.command(pass_context=True, aliases=["play", "hraj"])
	async def yt(self,ctx, url, member: discord.Member = None):
		server = ctx.message.server
		author = ctx.message.author
		voice_client = self.bot.voice_client_in(server)
		vc = await self.bot.join_voice_channel(author.voice_channel)
		msg = "Stahuji audio..."
		msg = await self.bot.say(msg)
		player = await vc.create_ytdl_player(url,after = lambda: checkqueue(server.id))
		await self.bot.edit_message(msg, new_content="Hotovo!")
		players[server.id] = player
		vid_infos[player.url] = {'name':player.title,'duration':player.duration,'rating':int(player.likes/((player.likes+player.dislikes)/100))}
		player.volume = volume
		player.start()
	@commands.command(pass_context=True, aliases=["disconnect", "pryc", "stop"])
	async def leave(self,ctx, member: discord.Member = None):
		msg = await self.bot.say("Opouštím kanál")
		for x in self.bot.voice_clients:
			if(x.server == ctx.message.server):
				return await x.disconnect()
		await self.bot.delete_message(msg)

	@commands.command(pass_context=True, aliases=["pauza"])
	async def pause(self,ctx):
		my_id = ctx.message.server.id
		players[my_id].pause()

	@commands.command(pass_context=True, aliases=["pokracuj"])
	async def resume(self,ctx):
		my_id = ctx.message.server.id
		players[my_id].resume()

	def checkqueue(my_id):
		if queued[my_id] != []:
			player = queued[my_id].pop(0)
			players[my_id] = player
			player.start()
			del vid_infos[player.url]
	@commands.command(pass_context=True, aliases = ["dofronty","add"]) #, aliases=["fronta"])
	async def queue(self,ctx, url):
		if url in vid_infos:
			await self.bot.say('Tato písnička už je ve frontě!')
			return
		voice_client = self.bot.voice_client_in(ctx.message.server)
		player = await voice_client.create_ytdl_player(url,ytdl_options= ytdl_opts, after = lambda: checkqueue(ctx.message.server.id))
		player.volume = volume
		vid_infos[player.url] = {'name':player.title,'duration':player.duration,'rating':int(player.likes/((player.likes+player.dislikes)/100))}
		if ctx.message.server.id in queued:
			queued[ctx.message.server.id].append(player)
		else:
			queued[ctx.message.server.id] = [player]
		await self.bot.say("Přidáno do fronty :ok_hand:")
	@commands.command(pass_context=True)
	async def skip(self,ctx, aliases=["next","dalsi"]):
		del vid_infos[players[ctx.message.server.id].url]
		players[ctx.message.server.id].stop()
		player = queued[ctx.message.server.id].pop(0)
		players[ctx.message.server.id] = player		
		player.volume = volume
		player.start()

	@commands.command(pass_context = True)
	async def fronta(self,ctx):
		for x in self.bot.voice_clients:
			if(x.server == ctx.message.server):
				print(x.channel.voice_members)
		e = discord.Embed(colour = discord.Colour.red())
		for vid in vid_infos:
			d = timedelta(seconds = vid_infos[vid]['duration'])
			e.add_field(name = vid_infos[vid]['name'],value = str(d),inline = False)
		e.set_author(name='Fronta')
		await self.bot.say(embed = e)
def setup(bot):
	bot.add_cog(YT(bot))