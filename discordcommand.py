import discord
import requests
import json
from discord.ext import commands

bot = commands.Bot(command_prefix='$$', description='leuke negerbot')

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
    embed.add_field(name="Help command", value="$$help")
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
    champions1 = json.loads(open('discordbot/champions-en_gb.json').read())
    queues = json.loads(open('discordbot/queues.json').read())
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



bot.run('NjM0NDYyNDMwMjUxOTc0NjU3.XebLOw.E7qNEoNxU3-aPGmEkSJJXo8p15M')


