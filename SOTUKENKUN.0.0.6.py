import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv

load_dotenv()

handler = logging.FileHandler(filename='sotukenkun.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

bot =  commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    await bot.change_presence(activity=discord.Game(name='卒業研究.Ver.0.0.6'))

    #.envファイルから'console_channel_id'を取得する
    channel_id = int(os.getenv('console_channel_id'))
    channel = bot.get_channel(channel_id)

    #チャンネルIDがしっかり入っている場合にメッセージを送る
    if channel is not None:
        await channel.send("login success")
    #チャンネルIDが入っていない場合にコンソールにエラーを送る
    else:
        print("Failed to find the console channel")

#command-test
#join
@bot.command()
async def join(ctx):
    #ボイスチャンネルに接続していない人のコマンドをはじく
    if ctx.message.author.voice is None:
        await ctx.message.channel.send("You Not Connected Voice Channel")
        return
    # ボイスチャンネルに接続する
    await ctx.message.author.voice.channel.connect()
    await ctx.message.channel.send("Connected!")

#leave
@bot.command()
async def leave(ctx):
    if ctx.message.guild.voice_client is None:
            await ctx.message.channel.send("You Not Connected Voice Channel")
            return
    # 切断する
    await ctx.message.guild.voice_client.disconnect()
    await ctx.message.channel.send("Good Bye...")

@bot.command()
async def ping(ctx):
    # Ping値を秒単位で取得
    raw_ping = bot.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)
    # 送信する
    await ctx.message.reply(f"BotのPing値は{ping}msです。")

@bot.command()
async def test(ctx):
     # Ping値を秒単位で取得
    raw_ping = bot.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)
    # 送信する
    await ctx.message.channel.send(f"Now Working\nBotのPing値は{ping}msです。")


#BOTを起動する
#.envファイルから'TOKEN'を取得する
bot.run(os.getenv('TOKEN'), log_handler=handler)
