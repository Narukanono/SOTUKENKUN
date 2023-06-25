import discord
from discord import app_commands
import logging
import os
from dotenv import load_dotenv
import requests
import json
import wave
import pickle
import datetime
import asyncio
import re

#envファイルの読み込み
load_dotenv()

#speakerのユーザデータを保存するdataというフォルダが無いことの確認
if not os.path.isdir("./userdata"):
    #無いので作成
    os.makedirs("./userdata")

#読み上げの音声データを保存するためのaudioというフォルダが無いことの確認
if not os.path.isdir("./audio"):
    #無いので作成
    os.makedirs("./audio")

#サーバーごとに実行チャンネルと辞書を保存するためのserverというフォルダが無いことの確認
if not os.path.isdir("./serverdata"):
    #無いので作成
    os.makedirs("./serverdata")

#再生待ちに使うqueueの作成
queue =[]

#コンソール表示に使うあれこれ
connecting_vcs = 0

#ログファイルの作成
#ddnに現在の時間を入れる
ddn = datetime.datetime.now()
#ddtに今日の日付を入れる
ddt = datetime.date.today()
#現在の「年-月-日」というフォルダが無いことの確認
if not os.path.isdir(f"./log/{ddt}"):
    #無いので作成
    os.makedirs(f"./log/{ddt}")
