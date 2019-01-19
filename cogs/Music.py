import asyncio
import discord
from discord.ext import commands
if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')
my_queue = {}
def __init__(self, bot):
        self.bot = bot

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = ' {0.title} od {0.uploader}, přidal {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [délka: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()
    def toggle_next(self,ctx):
        try:
            del my_queue[str(ctx.message.server.id)]["player"][0]
        except:
            pass
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)
    async def audio_player_task(self):
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Teď hraju ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()
class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True,aliases=["pripoj"])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def join(self, ctx, *, channel : discord.Channel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say('Už jsem v kanálu...')
        except discord.InvalidArgument:
            await self.bot.say('Ale tohle není kanál...')
        else:
            await self.bot.say('Ready na pořádnou hudbu v ' + channel.name)

    @commands.command(pass_context=True, no_pm=True,aliases=["dokanalu"])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('Jsi si jistý že jsi v kanále?')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True
    @commands.command(pass_context=True, no_pm=True,aliases=["hraj","hrej"])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def play(self, ctx, *, song : str):
        await self.bot.send_typing(ctx.message.channel)
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" 
        if state.voice is None:
            success = await ctx.invoke(self.summon)
            await self.bot.say("Načítání písničky...")
            if not success:
                return await self.bot.say("Cestou se vyskytla chyba")
        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, before_options=beforeArgs, after=lambda: state.toggle_next(ctx))
        except Exception as e:
            await self.bot.say("Při stahování písničky se vyskytla chyba, zkus jinou")
        else:
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Přidáno do fronty ' + str(entry))
            if str(ctx.message.server.id) not in my_queue:              #pridani do vlastni fronty protoze pres asyncio.Queue() nejde iterovat rip
                my_queue[str(ctx.message.server.id)] = {"player":[player,],"volume":0.2}
            else:
                my_queue[str(ctx.message.server.id)]["player"].append(player)
            await state.songs.put(entry)
            
            try:
                player.volume = my_queue[str(ctx.message.server.id)]["volume"]
            except Exception as e:
                raise e
                player.volume=0.45

    @commands.command(pass_context=True, no_pm=True,aliases=["hlasitost"])
    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    async def volume(self, ctx, value : int=0):
        """Sets the volume of the currently playing song."""
        state = self.get_voice_state(ctx.message.server)
        if value < 0:
            return await self.bot.say("Záporná hlasitost? Hmmm....")
        if value==0:
            return await self.bot.say(f"Hlasitost: {state.player.volume*100}%")
        if value > 200:
            return await self.bot.say("Maximální hlasitost je 200%")
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            my_queue[str(ctx.message.server.id)]["volume"]=player.volume
            await self.bot.say('Hlasitost nastavena na {:.0%}'.format(player.volume))
    @commands.command(pass_context=True, no_pm=True,aliases=["pauza"])
    async def pause(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()      
    @commands.command(pass_context=True, no_pm=True,aliases=["pokracuj","continue"])
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)
        try:
            del my_queue[str(server.id)]
        except:
            pass
        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
            await self.bot.say("Odpojil jsem se a smazal jsem frontu")
        except:
            pass

    @commands.command(pass_context=True, no_pm=True,aliases=["preskoc"])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """
        await self.bot.send_typing(ctx.message.channel)
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Teď nic nehraju...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say(f'Přeskočeno na pokyn {ctx.message.author.display_name}...')
            state.skip()
        elif voter.id not in state.skip_votes:
            mems = ctx.message.author.voice_channel.voice_members
            if not len(mems) > 1:
                return await self.bot.say("V kanálu ale nikdo jiný není!")
            needed = int(len(mems)/2)
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= needed:
                await self.bot.say('Odhlasováno, přeskakuji písničku')
                state.skip()
            else:
                await self.bot.say(f'Tvůj hlas byl zaznamenán momentálně jsme na [{total_votes}/{needed}]')
        else:
            await self.bot.say('Pro přeskočení už jsi hlasoval')

    @commands.command(pass_context=True, no_pm=True,aliases=["hraje"])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def playing(self, ctx):
        """Shows info about the currently played song."""
        await self.bot.send_typing(ctx.message.channel)
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Momentálně nic nehraju')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('Právě hraju {} [přeskočení: {}/3]'.format(state.current, skip_count))
   

    @commands.command(pass_context = True,no_pm=True,aliases=["fronta"])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def queue(self,ctx):
        await self.bot.send_typing(ctx.message.channel)
        server = ctx.message.server
        e = discord.Embed(colour = discord.Colour.red())
        e.set_author(name="Fronta")
        if server.id in my_queue:
            if my_queue[server.id] != {}:
                i = 0
                duration = 0
                error = False
                for x in my_queue[server.id]["player"]:
                    try:    
                        i+=1
                        duration += x.duration
                        m,s=divmod(x.duration,60)
                        if s<10:
                            s="0"+str(s)
                        rating = round(x.likes/((x.likes+x.dislikes)/100),1)
                        info = f"délka: {m}:{s}, hodnocení: {rating}%"
                        e.add_field(name=f"{str(i)}) {x.title} od {x.uploader}",value=info,inline=False)
                    except:
                        if not error:
                            error = True
                m,s = divmod(duration,60)
                if s<10:
                        s="0"+str(s)
                e.set_footer(text=f"Celková délka fronty je {m}:{s}")
                if error:
                    await self.bot.say("Při sestavování fronty se vyskytla chybka, nejvíc lit písničky se nejspíš neobjeví :information_desk_person:")                    
                await self.bot.send_message(ctx.message.channel,embed=e)
            else:
                await self.bot.say("Ve frontě nic není!")
        else:
            await self.bot.say("Ve frontě nic není!")

def setup(bot):
    bot.add_cog(Music(bot))
