import discord
import logging

handler = logging.FileHandler(filename='sotukenkun.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as{client.user}')
    channel = client.get_channel(1096803719053590619)
    await channel.send("login success")

@client.event
async def on_message(message):
    # メッセージの送信者がbotだった場合は無視する
    if message.author.bot:
        return

    if message.content == "!join":
        #ボイスチャンネルに接続していない人のコマンドをはじく
        if message.author.voice is None:
            await message.channel.send("You Not Connected Voice Channel")
            return
        # ボイスチャンネルに接続する
        await message.author.voice.channel.connect()
        await message.channel.send("Connected!")

    
    elif message.content == "!leave":
        if message.guild.voice_client is None:
                await message.channel.send("You Not Connected Voice Channel")
                return
        # 切断する
        await message.guild.voice_client.disconnect()
        await message.channel.send("Good Bye...")

    #ping コマンド
    elif message.content == "!ping":
        # Ping値を秒単位で取得
        raw_ping = client.latency
        # ミリ秒に変換して丸める
        ping = round(raw_ping * 1000)
        # 送信する
        await message.reply(f"BotのPing値は{ping}msです。")

    #test コマンド
    elif message.content == "!test":
        # Ping値を秒単位で取得
        raw_ping = client.latency
        # ミリ秒に変換して丸める
        ping = round(raw_ping * 1000)
        # 送信する
        await message.channel.send(f"Now Working\nBotのPing値は{ping}msです。")

client.run('TOKEN', log_handler=handler)