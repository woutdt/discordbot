import discord
import requests
import json
import youtube_dl
import os
from discord import FFmpegPCMAudio
from os import system
from discord.ext import commands
import mysql.connector

import asyncio
import functools
import itertools
import math
import random
from async_timeout import timeout

bot = commands.Bot(command_prefix='.', description='leuke negerbot')

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="wout",
    database="userlevels",
    auth_plugin="mysql_native_password"
)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(db)
    for guild in bot.guilds:
        print(guild.id)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=".help", state="ROAM's discordbot", details="discord.py, python, youtube_dl"))

def checkLevel(xp: int):
    if xp <= 50:
        if xp == 50:
            level = 2
            promoted = True
        else:
            level = 1
            promoted = False
    elif xp <= 120:
        if xp == 120:
            level = 3
            promoted = True
        else:
            level = 2
            promoted = False
    elif xp <= 190:
        if xp == 190:
            level = 4
            promoted = True
        else:
            level = 3
            promoted = False
    elif xp <= 280:
        if xp == 280:
            level = 5
            promoted = True
        else:
            level = 4
            promoted = False
    elif xp <= 380:
        if xp == 380:
            level = 6
            promoted = True
        else:
            level = 5
            promoted = False
    elif xp <= 490:
        if xp == 490:
            level = 7
            promoted = True
        else:
            level = 6
            promoted = False
    elif xp <= 600:
        if xp == 600:
            level = 8
            promoted = True
        else:
            level = 7
            promoted = False
    elif xp <= 720:
        if xp == 720:
            level = 9
            promoted = True
        else:
            level = 8
            promoted = False
    elif xp <= 850:
        if xp == 850:
            level = 10
            promoted = True
        else:
            level = 9
            promoted = False
    elif xp <= 1000:
        if xp == 1000:
            level = 11
            promoted = True
        else:
            level = 10
            promoted = False
    elif xp <= 1250:
        if xp == 1250:
            level = 12
            promoted = True
        else:
            level = 11
            promoted = False
    elif xp <= 1500:
        if xp == 1500:
            level = 13
            promoted = True
        else:
            level = 12
            promoted = False
    elif xp <= 1750:
        if xp == 1750:
            level = 14
            promoted = True
        else:
            level = 13
            promoted = False
    elif xp <= 2000:
        if xp == 2000:
            level = 15
            promoted = True
        else:
            level = 14
            promoted = False
    elif xp <= 2300:
        if xp == 2300:
            level = 16
            promoted = True
        else:
            level = 15
            promoted = False
    elif xp > 1000000:
        level = 420
        promoted = False
    elif xp > 69000:
        level = 69
        promoted = False
    
    response = {
        'level': level,
        'promoted': promoted
    }
    return response

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith(".idee "):
        f=open("idee.txt", "a+")
        f.write("van {} :->  {} \n".format(message.author.name, message.content))
        thisChannel = message.guild.get_channel(message.channel.id)
        await thisChannel.send("idee verstuurd naar database!")
    print("guild: {} , channel: {}, author: {}, message: {}".format(message.guild.name, message.channel.name, message.author.name, message.content))
    f= open("logs.txt", "a")
    f.write("guild: {} , channel: {}, author: {}, message: {} \n".format(message.guild.name, message.channel.name, message.author.name, message.content))
    await bot.process_commands(message)

    if message.content.startswith("."):
        pass
    else:
        xp = 5
        cursor = db.cursor()
        cursor.execute("SELECT user_xp FROM users WHERE client_id = {}".format(str(message.author.id)))
        result = cursor.fetchall()
        if len(result) == 0:
            print("new user in database with name {}".format(message.author.name))
            cursor.execute('INSERT INTO users (client_id, user_xp, name) VALUES({},{},"{}")'.format(str(message.author.id), str(xp), str(message.author.name)))
            db.commit()
            await message.channel.send("you just made your first xp, blijf berichte sturen voor meer xp en ket")
        else:
            currentXP = result[0][0]
            newXP = currentXP + xp
            cursor.execute("UPDATE users SET user_xp = {} WHERE client_id = {}".format(str(newXP),str(message.author.id)))
            db.commit()
            print("user: {}, xp: {}".format(str(message.author.name), str(newXP)))
            cursor = db.cursor()
            cursor.execute("SELECT user_xp FROM users WHERE client_id = {}".format(str(message.author.id)))
            levelXP = cursor.fetchall()
            levelXP = levelXP[0][0]
            levelObj = checkLevel(levelXP)
            if levelObj['promoted'] == True:
                await message.channel.send(message.author.mention + ' has leveled up to level {}, keihard'.format(str(levelObj['level'])))

