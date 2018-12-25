import os
import discord
import textwrap
import requests
import shutil
from discord.ext import commands
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
class Images:
	def __init__(self,bot):
		self.bot=bot
	async def getimage(self,ctx):
		async for x in self.bot.logs_from(ctx.message.channel, limit = 15):
			if x.attachments != []:
				suffixes = ('.jpeg','.jpg','.png')
				if x.attachments[0]['url'].endswith(suffixes):
					filename = x.attachments[0]['url'].split('/')
					filename = filename[-1]
					response = requests.get(x.attachments[0]['url'], stream=True)
					filename = ctx.message.server.id + filename
					with open(filename, 'wb') as out_file:
						shutil.copyfileobj(response.raw, out_file)
					size=500,500
					im = Image.open(filename)
					width,height = im.size
					if width > 2100 or height > 2100:
						#await self.bot.say("Obrázek je moc velký")
						im.close()
						os.remove(filename)
						del response
						return None
					im.thumbnail(size)
					del response
					return (im,filename)

	@commands.command(pass_context=True,aliases=['df','trojobal','obrazekvtrojobalu','deep-fry','deep_fry'])
	@commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
	async def deepfry(self,ctx,*factor):
		await self.bot.send_typing(ctx.message.channel)
		if len(factor)>0 and len(factor)<2:
			try:
				factor=float(factor[0])
			except:
				await self.bot.say("To as není úplně číslo, co?")
				return
		if factor == ():
			factor = 7.0
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await self.bot.say("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		im = im.convert(mode="RGB")
		im = ImageEnhance.Color(im).enhance(factor/2)
		im = ImageEnhance.Sharpness(im).enhance(factor*15)	
		im = ImageEnhance.Contrast(im).enhance(factor*1.5)					
		im.save(filename,"JPEG",quality = 4)
		await self.bot.send_file(ctx.message.channel,filename)
		os.remove(filename)		

	@commands.command(pass_context=True,aliases=['impact','impactmeme','impakt','memetext','txt'])
	@commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
	async def text(self,ctx,*text):
		await self.bot.send_typing(ctx.message.channel)
		if text == ():
			await self.bot.say("Musíš mi dát nějaký text!")
			return
		text = ' '.join(text)
		para = textwrap.wrap(text, width=15)
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await self.bot.say("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")

		width, height = im.size
		draw = ImageDraw.Draw(im)					
		fnt = ImageFont.truetype("./images/extras/impact.ttf", int(height/5))
		current_h, pad = 0,1					
		
		for line in para:
		    w, h = draw.textsize(line, font=fnt)
		    #x = (width - w) / 2
		    draw.text((((width - w) / 2)-2, current_h-2), line, font=fnt,fill="black")
		    draw.text((((width - w) / 2)+2, current_h-2), line, font=fnt,fill="black")
		    draw.text((((width - w) / 2)-2, current_h+2), line, font=fnt,fill="black")
		    draw.text((((width - w) / 2)+2, current_h+2), line, font=fnt,fill="black")
		    draw.text((((width - w) / 2),current_h), line, font=fnt, fill="white")
		    current_h += h + pad	
		im = im.convert(mode="RGB")
		im.save(filename,"JPEG",quality = 90)
		await self.bot.send_file(ctx.message.channel,filename)
		os.remove(filename)

	@commands.command(pass_context=True,aliases=['cz','czflag','cz_flag'])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def czech(self,ctx):
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await self.bot.say("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		im = im.convert(mode="RGB")
		im.thumbnail(size)
		os.chdir('./images')
		cz = Image.open("czech_flag.png")
		cz=cz.resize((im.size)).convert('RGB')
		im=Image.blend(im,cz,0.3)
		
		im.save(filename,"JPEG",quality = 90)
		await self.bot.send_file(ctx.message.channel,filename)
		os.remove(filename)
		os.chdir('..')
		os.remove(filename)					

	@commands.command(pass_context=True,aliases=['otoc'])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def rotate(self,ctx,*angle):
		if angle == ():
			angle = 90
		else:
			angle = int(angle[0])
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await self.bot.say("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		im = im.convert(mode="RGB")
		im.thumbnail(size)
		im = im.rotate(angle,expand=1)
		im.save(filename,"JPEG",quality = 90)
		await self.bot.send_file(ctx.message.channel,filename)
		os.remove(filename)					

	@commands.command(pass_context=True,aliases=['meme1','jetoto','isthis'])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def isthisa(self,ctx,*args):
		await self.bot.send_typing(ctx.message.channel)
		if args == ():
			await self.bot.say("Musíš mi dát nějaký text!")
			return
		text = ' '.join(args)
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await self.bot.say("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		size=200,300

		im.thumbnail(size,Image.ANTIALIAS)
		background = Image.open("./images/extras/meme_template3.jpg").convert('RGBA')
		im=im.convert("RGBA")
		background.paste(im,(650,80),im)
		width,height=background.size
		fnt = ImageFont.truetype("./images/extras/arial.ttf", int(height/15))
		draw = ImageDraw.Draw(background)	
		tw,th=50,700
		draw.text((tw-2, th-2), text, font=fnt,fill="black")
		draw.text((tw+2, th-2), text, font=fnt,fill="black")
		draw.text((tw-2, th+2), text, font=fnt,fill="black")
		draw.text((tw+2, th+2), text, font=fnt,fill="black")
		draw.text((50,700),text, font=fnt,fill="white")
		background =background.convert(mode="RGB")
		background.save(filename,"JPEG",quality = 90)
		await self.bot.send_file(ctx.message.channel,filename)
		os.remove(filename)		

	@commands.command(pass_context=True,aliases=['meme2'])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def phone(self,ctx):
		await self.bot.send_typing(ctx.message.channel)
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await self.bot.say("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		foreground = Image.open("./images/extras/meme_template2.png")
		canvas = Image.new('RGBA', foreground.size, (255,255,255,0))
		im=im.convert('RGBA')
		size=310,580
		#im.thumbnail(size,Image.ANTIALIAS)
		im=im.resize(size,resample=Image.LANCZOS)
		im=im.rotate(-7.8,expand=1)	
		canvas.paste(im,(565,625),im)
		canvas.paste(foreground,(0,0),foreground)		
		canvas=canvas.convert(mode="RGB")	
		canvas.save(filename,"JPEG",quality = 90)
		await self.bot.send_file(ctx.message.channel,filename)
		os.remove(filename)		

	@commands.command(pass_context=True,aliases=['meme3','thatswherethetroublebegan'])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def thatsmile(self,ctx):
		await self.bot.send_typing(ctx.message.channel)
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await self.bot.say("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		background = Image.open("./images/extras/meme_template4.jpg")
		size=246,289
		im=im.resize(size,resample=Image.LANCZOS).convert('RGBA')
		background.paste(im,(251,0),im)
		background.save(filename,"JPEG",quality = 90)
		await self.bot.send_file(ctx.message.channel,filename)
		os.remove(filename)

	@commands.command(pass_context=True,aliases=['meme4'])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def birthcontrol(self,ctx):
		await self.bot.send_typing(ctx.message.channel)
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await self.bot.say("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		background = Image.open("./images/extras/meme_template1.jpg")
		size=200,200
		im=im.resize(size,resample=Image.LANCZOS).convert('RGBA')
		background.paste(im,(480,300),im)
		background.save(filename,"JPEG",quality = 90)
		await self.bot.send_file(ctx.message.channel,filename)
		os.remove(filename)
def setup(bot):
	bot.add_cog(Images(bot))