import discord
import json
from discord.ext.commands import Bot

# 사용자가 명령어 입력 시 /를 입력하고 명령어 입력
client = Bot(command_prefix='/', intents=discord.Intents.all())

with open('./config.json', 'r') as f:
    json_data = json.load(f)

TOKEN = json_data['token']
# CHANNEL_ID = json_data['channel_id']

# 내전 관련 변수

people = []

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
    box.add_field(name='/참가', value='/참가 [이름]으로 해당 소환사 내전 명단에 추가')
    box.add_field(name='/제외', value='/제외 [이름]으로 해당 소환사 내전 명단에서 제외')

    await ctx.send(embed=box)

@client.command(aliases=['참가'])
async def war(ctx):
    await ctx.send(ctx)
    box = discord.Embed(title='내전 관련 명령어 모음', description='', color=0x444)
    box.add_field(name='/내전 인원추가 [이름]', value='[이름] 인원 추가')

    await ctx.send(embed=box)

client.run(TOKEN)