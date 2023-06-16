# SOTUKENKUN
卒業研究で作っているBOTの記録です。<br>
ふ～ん程度に見てもらえると嬉しいです！<br>
<br>
[サポートサーバー](https://discord.gg/GdxpBmbdG7)（Discord）
## 理想の完成像
やりたいこと
- **大前提としてDiscordのBOTを作成する**
- VOICE VOXを使用したVC読み上げを作成する
- ユーザーごとに声を変えられるようにする
- /コマンドに対応する。
- その他の便利機能も時間が許してくれる限り作りたい
## バージョン情報
最新バージョン Ver.0.9.0<br>
**これは完全版(正式リリース)ではありません**
## .envファイルについて
Ver.0.0.5のアップデートからトークンと簡易コンソールチャンネルを.envファイルから読み取るように変更しました。<br>
そのため、今後の利用には.pyファイルはいじらずに.envファイルを作成してもらう必要がございます。<br>
書き方は下記をご覧ください。<br>
<br>
.envファイルの書き方
・新しいファイルを作成し、「.env」というファイルを作成してください。
＝＝＞ファイルに名前はつけないでください。拡張子のみでないと動きません。ダメな例「example.env」
・書くものというところを書いてください(your~hereのところは各自変えてください)
```env:.env
console_channel_id=your_console_channel_here
ffmpeg_file_path='your_ffmpeg_exefile_path_here'
TOKEN='your_token_here'
```
| 書くもの | 役割 |
| :--- | :--- |
| console_channel_id=your_console_channel_here | 簡易コンソールチャンネル |
| ffmpeg_file_path='your_ffmpeg_exefile_path' | 音声の再生に必要なffmpegのexeファイルのパス（必ず「ffmpeg.exe」まで入れてください） |
| TOKEN='your_token_here' | トークン |
## バージョンごとの変更点
### 最新リリース
| Ver.0.9.0 |
| :--- |
| helpコマンドを追加しました。 |
| VOICEVOXによる読み上げに対応しました。それに伴い下記の2コマンドが追加されました。 |
| speakersコマンドを追加しました。 |
| schengeコマンドを追加しました。 |
| pingコマンドとほぼ変わらないためtestコマンドを削除しました。 |
### 旧リリース
| Ver.0.0.7 |
| :--- |
| スラッシュコマンドに対応しました。 |
| $コマンドをなくしました。 |
| ステータスを「卒業研究」から「卒研くん」へ変更しました。 |
####
| Ver.0.0.6 |
| :--- |
| コマンドの実装方法を変更しました。 |
| => on_messageからcommandsへ |
####
| Ver.0.0.5 |
| :--- |
| トークンと簡易コンソールチャンネルのIDを.envファイルに移動しました。 |
| 「卒業研究.Ver.0.0.5をプレイ中」と表示されるようになりました。 |
| コマンドを「！」から「＄」に変更しました。 |
####
| Ver.0.0.4 |
| :--- |
| 動くようになりました。 |
| BOTのログイン時にコンソールチャンネルに「login success」と送信するようになりました。 |
| 「!join」「!leave」「!ping」「!test」コマンドを追加しました。 |
####
| Ver.0.0.3 |
| :--- |
| **コマンド異常で動きません。** |
| ボイスチャンネルに接続・切断できるようにしました。(コマンド異常) |
| testコマンドを追加しました。 |
####
| Ver.0.0.2 |
| :--- |
| 簡単なログが出るようになりました。 |
####
| Ver.0.0.1 |
| :--- |
| [Discord.py](https://discordpy.readthedocs.io/ja/latest/quickstart.html)そのままです。() |
## VOICEVOXのクレジット
使用しているVOICEVOCのクレジットはファイル[voicevox_credit.txt](https://github.com/Narukanono/SOTUKENKUN/blob/main/voicevox_credit.txt)をご覧ください。
