import os
import shutil
import random
import discord
import textwrap
import requests
from discord.ext import commands
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
class Images:
	def __init__(self,bot):
		self.bot=bot
	@commands.command(pass_context=True,no_pm=True,aliases=['df','trojobal','obrazekvtrojobalu','deep-fry','deep_fry'])
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
						await self.bot.say("Obrázek je moc velký")
						im.close()
						os.remove(filename)
						del response
						return
					im.thumbnail(size)
					im = im.convert(mode="RGB")
					im = ImageEnhance.Color(im).enhance(factor/2)
					im = ImageEnhance.Sharpness(im).enhance(factor*15)	
					im = ImageEnhance.Contrast(im).enhance(factor*1.5)					
					im.save(filename,"JPEG",quality = 4)
					await self.bot.send_file(ctx.message.channel,filename)
					os.remove(filename)
					del response
					break
	
	@commands.command(pass_context=True,no_pm=True,aliases=['impact','impactmeme','impakt','memetext','txt'])
	@commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
	async def text(self,ctx,*text):
		await self.bot.send_typing(ctx.message.channel)
		if text == ():
			await self.bot.say("Musíš mi dát nějaký text!")
			return
		text = ' '.join(text)
		bottom_text = text.split('//')
		text = bottom_text[0]
		bottom_text=bottom_text[-1]
		para = text.splitlines()
		para = textwrap.wrap(text, width=15)
		bottom_para = bottom_text
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
					width, height = im.size
					if width > 2100 or height > 2100:
						await self.bot.say("Obrázek je moc velký")
						im.close()
						os.remove(filename)
						del response
						return
					im.thumbnail(size)
					
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
					"""	y = width-10
					draw.text((x-2, y-2), bottom_text, font=fnt, fill="black")
					draw.text((x+2, y-2), bottom_text, font=fnt, fill="black")
					draw.text((x-2, y+2), bottom_text, font=fnt, fill="black")
					draw.text((x+2, y+2), bottom_text, font=fnt, fill="black")
					draw.text((x, y), bottom_text, font=fnt, fill="white")"""
					im = im.convert(mode="RGB")
					im.save(filename,"JPEG",quality = 90)
					await self.bot.send_file(ctx.message.channel,filename)
					os.remove(filename)
					del response
					break
	@commands.command(pass_context=True,no_pm=True,aliases=['cz','czflag','cz_flag'])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def czech(self,ctx):
		await self.bot.send_typing(ctx.message.channel)
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
					width, height = im.size
					if width > 2000 or height > 2000:
						await self.bot.say("Obrázek je moc velký")
						im.close()
						os.remove(filename)
						del response
						return
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
					del response
					break
	@commands.command(pass_context=True,no_pm=True,aliases=['otoc'])
	@commands.cooldown(rate=1, per=6, type=commands.BucketType.user)
	async def rotate(self,ctx,*angle):
		await self.bot.send_typing(ctx.message.channel)
		if angle == ():
			angle = 90
		else:
			angle = int(angle[0])
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
					width, height = im.size
					if width > 2000 or height > 2000:
						await self.bot.say("Obrázek je moc velký")
						im.close()
						os.remove(filename)
						del response
						return
					im = im.convert(mode="RGB")
					im.thumbnail(size)
					im = im.rotate(angle,expand=1)
					im.save(filename,"JPEG",quality = 90)
					await self.bot.send_file(ctx.message.channel,filename)
					os.remove(filename)					
					del response
					break
def setup(bot):
	bot.add_cog(Images(bot))