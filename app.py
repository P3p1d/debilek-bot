# -*- coding: UTF-8 -*-
import socket
import os
import sys,traceback
import time
import asyncio
import discord
import aiohttp
from discord import Game
from discord.ext import commands
import requests

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    prefixes = ['§','debile ']
    #if not message.server:
    #    # pouze vykricnik mimo server
    #    return '!'
    return commands.when_mentioned_or(*prefixes)(bot, message)
HOST = '' 
PORT = os.environ["PORT"] 
TOKEN = os.environ["TOKEN"]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST,PORT))
except Exception as e:
    print(e)
bot = discord.Client()
bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')
#()  []  {} `
init_extensions = ['cogs.fun','cogs.wiki','cogs.help','cogs.money','cogs.error_handler','cogs.images','cogs.Music','cogs.ascii_art','cogs.nasa']

if __name__ == '__main__':
    for extension in init_extensions:
        try:
            bot.load_extension(extension)
            print(f'Nacteno {extension}')
        except Exception as e:
            print(f'Nepodarilo se nacist {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.command(pass_context=True)
async def ping(ctx):
    before = time.monotonic()
    message = await bot.say("Pong!")
    ping = (time.monotonic() - before) * 1000
    msg = f"Ping je `{str(int(ping))}` milisekund."
    await bot.say(msg)

@bot.command(pass_context=True)
async def info(ctx):
    em = discord.Embed(color=discord.Color.green())
    em.title = 'Debílek Info'
    em.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    em.description = 'S láskou stvořen Pepidem'
    em.add_field(name="Servery", value=len(bot.servers))
    em.add_field(name="Online Uživatelé", value=str(len({m.id for m in bot.get_all_members() if m.status is not discord.Status.offline})))
    em.add_field(name='Kanály', value=f"{sum(1 for g in bot.servers for _ in g.channels)}")
    em.add_field(name="Knihovna", value=f"discord.py")
    em.add_field(name="Pozvěte Debílka na další server!", value=f"[Zde](https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=268905542)")
    em.add_field(name="Více informací o Debílkovi", value=f"[Zde](https://debilekbot.glitch.me/)",inline=False)
    em.set_footer(text="DebílekBot | jede na discord.py")
    await bot.say(embed=em)

@bot.command(pass_context=True,aliases = ['forfeit','vypadni'])
async def quit(ctx):
    if str(ctx.message.author) != "Pepid#2491":
        await bot.say("Tohle nemůžeš!")
        return
    else:
        await bot.say("Tak čau!")
        await bot.logout()
#------------------------------------------------------------------
url = f"https://discordbots.org/api/bots/{bot.user.id}/stats"
payload = {"server_count": str(len(bot.guilds))}
headers = {"Authorization": os.environ["dblTOKEN"]}
r = requests.post(url, data=payload, headers=headers)
print("[+] Guild change detected, posting guild count to DBL")
#-------------------------------------------------------------------
@bot.event
async def on_ready():
    print('Online jako:')
    print(bot.user.name)
    print(bot.user.id)
    print('-'*len(bot.user.id))
    await bot.change_presence(game=Game(name="si s kouskem hlíny"))
bot.run(TOKEN, bot = True)