#先ほど作ったフォルダの中に現在の「時間-分-秒.log」というファイル名でログファイルを作成
handler = logging.FileHandler(filename=f'./log/{datetime.date.today()}/{ddn.hour}-{ddn.minute}-{ddn.second}.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
client =  discord.Client(intents=intents)
intents.message_content = True
tree = app_commands.CommandTree(client)

#音声合成用class
class VoicevoxConnect():
    #URLチェック
    def remove_url(text):
        uclear = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        return re.sub(uclear, 'URL省略', text)
    #絵文字チェック
    def remove_emozi(text):
        eclear = r'<:[a-zA-Z0-9_]+:[0-9]+>'
        return re.sub(eclear, '', text)
    #メンションチェック
    def remove_mention18(text):
        mclear = r'<@[0-9]{18}>'
        return re.sub(mclear, '', text)
    def remove_mention19(text):
        mclear = r'<@[0-9]{19}>'
        return re.sub(mclear, '', text)
    #音声合成
    async def generate_wav_file(text, speaker, filepath):
        audio_query = requests.post(f'http://127.0.0.1:50021/audio_query?text={text}&speaker={speaker}')
        headers = {'Content-Type': 'application/json',}
        synthesis = requests.post(
            f'http://127.0.0.1:50021/synthesis?speaker={speaker}',
            headers=headers,
            data=json.dumps(audio_query.json())
        )
        wf = wave.open(filepath, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(synthesis.content)
        wf.close()

@client.event
#BOTが起動したら
async def on_ready():
    global connect
    global voicevoxConnect
    #コンソールにログを送る
    print(f"{client.user} にログインしました。")

    #アクティビティの変更
    await client.change_presence(activity=discord.Game(name='卒研くん.Ver.1.0.2'))

    #treeコマンドの同期
    await tree.sync()

    #VCへの接続の有無
    connect = 0

    voicevoxConnect = VoicevoxConnect()

    #.envファイルから'console_channel_id'を取得する
    channel_id = int(os.getenv('console_channel_id'))
    channel = client.get_channel(channel_id)

    #チャンネルIDがしっかり入っている場合に「コンソールチャンネル」にメッセージを送る
    if channel is not None:
        await channel.send("起動しました。")
    #チャンネルIDが入っていない場合に「コンソール」にエラーを送る
    else:
        print("コンソールチャンネルのIDが正しく入力されていません。.envファイルをご確認ください。")

#shelp
@tree.command(name="shelp",description="ヘルプを表示します。")
async def shelp(interaction: discord.Interaction):
    help = discord.Embed(title="コマンドのヘルプです。")
    help.add_field(name="/shelp",value="このヘルプです。")
    help.add_field(name="/sjoin",value="BOTをボイスチャンネルに接続します。あなたがボイスチャンネルに接続してから使用してください。")
    help.add_field(name="/sspeakers",value="読み上げに使用するVOICEVOXの話者のID一覧表です。（ノーマルのみ）")
    help.add_field(name="/svoicevoxcredits",value="読み上げに使用しているVOICEVOXのクレジット一覧です。")
    help.add_field(name="/sschenge",value="読み上げに使用するVOICEVOXの話者をIDを指定して変更します。先に/sspeakersでIDを確認することをおすすめします。")
    help.add_field(name="/sleave",value="BOTをボイスチャンネルから切断させます。うまく動かないときや終了するときにお試しください。")
    help.add_field(name="/sping",value="BOTのPing値を確認できます。")
    await interaction.response.send_message(embed=help)

#sjoin
@tree.command(name="sjoin",description="BOTをVCに接続します。")
async def sjoin(interaction: discord.Interaction):
    global connect
    global connecting_vcs
    #ボイスチャンネルに接続していない人のコマンドをはじく
    if interaction.user.voice is None:
        await interaction.response.send_message("あなたがVCにいないためBOTを接続できません。\nBOTを接続したいVCに入ってから再度お試しください。")
        return
    # ボイスチャンネルに接続する
    await interaction.user.voice.channel.connect()
    await interaction.response.send_message("接続しました。")
    #メッセージチャンネルを保存するためのフォルダ確認
    if not os.path.isdir(f"serverdata/{interaction.guild_id}"):
        os.makedirs(f"serverdata/{interaction.guild_id}")
    #作成するファイル名を「message_channel.pkl」にする
    filename = f'serverdata/{interaction.guild_id}/message_channel.pkl'
    #dataにmessage_channelを入力する
    data = f'{interaction.channel_id}'
    #先ほど決めたファイル名でファイルを作成する
    with open(filename, 'wb') as f:
        #dataを書き込む
        pickle.dump(data, f)
    #VCに接続したよの「1」
    connect = 1
    connecting_vcs = int(connecting_vcs) + 1
    print("VCに接続されました。\n現在の接続数：", + connecting_vcs)

#sspeakers
@tree.command(name="sspeakers",description="VOICEVOXの話者一覧です。")
async def sspeakers(interaction: discord.Interaction):
    speakers = discord.Embed(title="VOICEVOXの話者一覧です。（ノーマルのみ記載）Ver.0.14.7")
    speakers.add_field(name="四国めたん　ノーマル",value=2)
    speakers.add_field(name="ずんだもん　ノーマル",value=3)
    speakers.add_field(name="春日部つむぎ　ノーマル",value=8)
    speakers.add_field(name="雨晴はう　ノーマル",value=10)
    speakers.add_field(name="波音リツ　ノーマル",value=9)
    speakers.add_field(name="玄野武宏　ノーマル",value=11)
    speakers.add_field(name="白上虎太郎　ふつう",value=12)
    speakers.add_field(name="青山龍星　ノーマル",value=13)
    speakers.add_field(name="冥鳴ひまり　ノーマル",value=14)
    speakers.add_field(name="九州そら　ノーマル",value=16)
    speakers.add_field(name="もち子さん　ノーマル",value=20)
    speakers.add_field(name="剣崎雌雄　ノーマル",value=21)
    speakers.add_field(name="WhiteCUL　ノーマル",value=23)
    speakers.add_field(name="後鬼　人間Ver.",value=27)
    speakers.add_field(name="No.7　ノーマル",value=29)
    speakers.add_field(name="ちび式じい　ノーマル",value=42)
    speakers.add_field(name="櫻歌ミコ　ノーマル",value=43)
    speakers.add_field(name="小夜/SAYO　ノーマル",value=46)
    speakers.add_field(name="ナースロボ＿タイプT　ノーマル",value=47)
    speakers.add_field(name="†聖騎士 紅桜†　ノーマル",value=51)
    speakers.add_field(name="雀松朱司　ノーマル",value=52)
    speakers.add_field(name="麒ヶ島宗麟　ノーマル",value=53)
    speakers.add_field(name="春歌ナナ　ノーマル",value=54)
    speakers.add_field(name="猫使アル　ノーマル",value=55)
    speakers.add_field(name="猫使ビィ　ノーマル",value=58)
    speakers.add_field(name="中国うさぎ　ノーマル",value=61)
    await interaction.response.send_message(embed=speakers)

#svoicevoxcredits
@tree.command(name="svoicevoxcredits",description="読み上げに使用しているVOICEVOXのクレジットです。")
async def svoicevoxcredits(interaction: discord.Interaction):
    credits = discord.Embed(title="VOICEVOXのクレジットです。Ver.0.14.7")
    credits.add_field(name="VOICEVOX:四国めたん",value=2)
    credits.add_field(name="VOICEVOX:ずんだもん",value=3)
    credits.add_field(name="VOICEVOX:春日部つむぎ",value=8)
    credits.add_field(name="VOICEVOX:雨晴はう",value=10)
    credits.add_field(name="VOICEVOX:波音リツ",value=9)
    credits.add_field(name="VOICEVOX:玄野武宏",value=11)
    credits.add_field(name="VOICEVOX:白上虎太郎",value=12)
    credits.add_field(name="VOICEVOX:青山龍星",value=13)
    credits.add_field(name="VOICEVOX:冥鳴ひまり",value=14)
    credits.add_field(name="VOICEVOX:九州そら",value=16)
    credits.add_field(name="VOICEVOX:もち子(cv 明日葉よもぎ)",value=20)
    credits.add_field(name="VOICEVOX:剣崎雌雄",value=21)
    credits.add_field(name="VOICEVOX:WhiteCUL",value=23)
    credits.add_field(name="VOICEVOX:後鬼",value=27)
    credits.add_field(name="VOICEVOX:No.7",value=29)
    credits.add_field(name="VOICEVOX:ちび式じい",value=42)
    credits.add_field(name="VOICEVOX:櫻歌ミコ",value=43)
    credits.add_field(name="VOICEVOX:小夜/SAYO",value=46)
    credits.add_field(name="VOICEVOX:ナースロボ＿タイプＴ",value=47)
    credits.add_field(name="VOICEVOX:†聖騎士 紅桜†",value=51)
    credits.add_field(name="VOICEVOX:雀松朱司",value=52)
    credits.add_field(name="VOICEVOX:麒ヶ島宗麟",value=53)
    credits.add_field(name="VOICEVOX:春歌ナナ",value=54)
    credits.add_field(name="VOICEVOX:猫使アル",value=55)
    credits.add_field(name="VOICEVOX:猫使ビィ",value=58)
    credits.add_field(name="VOICEVOX:中国うさぎ",value=61)
    await interaction.response.send_message(embed=credits)

#sschange
@tree.command(name="sschenge",description="話者をIDを使って変更します")
async def sschenge(interaction: discord.Interaction, speaker:int):
    #話者IDを入力してもらう
    await interaction.response.send_message(speaker)
    #作成するファイルの名前を「ユーザID.pkl」にする
    filename = f'userdata/{interaction.user.id}.pkl'
    #dataにspeakerを入力する
    data = {"sspeaker": speaker}
    #先ほど決めたファイル名でファイルを作成する
    with open(filename,'wb') as f:
        #dataを書き込む
        pickle.dump(data, f)

#音声合成
@client.event
async def on_message(message):
    global connect
    global VoicevoxConnect
    #メッセージがBOTじゃないかチェック
    if message.author.bot:
        return
    #VCに接続してないよの「0」なのでそのまま終了
    if connect == 0:
        return
    #VCに接続してるよの「1」なので音声合成を開始
    if connect == 1:
        #message_channel.pklのファイルパスをnamefileに入れる
        namefile = f'serverdata/{message.guild.id}/message_channel.pkl'
        #namefileで検索する
        with open(namefile, 'rb') as f:
            #message_channelを読み込む
            message_channel = pickle.load(f)
            #message_channelをintに変換
            message_channel = int(message_channel)
        #channel_messageにint型でチャンネルIDを入力
        channel_message = int(f'{message.channel.id}')
        #メッセージが送られたチャンネルがメッセージチャンネルじゃない場合終了
        if not channel_message == message_channel:
            return
        #話者IDの初期設定
        #「3」はずんだもんノーマル
        speaker = 3
        #メッセージを送ったユーザのIDをファイル名に入れる
        filename = f'userdata/{message.author.id}.pkl'
        #メッセージを送ったユーザのspeakerデータがあるか検索する
        #ない場合は初期設定のずんだもん
        if os.path.isfile(filename) == True:
            #filenameで検索する
            with open(filename, 'rb') as f:
                #dataを読み込む
                data = pickle.load(f)
                #speakerにdataの中身のsspeakerを入力する
                speaker = data.get("sspeaker")
        #音声ファイルのパスを入力する
        filepath = f'audio/{message.id}.wav'
        #メッセージをchatに入れる
        chat = message.content
        #絵文字を削除
        chat = VoicevoxConnect.remove_emozi(text=chat)
        #メンションを削除
        chat = VoicevoxConnect.remove_mention18(text=chat)
        chat = VoicevoxConnect.remove_mention19(text=chat)
        #chatが空なら処理を終わる
        if chat == '':
            return
        #メッセージをqueueに追加
        queue.append(message.id)
        #URLを変換
        chat = VoicevoxConnect.remove_url(text=chat)
        #message.content（メッセージ内容）、speaker（話者ID）、filepath（音声ファイルの位置）を使い、最初に作ったVoicevoxConnect.generate_wav_fileを使用する
        await VoicevoxConnect.generate_wav_file(chat, speaker, filepath)
        #再生
        await play(message=message)

#再生待ち
@client.event
async def play(message):
    if not queue is None:
        if message.guild.voice_client.is_playing():
            await asyncio.sleep(0.5)
            await play(message=message)
        play_queue = queue[0]
        del queue[0]
        await message.guild.voice_client.play(discord.FFmpegPCMAudio(executable=os.getenv("ffmpeg_file_path"), source=f"audio/{play_queue}.wav"))
        await asyncio.sleep(1)
        await play(message=message)

#無人時自動切断
@client.event
#VCにアップデートがあった時
async def on_voice_state_update(member, before, after):
    global connect
    global connecting_vcs
    #VCにBOTしかいない場合
    if (member.guild.voice_client is not None and member.id != client.user.id and member.guild.voice_client.channel is before.channel and len(member.guild.voice_client.channel.members) == 1):
        #切断
        await member.guild.voice_client.disconnect()
        connect = 0
        connecting_vcs = int(connecting_vcs) - 1
        print("誰もいなくなったのでVCから自動切断しました。\n現在の接続数：", + connecting_vcs)

#sleave
@tree.command(name="sleave",description="BOTをVCから切断します。")
async def sleave(interaction: discord.Interaction):
    global connect
    global connecting_vcs
    if connect == 0:
            await interaction.response.send_message("BOTがVCにいないため切断できません。")
            return
    if interaction.user.voice is None:
        await interaction.response.send_message("あなたがVCにいないためBOTを切断できません。")
        return
    # 切断する
    #message_channel.pklをnamefileに入れる
    namefile = f'serverdata/{interaction.guild_id}/message_channel.pkl'
    #namefileで検索する
    with open(namefile, 'rb') as f:
        #message_channelを読み込む
        message_channel = pickle.load(f)
        #message_channelをintに変換
        message_channel = int(message_channel)
    #channel_messageにint型でチャンネルIDを入力
    channel_message = int(f'{interaction.channel_id}')
    #メッセージが送られたチャンネルがメッセージチャンネルじゃない場合終了
    if not channel_message == message_channel:
        await interaction.response.send_message("このチャンネルからではBOTを切断できません。\nBOTを起動したチャンネルからもう一度お試しください。")
        return
    connect = 0
    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message("VCから切断しました。")
    connecting_vcs = int(connecting_vcs) - 1
    print("VCからコマンドで切断されました。\n現在の接続数：", + connecting_vcs)
    

#sping
@tree.command(name="sping",description="pingを確認します。")
async def tping(interaction: discord.Interaction):
     # Ping値を秒単位で取得
    raw_ping = client.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)
    # 送信する
    await interaction.response.send_message(f"BotのPing値は{ping}msです。")
    print(f"Pingを送信しました。\n現在のPingは {ping}ms です。")

#sstop
@tree.command(name="sstop",description="Botを停止します。管理者権限が必要です。")
@app_commands.default_permissions(administrator=True)
async def sstop(interaction:discord.Interaction):
    await interaction.response.send_message("Botを停止します。")
    await client.close()

#BOTを起動する
#.envファイルから'TOKEN'を取得する
client.run(os.getenv('TOKEN'), log_handler=handler)
