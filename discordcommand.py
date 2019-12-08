import discord
import requests
import json
import youtube_dl
import os
from discord import FFmpegPCMAudio
from os import system
from discord.ext import commands

bot = commands.Bot(command_prefix='.', description='leuke negerbot')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="neger bot", description="league of legends is gay", color=0xeee657)
    embed.add_field(name="ROAM", value="made using python")
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")
    embed.add_field(name="Help command", value=".help")
    embed.add_field(name="Invite", value="https://discordapp.com/api/oauth2/authorize?client_id=634462430251974657&permissions=8&scope=bot")
    embed.add_field(name="github", value="https://github.com/woutdt/discordbot/blob/master/discordcommand.py")
    embed.set_thumbnail(url="https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwjTuJq7rprmAhWMjKQKHcldCAUQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.raspberrypi.org%2Ftrademark-rules%2F&psig=AOvVaw05IWS-adSk_PsJcCkjF8cX&ust=1575492873986160")

    await ctx.send(embed=embed)

@bot.command()
async def neger(ctx):
    await ctx.send("wannes is een neger")

@bot.command()
async def nigger(ctx,*, arg):
    await ctx.send(arg+" is een grote neger")

@bot.command()
async def homo(ctx, *, member):
    await ctx.channel.purge(limit =1)
    await ctx.send(member + " is een homo")

@bot.command()
async def koekje(ctx):
    await ctx.channel.purge(limit =1)
    await ctx.send("<:hondekoekje:615167466259087370>")

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, id="634801799076904971")
    await member.add_roles(member, role)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="leuke negerbot", description="all commands available right now:", color=0x3eeb69)

    embed.add_field(name="$$neger", value="replies with: wannes is een neger", inline=False)
    embed.add_field(name="$$nigger naam", value="naam = parameter => 'naam' is een neger", inline=False)
    embed.add_field(name="$$koekje", value="<:hondekoekje:615167466259087370>", inline=False)
    embed.add_field(name="$$info", value="info about this bot", inline=False)
    embed.add_field(name="$$homo @naam", value="naam= parameter => @naam is een homo")
    embed.add_field(name="$$summoner ---naam----", value="veel uren werk", inline=False)
    
    embed.add_field(name="in production", value="...", inline=False)

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

#musicbot
@bot.command()
async def musichelp(ctx):
    embed = discord.Embed(title="commands to play music", description="more to follow")
    embed.add_field(name="join", value="to start playing, invite wannesbot to your current voice channel \n or use: 'j'")
    embed.add_field(name="play [url]", value="play music from a youtube url \n or use: 'pl")
    embed.add_field(name="pause", value="pause the music \n or use: 'p'")
    embed.add_field(name="stop", value="delete the current playing music \n or use: 's'")
    embed.add_field(name="leave", value="make wannesbot leave the voice channel :( \n or use: 'l'")
    await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['j', 'jo'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a negervoice channel")
        return
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        voice.is_connected()
    await ctx.send(f"Joined {channel}")

@bot.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music end or use the 'stop' command")
        return
    await ctx.send("This process can take some time....")
    print("music process started")
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    await ctx.channel.purge(limit= 1)
    voice.is_playing()

@bot.command(pass_context=True, aliasas=['s', 'st'])
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("done playing music")
    song = os.path.isfile("song.mp3")
    if song:
        os.remove("song.mp3")

@bot.command(pass_context=True, aliases=['p'])
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.pause()  
    embed = discord.Embed(title="paused")
    await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['l', 'le', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Don't think I am in a voice channel")

#run bot command



