import discord
from discord import app_commands
import logging
import os
from dotenv import load_dotenv

load_dotenv()

handler = logging.FileHandler(filename='sotukenkun.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
client =  discord.Client(intents=intents)
intents.message_content = True
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

    await client.change_presence(activity=discord.Game(name='卒研くん.Ver.0.0.7'))

    await tree.sync()

    #.envファイルから'console_channel_id'を取得する
    channel_id = int(os.getenv('console_channel_id'))
    channel = client.get_channel(channel_id)

    #チャンネルIDがしっかり入っている場合にメッセージを送る
    if channel is not None:
        await channel.send("login success")
    #チャンネルIDが入っていない場合にコンソールにエラーを送る
    else:
        print("Failed to find the console channel")

#command-test
#join
@tree.command(name="sjoin",description="BOTをVCに接続します。")
async def join(interaction: discord.Interaction):
    #ボイスチャンネルに接続していない人のコマンドをはじく
    if interaction.user.voice is None:
        await interaction.response.send_message("You Not Connected Voice Channel")
        return
    # ボイスチャンネルに接続する
    await interaction.user.voice.channel.connect()
    await interaction.response.send_message("Connected!")

#leave
@tree.command(name="sleave",description="BOTをVCから切断します。")
async def leave(interaction: discord.Interaction):
    if interaction.client.voice_clients is None:
            await interaction.response.send_message("Bot Not Connected Voice Channel")
            return
    if interaction.user.voice is None:
        await interaction.response.send_message("You Not Connect Voive Channel")
        return
    # 切断する
    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message("Good Bye...")

@tree.command(name="sping",description="pingを確認します。")
async def test(interaction: discord.Interaction):
     # Ping値を秒単位で取得
    raw_ping = client.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)
    # 送信する
    await interaction.response.send_message(f"BotのPing値は{ping}msです。")

@tree.command(name="stest",description="動作確認コマンドです。")
@app_commands.default_permissions(administrator=True)
async def test(interaction: discord.Interaction):
     # Ping値を秒単位で取得
    raw_ping = client.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)
    # 送信する
    await interaction.response.send_message(f"Now Working\nBotのPing値は{ping}msです。")


#BOTを起動する
#.envファイルから'TOKEN'を取得する
client.run(os.getenv('TOKEN'), log_handler=handler)
