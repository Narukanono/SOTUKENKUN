import discord
import logging

handler = logging.FileHandler(filename='sotukenkun.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as{client.user}')

@client.event
async def on_message(message):
    # メッセージの送信者がbotだった場合は無視する
    if message.author.bot:
        return

    if message.content == "!join":
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

@client.event
async def on_message(message):
    # 送信者がbotである場合は弾く
    if message.author.bot:
        return 
    elif message.content == "test":
        # メッセージが送られてきたチャンネルに送る
        await message.channel.send("Now Working")

client.run('TOKEN', log_handler=handler)