@bot.command()
async def level(ctx):
    levelcursor = db.cursor()
    levelcursor.execute("SELECT user_xp FROM users WHERE client_id = {}".format(str(ctx.author.id)))
    result = levelcursor.fetchall()
    result = result[0][0]
    levelObj = checkLevel(result)
    await ctx.send(ctx.author.mention)
    await ctx.send("```glsl\n you are level: {}, jij gaat zo dik ```".format(str(levelObj['level'])))

@bot.command()
async def ranking(ctx, page: int =1):
    cursor = db.cursor()
    cursor.execute("SELECT user_xp, name FROM users ORDER BY user_xp DESC")
    result = cursor.fetchall()

    items_per_page = 10

    start = (page - 1) * items_per_page
    end = start + items_per_page

    queue = ''
    for i, person in enumerate(result[start:end], start=start):
        queue += '`{0}.` **{1[1]}**: {1[0]}\n'.format(i + 1, person)

    embed = (discord.Embed(description='**XP ranking**\n\n{}'.format(queue)))
    await ctx.send(embed=embed)

@bot.command()
async def savedSummoner(ctx, name):
    if name:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE summonerName = {}".format(str(name)))
        result =  db.fetchall()
        if result:
            pass

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="ROAM's bot", description="made by Wout De Tollenaere", color=0x3eeb69)
    embed.add_field(name="ROAM", value="code: python, discord.py, requests, riotApi, youtube_dl")
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")
    embed.add_field(name="prefix", value=". ==> used before every command ==> [prefix]command")
    embed.add_field(name="[]", value="variable ==> usually want u want to search (only where needed)")
    embed.add_field(name="Help command", value=".help")
    embed.add_field(name="Invite", value="https://discordapp.com/api/oauth2/authorize?client_id=634462430251974657&permissions=8&scope=bot")
    embed.add_field(name="github", value="https://github.com/woutdt/discordbot/blob/master/discordcommand.py")
    embed.set_thumbnail(url="https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwjTuJq7rprmAhWMjKQKHcldCAUQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.raspberrypi.org%2Ftrademark-rules%2F&psig=AOvVaw05IWS-adSk_PsJcCkjF8cX&ust=1575492873986160")

    await ctx.send(embed=embed)

@bot.command()
async def homo(ctx, *, member):
    await ctx.channel.purge(limit =1)
    await ctx.send(member + " is een homo")

@bot.command()
async def slaapwel(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(ctx.author.mention + ' gaat slapen, slaapwel!')

@bot.command()
async def koekje(ctx):
    await ctx.channel.purge(limit =1)
    await ctx.send("<:hondekoekje:615167466259087370>")

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="new member")
    guild = member.guild
    if role == None:
        await guild.create_role(name="new member")
        await member.add_roles(member, role)
    else:
        await member.add_roles(member, role)
    await member.guild.send('{}, just joined the server, hello!'.format(member.name))

bot.remove_command('help')

@bot.command()
async def neger(ctx, name):
    await ctx.channel.purge(limit=1)
    await ctx.send(name + "is een grote neger")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="24/7 uptime coming soon", description="all commands available right now:", color=0x3eeb69)

    embed.add_field(name="info", value="info about this bot", inline=False)
    embed.add_field(name="leagueoflegends", value="te moe voor een beschrijving fk dit ~ 3u 30 (AM)", inline=False)
    embed.add_field(name="djket", value="run this command for help with the musicbot")
    embed.add_field(name="games", value="uitleg over spelletjes", inline=False)
    embed.add_field(name="ranking", value="ranking")
    embed.add_field(name="level", value="level")
    await ctx.send(embed=embed)

@bot.command()
async def leagueoflegends(ctx):
    embed = discord.Embed(title="league of legends API", description="all commands available right now", color=0x3eeb69)
    embed.add_field(name="summoner [name]", value="short summary of your profile")
    embed.add_field(name="mastery [name]", value="gives your highest mastery champions")
    embed.add_field(name="lastgame [name]", value="gives details about your last game")
    embed.add_field(name=" \n more to follow", value="in the future....")
    await ctx.send(embed=embed)

headers = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": "RGAPI-d1921b67-13fb-4ec3-b0b6-81e934e391ff",
    "Accept-Language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}

URL = "https://euw1.api.riotgames.com/"

