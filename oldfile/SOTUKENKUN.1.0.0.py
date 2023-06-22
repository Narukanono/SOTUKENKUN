import discord
from discord import app_commands
import logging
import os
from dotenv import load_dotenv
import requests
import json
import wave
import pickle

#envファイルの読み込み
load_dotenv()

#speakerのユーザデータを保存するdataというフォルダが無いことの確認
if not os.path.isdir("./data"):
    #無いので作成
    os.makedirs("./data")

#ログファイルの作成（古いものは上書きされます）
handler = logging.FileHandler(filename='sotukenkun.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
client =  discord.Client(intents=intents)
intents.message_content = True
tree = app_commands.CommandTree(client)

#音声合成用class
class VoicevoxConnect():
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
    await client.change_presence(activity=discord.Game(name='卒研くん.Ver.1.0.0'))

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
        print(f"コンソールチャンネルのIDが正しく入力されていません。.envファイルをご確認ください。")

#help
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

#join
@tree.command(name="sjoin",description="BOTをVCに接続します。")
async def join(interaction: discord.Interaction):
    global connect
    #ボイスチャンネルに接続していない人のコマンドをはじく
    if interaction.user.voice is None:
        await interaction.response.send_message("あなたがVCにいないためBOTを接続できません。\nBOTを接続したいVCに入ってから再度お試しください。")
        return
    # ボイスチャンネルに接続する
    await interaction.user.voice.channel.connect()
    await interaction.response.send_message("接続しました。")
    #VCに接続したよの「1」
    connect = 1

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
    filename = f'data/{interaction.user.id}.pkl'
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
        #話者IDの初期設定
        #「3」はずんだもんノーマル
        speaker = 3
        #メッセージを送ったユーザのIDをファイル名に入れる
        filename = f'data/{message.author.id}.pkl'
        #先ほど入れたファイル名で検索する
        with open(filename, 'rb') as f:
            #dataを読み込む
            data = pickle.load(f)
            #speakerにdataの中身のsspeakerを入力する
            speaker = data.get("sspeaker")
        #音声ファイルのパスを入力する
        filepath = './audio.wav'
        #message.content（メッセージ内容）、speaker（話者ID）、filepath（音声ファイルの位置）を使い、最初に作ったVoicevoxConnect.generate_wav_fileを使用する
        await VoicevoxConnect.generate_wav_file(message.content, speaker, filepath)
        if (message.guild.voice_client.is_playing()):
            return
        #ffmpegを使用して音声合成したファイルを再生する
        message.guild.voice_client.play(discord.FFmpegPCMAudio(executable=os.getenv("ffmpeg_file_path"), source=filepath))

#無人時自動切断
@client.event
#VCにアップデートがあった時
async def on_voice_state_update(member, before, after):
    #VCにBOTしかいない場合
    if (member.guild.voice_client is not None and member.id != client.user.id and member.guild.voice_client.channel is before.channel and len(member.guild.voice_client.channel.members) == 1):
        #切断
        await member.guild.voice_client.disconnect()

#leave
@tree.command(name="sleave",description="BOTをVCから切断します。")
async def leave(interaction: discord.Interaction):
    global connect
    if connect == 0:
            await interaction.response.send_message("BOTがVCにいないため切断できません。")
            return
    if interaction.user.voice is None:
        await interaction.response.send_message("あなたがVCにいないためBOTを切断できません。")
        return
    # 切断する
    connect = 0
    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message("VCから切断しました。")

#sping
@tree.command(name="sping",description="pingを確認します。")
async def test(interaction: discord.Interaction):
     # Ping値を秒単位で取得
    raw_ping = client.latency
    # ミリ秒に変換して丸める
    ping = round(raw_ping * 1000)
    # 送信する
    await interaction.response.send_message(f"BotのPing値は{ping}msです。")

#BOTを起動する
#.envファイルから'TOKEN'を取得する
client.run(os.getenv('TOKEN'), log_handler=handler)
