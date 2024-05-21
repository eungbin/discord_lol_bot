import discord
import json
from discord.ext.commands import Bot
import random

# 사용자가 명령어 입력 시 /를 입력하고 명령어 입력
client = Bot(command_prefix='/', intents=discord.Intents.all())

with open('./config.json', 'r') as f:
    json_data = json.load(f)

TOKEN = json_data['token']
# CHANNEL_ID = json_data['channel_id']

# 내전 관련 변수

players = []
team_A = []
team_B = []

###############

# on_ready는 시작할 때 한번만 실행.
@client.event
async def on_ready():
    print('Login...')
    print(f'{client.user}에 로그인하였습니다.')
    print(f'ID: {client.user.name}')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('개발'))

@client.command(aliases=['도움말'])
async def hello(ctx):
    box = discord.Embed(title='명령어 모음', description='', color=0x444)
    box.add_field(name='/명단', value='/명단 현재 명단에 포함된 소환사 목록 확인')
    box.add_field(name='/참가', value='/참가 [이름]으로 해당 소환사 내전 명단에 추가')
    box.add_field(name='/다수참가', value='/다수참가 [이름,이름,이름]으로 해당 소환사 내전 명단에 추가')
    box.add_field(name='/제외', value='/제외 [이름]으로 해당 소환사 내전 명단에서 제외')
    box.add_field(name='모든 명령어의 []는 제외하여야 합니다!')

    await ctx.send(embed=box)

@client.command(aliases=['참가'])
async def join(ctx, *args):
    if args.__len__() > 1:
        box = discord.Embed(title='/참가 [소환사명]의 형태로 입력해주세요.', color=0x444)
    
    elif players.__len__() == 10:
        box = discord.Embed(title='10명의 소환사 모두 등록되어 있습니다.')

    elif args[0] in players:
        box = discord.Embed(title='이미 참가한 소환사입니다.')
    
    else:
        box = discord.Embed(title='현재 참가 인원', color=0x444)
        players.append(args[0])
        for player in players:
            box.add_field(name=player, value='')
        
    await ctx.send(embed=box)

@client.command(aliases=['다수참가'])
async def manyJoin(ctx, *args):
    names = args[0].split(',')
    dup_player = []

    if args.__len__() > 1:
        box = discord.Embed(title='/다수참가 [소환사명]의 형태로 입력해주세요.', color=0x444)

    elif args.__len__() + players.__len__() > 10:
        box = discord.Embed(title='총 10명의 소환사만 등록이 가능합니다.')
    
    else:
        box = discord.Embed(title='현재 참가 인원', color=0x444)

        for name in names:
            if name in players:
                dup_player.append(name)
            else:
                players.append(name)
        for player in players:
            box.add_field(name=player, value='')
        
        if dup_player.__len__() > 0:
            dup_str = ''
            for player in dup_player:
                dup_str += player+' '
            box.add_field(name='중복 입력된 플레이어', value=dup_str)

    await ctx.send(embed=box)

@client.command(aliases=['제외'])
async def exceptMember(ctx, *args):
    if args.__len__() > 1:
        box = discord.Embed(title='/제외 [소환사명]의 형태로 입력해주세요.', color=0x444)
    
    elif players.__len__() == 0:
        box = discord.Embed(title='현재 참가중인 소환사가 존재하지 않습니다.', color=0x444)

    else:
        if args[0] in players:
            players.remove(args[0])
            box = discord.Embed(title='현재 참가 인원', color=0x444)
            for player in players:
                box.add_field(name=player, value='')
        
        else:
            box = discord.Embed(title='입력하신 소환사는 참여중이지 않습니다.', color=0x444)

    await ctx.send(embed=box)

@client.command(aliases=['랜덤팀'])
async def random(ctx, *args):
    team_A = [], team_B = []

    if players.__len__() != 10:
        box = discord.Embed(title='명단에 등록된 소환사가 부족합니다! 총 10명을 채워주세요.')
        await ctx.send(embed=box)
        return
    
    for player in players:
        if team_A.__len__() == 5:
            team_B.append(player)
        elif team_B.__len__() == 5:
            team_A.append(player)
        else:
            if random.randrange(1, 3) == 1:
                team_A.append(player)
            else:
                team_B.append(player)
            
        


client.run(TOKEN)