@bot.command()
async def summoner(ctx, *, arg):
    summonerName = arg
    r = requests.get(url = URL+'lol/summoner/v4/summoners/by-name/'+summonerName+'?api_key=RGAPI-d1921b67-13fb-4ec3-b0b6-81e934e391ff', params = '', headers=headers)
    data = r.json()
    m = requests.get(url = URL+'lol/match/v4/matchlists/by-account/'+ data['accountId']+ '?endIndex=5&beginIndex=0',params=None, headers = headers)
    matches = m.json()
    stats = []
    hero = []
    champions1 = json.loads(open('champions-en_gb.json').read())
    queues = json.loads(open('queues.json').read())
    for i in matches['matches']:
        s = requests.get(url = URL+'lol/match/v4/matches/' + str(i['gameId']),params=None, headers= headers )
        sgame = s.json()
        queueId = sgame['queueId']
        for object in queues:
            if object['queueId'] == queueId:
                gamemode = object['description']
                gamemode = gamemode[:-1]
                break
        for p in sgame['participants']:
            if p['championId'] == i['champion']:
                hero.append(champions1[str(p['championId'])])
                if p['stats']['win'] == True:
                    win = "win"
                elif p['stats']['win'] == False:
                    win = "Loss"
                else:
                    win = "draw"

                object = {
                    'win': win,
                    'gamemode': gamemode,
                    'kills': p['stats']['kills'],
                    'deaths': p['stats']['deaths'],
                    'assists': p['stats']['assists']
                }
                stats.append(object)
                break

    mastery = requests.get(url=URL+'lol/champion-mastery/v4/champion-masteries/by-summoner/'+data['id'], params=None, headers=headers)
    masteryChampion = mastery.json()
    masteryChampion = masteryChampion[0]
    masteryChampion['name']= champions1[str(masteryChampion['championId'])]
    
    embed = discord.Embed(title=data['name'], description='summoner', color=0x3eeb69)
    embed.set_thumbnail(url="http://ddragon.leagueoflegends.com/cdn/9.23.1/img/profileicon/"+ str(data['profileIconId'])+ ".png")
    embed.add_field(name="level", value=data['summonerLevel'])
    embed.add_field(name="highest mastery champion", value="{} \n mastery score: {} \n champion level: {}".format(masteryChampion['name'], masteryChampion['championPoints'], masteryChampion['championLevel']))

    await ctx.send(embed=embed)

    a = 0
    for i in stats:
        if a == 3:
            break
        if i['win'] == "win":
            embed = discord.Embed(title="{}".format(i['gamemode'].lower()), description=hero[a], color=0x3eeb69)
        elif i['win'] == "Loss":
            embed = discord.Embed(title="{}".format(i['gamemode'].lower()), description=hero[a], color=0xfd0303)
        else:
            break
        embed.add_field(name="kills", value=i['kills'])
        embed.add_field(name="deaths", value=str(i['deaths']))
        embed.add_field(name="assists", value=str(i['assists']))
        embed.set_thumbnail(url="http://ddragon.leagueoflegends.com/cdn/9.23.1/img/champion/{}.png".format(hero[a]))

        await ctx.send(embed=embed)

        a = a + 1


@bot.command()
async def mastery(ctx, *, arg):
    summonerName = arg
    r = requests.get(url = URL+'lol/summoner/v4/summoners/by-name/'+summonerName+'?api_key=RGAPI-d1921b67-13fb-4ec3-b0b6-81e934e391ff', params = '', headers=headers)
    summoner = r.json()
    mastery = requests.get(url=URL+'lol/champion-mastery/v4/champion-masteries/by-summoner/'+summoner['id'], params=None, headers=headers)
    masteryChampions = mastery.json()
    championNames = json.loads(open('champions-en_gb.json').read())


    embed = discord.Embed(title="highest mastery champions", description=summoner['name'])
    a = 0
    for champion in masteryChampions:
        if a == 3:
            break
        championName = championNames[str(champion['championId'])]
        if champion['chestGranted'] == True:
            chestGranted = "Yes"
        elif champion['chestGranted'] == False:
            chestGranted == "No"
        embed.add_field(name=championName, value="mastery score: {} \n champion level: {} \n point since last level: {} \n chest granted: {}".format(champion['championPoints'], champion['championLevel'], champion['championPointsSinceLastLevel'], chestGranted))
        a += 1
    
    await ctx.send(embed=embed)

