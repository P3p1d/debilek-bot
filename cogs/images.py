import os
import discord
import textwrap
import requests
import shutil
from discord.ext import commands
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
class Images(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
	async def getimage(self,ctx):
		async for x in ctx.channel.history(limit = 15):
			if x.attachments != []:
				suffixes = ('.jpeg','.jpg','.png')
				if x.attachments[0].url.endswith(suffixes):
					filename = x.attachments[0].url.split('/')
					filename = filename[-1]
					response = requests.get(x.attachments[0].url, stream=True)
					filename = str(ctx.message.guild.id) + filename
					with open(filename, 'wb') as out_file:
						shutil.copyfileobj(response.raw, out_file)
					size=500,500
					im = Image.open(filename)
					width,height = im.size
					if width > 2100 or height > 2100:
						#await ctx.channel.send("Obrázek je moc velký")
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
		await ctx.channel.trigger_typing()
		if len(factor)>0 and len(factor)<2:
			try:
				factor=float(factor[0])
			except:
				await ctx.channel.send("To as není úplně číslo, co?")
				return
		if factor == ():
			factor = 7.0
		try:
			im,filename=await self.getimage(ctx)
		except Exception as e:
			raise e
			return await ctx.channel.send("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		im = im.convert(mode="RGB")
		im = ImageEnhance.Color(im).enhance(factor/2)
		im = ImageEnhance.Sharpness(im).enhance(factor*15)	
		im = ImageEnhance.Contrast(im).enhance(factor*1.5)					
		im.save(filename,"JPEG",quality = 4)
		await ctx.channel.send(file=discord.File(filename))
		os.remove(filename)		

	@commands.command(pass_context=True,aliases=['impact','impactmeme','impakt','memetext','txt'])
	@commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
	async def text(self,ctx,*text):
		await ctx.channel.trigger_typing()
		if text == ():
			await ctx.channel.send("Musíš mi dát nějaký text!")
			return
		text = ' '.join(text)
		para = textwrap.wrap(text, width=15)
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await ctx.channel.send("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")

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
		await ctx.channel.send(file=discord.File(filename))
		os.remove(filename)

	@commands.command(pass_context=True,aliases=['cz','czflag','cz_flag'])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def czech(self,ctx):
		await ctx.channel.trigger_typing()
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await ctx.channel.send("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		im = im.convert(mode="RGB")
		im.thumbnail(size)
		cz = Image.open("./images/czech_flag.png")
		cz=cz.resize((im.size)).convert('RGB')
		im=Image.blend(im,cz,0.3)
		
		im.save(filename,"JPEG",quality = 90)
		await ctx.channel.send(file=discord.File(filename))
		os.remove(filename)
		os.remove(filename)					

	@commands.command(pass_context=True,aliases=['otoc'])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def rotate(self,ctx,*angle):
		await ctx.channel.trigger_typing()
		if angle == ():
			angle = 90
		else:
			angle = int(angle[0])
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await ctx.channel.send("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		im = im.convert(mode="RGB")
		im.thumbnail(size)
		im = im.rotate(angle,expand=1)
		im.save(filename,"JPEG",quality = 90)
		await ctx.channel.send(file=discord.File(filename))
		os.remove(filename)					

	@commands.command(pass_context=True,aliases=['meme1','jetoto','isthis'])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def isthisa(self,ctx,*args):
		await ctx.channel.trigger_typing()
		if args == ():
			await ctx.channel.send("Musíš mi dát nějaký text!")
			return
		text = ' '.join(args)
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await ctx.channel.send("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
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
		await ctx.channel.send(file=discord.File(filename))
		os.remove(filename)		

	@commands.command(pass_context=True,aliases=['meme2'])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def phone(self,ctx):
		await ctx.channel.trigger_typing()
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await ctx.channel.send("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		foreground = Image.open("./images/extras/meme_template2.png")
		canvas = Image.new('RGBA', foreground.size, (255,255,255,0))
		im=im.convert('RGBA')
		size=310,580
		#im.thumbnail(size,Image.ANTIALIAS)
		im=im.resize(size,resample=Image.LANCZOS)
		im=im.rotate(-7.7,expand=1)	
		canvas.paste(im,(565,625),im)
		canvas.paste(foreground,(0,0),foreground)		
		canvas=canvas.convert(mode="RGB")	
		canvas.save(filename,"JPEG",quality = 90)
		await ctx.channel.send(file=discord.File(filename))
		os.remove(filename)		

	@commands.command(pass_context=True,aliases=['meme3','thatswherethetroublebegan'])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def thatsmile(self,ctx):
		await ctx.channel.trigger_typing()
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await ctx.channel.send("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		background = Image.open("./images/extras/meme_template4.jpg")
		size=246,289
		im=im.resize(size,resample=Image.LANCZOS).convert('RGBA')
		background.paste(im,(251,0),im)
		background.save(filename,"JPEG",quality = 90)
		await ctx.channel.send(file=discord.File(filename))
		os.remove(filename)

	@commands.command(pass_context=True,aliases=['meme4'])
	@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
	async def birthcontrol(self,ctx):
		await ctx.channel.trigger_typing()
		try:
			im,filename=await self.getimage(ctx)
		except TypeError:
			return await ctx.channel.send("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		background = Image.open("./images/extras/meme_template1.jpg")
		size=200,200
		im=im.resize(size,resample=Image.LANCZOS).convert('RGBA')
		background.paste(im,(480,300),im)
		background.save(filename,"JPEG",quality = 90)
		await ctx.channel.send(file=discord.File(filename))
		os.remove(filename)
	
	@commands.command(pass_context=True,aliases=['meme5'])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def bart(self,ctx,*text):
		await ctx.channel.trigger_typing()
		if text == ():
			return await ctx.channel.send("Musíš mi dát nějaký text!")
		text=" ".join(text)
		if len(text)>25:
			return await ctx.channel.send("Text je příliš dlouhý, maximum je 25 písmen.")
		im=Image.open("./images/extras/meme_template5.jpg")
		filename=f"bart{ctx.message.guild.id}.jpg"
		width,height=im.size
		fnt = ImageFont.truetype("./images/extras/arial.ttf", int(height/28))
		draw = ImageDraw.Draw(im)
		w, h = draw.textsize(text, font=fnt)
		tw,th=width-w,860
		draw.text(((tw/2)-2,th-2), text, font=fnt,fill="black")
		draw.text(((tw/2)+2,th-2), text, font=fnt,fill="black")
		draw.text(((tw/2)-2,th+2), text, font=fnt,fill="black")
		draw.text(((tw/2)+2,th+2), text, font=fnt,fill="black")
		draw.text(((tw/2,th)),text, font=fnt,fill="white")
		im.save(filename,"JPEG",quality = 90)
		await ctx.channel.send(file=discord.File(filename))
		os.remove(filename)
	@commands.command(pass_context=True,aliases=['meme6','vocko','nottoday'])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def moe(self,ctx):
		await ctx.channel.trigger_typing()
		await ctx.channel.send(file=discord.File("./images/extras/meme_template6.jpg"))

	@commands.command(pass_context=True,aliases=['meme7','nabozenstvi','phone2'])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def religion(self,ctx):
		await ctx.channel.trigger_typing()
		try:
			back,filename=await self.getimage(ctx)
		except TypeError:
			return await ctx.channel.send("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		size=541,423
		im=Image.open("./images/extras/meme_template7.png").convert('RGBA')
		canvas = Image.new('RGBA', im.size, (255,255,255,0))
		back=back.resize(size,resample=Image.LANCZOS).convert('RGBA')
		width,height=im.size
		canvas.paste(back,(0,230),back)
		canvas.paste(im,(0,0),im)
		canvas=canvas.convert(mode="RGB")	
		canvas.save(filename,"JPEG",quality = 90)
		await ctx.channel.send(file=discord.File(filename))
		os.remove(filename)
	@commands.command(pass_context=True,aliases=['meme8'])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def disability(self,ctx):	
		await ctx.channel.trigger_typing()
		try:
			front,filename=await self.getimage(ctx)
		except TypeError:
			return await ctx.channel.send("Žádný obrázek ve správné velikosti se mi nepodařilo najít :cry:")
		size=235,240
		im = Image.open("./images/extras/meme_template10.jpg").convert('RGBA')
		front = front.resize(size,resample=Image.LANCZOS).convert('RGBA')
		im.paste(front,(520,325),front)
		im=im.convert('RGB')
		im.save(filename,"JPEG",quality = 90)
		await ctx.channel.send(file=discord.File(filename))
		os.remove(filename)
def setup(bot):
	bot.add_cog(Images(bot))