@bot.command()
async def lastgame(ctx, *, arg):
    summonerName = arg
    summoner = requests.get(url = URL+'lol/summoner/v4/summoners/by-name/'+summonerName, params = '', headers=headers).json()
    lastGames = requests.get(url = URL+'lol/match/v4/matchlists/by-account/'+ summoner['accountId']+ '?endIndex=5&beginIndex=0',params=None, headers = headers).json()
    wantedGame = requests.get(url= URL+'lol/match/v4/matches/{}'.format(lastGames['matches'][0]['gameId']), params=None, headers = headers).json()

    mainGameInfo = wantedGame  #game variable
    gameParticipants = wantedGame['participants']
    gameTeams = wantedGame['teams']
    participantIdentities = wantedGame['participantIdentities']

    championNames = json.loads(open('champions-en_gb.json').read())
    gameModes = json.loads(open('queues.json').read())
    for object in gameModes:
        if object['queueId'] == mainGameInfo['queueId']:
                gamemode = object['description']
                gamemode = gamemode[:-1]
                break
    for participant in participantIdentities:
        if participant['player']['accountId'] == summoner['accountId']:
            participantId = participant['participantId']
            break
    for gameParticipant in gameParticipants:
        if gameParticipant['participantId'] == participantId:
            wantedParticipant = gameParticipant  #participant variable
            break
    if wantedParticipant['teamId'] == 100:
        teamSide = "Blue side"
    elif wantedParticipant['teamId'] == 200:
        teamSide = "Red side"
    for team in gameTeams:
        if team['teamId'] == wantedParticipant['teamId']:
            winOrLoss = team['win']
            thisTeam = team  #team variable for param summoner
            if winOrLoss == "Fail":
                winOrLoss = "Lost"
            elif winOrLoss == "Win":
                winOrLoss = "Won"
            break
    championName = championNames[str(wantedParticipant['championId'])]
    kda = "{}/{}/{}".format(wantedParticipant['stats']['kills'], wantedParticipant['stats']['deaths'], wantedParticipant['stats']['assists'])

    #killparticipation
    def calcKillParticipation():
        summonerKills = wantedParticipant['stats']['kills'] + wantedParticipant['stats']['assists']
        teamKills = 0
        for gameParticipant in gameParticipants:
            if gameParticipant['teamId'] == wantedParticipant['teamId']:
                teamKills = teamKills + gameParticipant['stats']['kills']
        killPercentage = int(summonerKills / teamKills * 100)
        return killPercentage
        
    def calcCsPMin():
        summonerCsKills = wantedParticipant['stats']['totalMinionsKilled']
        gameLength = mainGameInfo['gameDuration'] / 60
        minionPMin = round(summonerCsKills / gameLength, 2)
        return minionPMin

    if winOrLoss == "Won":
        embed = discord.Embed(title="last game stats for {}".format(summonerName), description=gamemode, color=0x3eeb69)
    elif winOrLoss == "Lost":
        embed = discord.Embed(title="last game stats for {}".format(summonerName), description=gamemode, color=0xfd0303)

    embed.set_thumbnail(url="http://ddragon.leagueoflegends.com/cdn/9.23.1/img/champion/{}.png".format(championName))
    embed.add_field(name="team", value="{} , played as {} and {} with a KDA of {}".format(teamSide, championName, winOrLoss, kda ), inline=False)
    embed.add_field(name="team stats", value="towers destroyed: {} \n dragon kills: {} \n baron kills: {} \n first blood: {} \n rift herald kills: {} \n kill percentage: {}%".format(thisTeam['towerKills'], thisTeam['dragonKills'], thisTeam['baronKills'], thisTeam['firstBlood'], thisTeam['riftHeraldKills'], calcKillParticipation()))
    embed.add_field(name="player stats",value="damage to objectives: {} \n neutrals killed: {} \n wards killed: {} \n damage dealt: {} \n gold earned: {}".format(wantedParticipant['stats']['damageDealtToObjectives'],wantedParticipant['stats']['neutralMinionsKilled'], wantedParticipant['stats']['wardsKilled'], wantedParticipant['stats']['totalDamageDealt'], wantedParticipant['stats']['goldEarned'] ))
    embed.add_field(name="-", value="champion level: {} \n total minions: {} \n physical dmg: {} \n magic dmg: {} \n damage taken: {} \n Cs/Min: {}/min".format(wantedParticipant['stats']['champLevel'], wantedParticipant['stats']['totalMinionsKilled'], wantedParticipant['stats']['physicalDamageDealt'], wantedParticipant['stats']['magicDamageDealt'], wantedParticipant['stats']['totalDamageTaken'], calcCsPMin() ))

    await ctx.send(embed=embed)

youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self), 
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon')
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume')
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='stop')
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 2:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/2**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

    @commands.command(name='queue')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop')
    async def _loop(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play')
    async def _play(self, ctx: commands.Context, *, search: str):

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')

@bot.command(pass_context=True)
async def djket(ctx):
    embed = discord.Embed(title="all commands for dj ket", description="made by ROAM", color=discord.Color.blurple())
    embed.add_field(name="join", value="always use this first, or the bot will break")
    embed.add_field(name="play [musictitle]", value="plays music, or adds the music to the queue")
    embed.add_field(name="pause", value="pause the currently playing song")
    embed.add_field(name="resume", value="resumes the currently playing song")
    embed.add_field(name="skip", value="skips the currently playing song")
    embed.add_field(name="remove [index queue]", value="removes the [index queue]nd song from the queue")
    embed.add_field(name="shuffle", value="shuffle the queue")
    embed.add_field(name="queue", value="show the current queue")
    embed.add_field(name="stop", value="stops dj ketekoek from playing music")
    embed.add_field(name="now", value="shows the currently playing song")
    embed.add_field(name="leave", value="dj wannes leaves the voice channel")
    embed.add_field(name="volume [0-100]", value="changes volume starting from the next song")
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def games(ctx):
    embed = discord.Embed(title="game ROAM's catalogus", description="games are currently programmed only in dutch", color=discord.Color.purple())
    embed.add_field(name="stp [keuze]", value="keuze uit schaar - steen - papier, let op spelling")
    embed.add_field(name="roll [max]", value="random getal tussen 0 en [max]")
    embed.add_field(name="guessthenumber [number]", value="gok een nummer tussen 1 en 200, het nummer is hetzelfde voor iedereen en blijft hetzelfde tot geraden m.a.w eenzelfde nummer 2 keer gokken heeft geen zin")
    embed.add_field(name="\n ideën voor meer games?", value="--> .idee [idee]")
    await ctx.send(embed=embed)

bot_choices = ['schaar', 'steen', 'papier']

@bot.command(pass_context=True, aliases=['stp'])
async def schaarsteenpapier(ctx, choice: str):
    bot_choice = bot_choices[random.randint(0, 2)]
    user_choice = choice
    print(bot_choice)
    if not user_choice:
        await ctx.send('```css\n ge moet wel kiezen uit schaar steen papier eh manneken\n```')
    if not user_choice == 'schaar' and not user_choice == 'steen' and not user_choice == 'papier':
        await ctx.send('```css\n hebje wel de correcte spelling gebruikt?\n```')
    
    win = ''
    if user_choice == 'steen':
        if bot_choice == 'papier':
            win = False
        elif bot_choice == 'schaar':
            win = True
        elif bot_choice == user_choice:
            win = None
    if user_choice == 'papier':
        if bot_choice == 'papier':
            win = None
        elif bot_choice == 'schaar':
            win = False
        elif bot_choice == 'steen':
            win = True
    if user_choice == 'schaar':
        if bot_choice == 'papier':
            win = True
        elif bot_choice == 'steen':
            win = False
        elif bot_choice == 'schaar':
            win = None

    if win == True:
        await ctx.send('```css\n jij wint {} verslaat {}\n```'.format(user_choice, bot_choice))
    elif win == False:
        await ctx.send('```css\n jij verliest {} verslaat {}\n```'.format(bot_choice, user_choice))
    elif win == None:
        await ctx.send('```css\n gelijkspel {} = {}\n```'.format(user_choice, bot_choice))

class RandomNumber:
    def __init__(self):
        self.number = random.randint(1,200)
        self.entries = 0
        self.roll = 0
    
    def addEntry(self):
        self.entries += 1
    
    def resetNumber(self):
        self.number = random.randint(1,200)
        self.entries = 0
    
    def fromRange(self, fromto):
        lastPoint = fromto
        self.roll = random.randint(0, lastPoint)
        return self.roll

numberguess = RandomNumber()

@bot.command(pass_context=True, aliases=['random'])
async def guessthenumber(ctx, guess):
    if numberguess.number == int(guess):
        await ctx.send('```cs\n proficiat, juiste nummer geraden \n nieuw nummer gekozen tussen 1 en 200\n```')
        numberguess.resetNumber()
    elif not numberguess.number == guess:
        numberguess.addEntry()
        await ctx.send('```cs\n spijtig, juiste nummer nog niet geraden , {0} keer geprobeerd\n het nummer tussen 1 en 200 blijft hetzelfde\n```'.format(numberguess.entries))  
    print(numberguess.number)
    print(numberguess.entries)

@bot.command(pass_context=True)
async def roll(ctx, fromto: int):
    setRange = fromto
    randomnumber = numberguess.fromRange(setRange)
    await ctx.send('```cs\n you rolled: {0} \n```'.format(randomnumber)) 

bot.add_cog(Music(bot))
#run bot command
bot.run('NjM0NDYyNDMwMjUxOTc0NjU3.XfQaAw.SX6MIkrDUinAcy7nrgCKOhQQYaE')


 