import json
import datetime
import discord
import os

debug = False

intents = discord.Intents.all()

client = discord.Client(intents = intents)

PATH = './settings.json'

if debug:
    PATH = "./test_settings.json"

BOT_SETTINGS = {"PLAYING": "", "TOKEN": ""}
SERVER_SETTINGS = {"": {"TEXT": 0, "VOICE": [0, 0], "PREFIX": "??"}}

CHANNELS = {}

GUILDS = {}

#jsonファイルへ[の書き出し
def save():
    file = open(PATH, 'w')
    temp = {"BOT":{}, "SERVER":{}}
    for i in BOT_SETTINGS:
        temp["BOT"][i] = BOT_SETTINGS[i]
    for i in SERVER_SETTINGS:
        temp["SERVER"][i] = SERVER_SETTINGS[i]
    json.dump(temp, file)

#jsonファイルの読み込み
def load():
    global BOT_SETTINGS, SERVER_SETTINGS
    file = open(PATH, "r")
    temp = json.load(file)
    for i in temp["BOT"]:
        BOT_SETTINGS[i] = temp["BOT"][i]
    for i in temp["SERVER"]:
        SERVER_SETTINGS[i] = temp["SERVER"][i]

load()

#CHANNELS辞書のアップデート
def update_channels():
    global CHANNELS
    for channel in client.get_all_channels():
        CHANNELS[channel.id] = str(channel.name)
    print("チャンネル辞書更新")
    #print(CHANNELS)

#サーバー辞書のアップデート
def update_guilds():
    global GUILDS
    for guilds in client.guilds:
        GUILDS[str(guilds.id)] = guilds.name
    print("サーバー辞書更新")
    #print(GUILDS)

#初参加サーバーに初期設定を適用
def initialize():
    global SERVER_SETTINGS
    temp_list = []
    for i in GUILDS:
        if not i in SERVER_SETTINGS:
            SERVER_SETTINGS[i] = {}
            SERVER_SETTINGS[i]["TEXT"] = 0
            SERVER_SETTINGS[i]["VOICE"] = []
            SERVER_SETTINGS[i]["PREFIX"] = "??"
            temp_list.append(i)
    print("初期化完了")
    #print(temp_list)

#removeprefixのやつ
def rmprefix(content, prefix):
    content = content.removeprefix(prefix)
    content = content.removeprefix(' ')
    return content

@client.event
async def on_ready():
    print("ログイン成功")
    await client.change_presence(activity = discord.Activity(name=str(BOT_SETTINGS["PLAYING"]), type=discord.ActivityType.playing))
    update_channels()
    update_guilds()
    initialize()

@client.event
async def on_message(message):
    global BOT_SETTINGS, SERVER_SETTINGS
    if message.author.bot:
        return

    if not message.guild.id in GUILDS:
        initialize()

    if message.content.startswith(SERVER_SETTINGS[str(message.guild.id)]["PREFIX"]):
        print(">> " + message.content)
        content = message.content.removeprefix(SERVER_SETTINGS[str(message.guild.id)]["PREFIX"])
        #"??set"の時
        if content.startswith("set"):
            content = rmprefix(content, "set")

            if content == '':
                await message.channel.send(f"チャンネルを指定してください\n例) {SERVER_SETTINGS[str(message.guild.id)]['PREFIX']} set `チャンネル名`")
                return
            if content.startswith("id"):
                content = rmprefix(content, "id")
                if content == '':
                    await message.channel.send(f"IDを指定してください\n例) {SERVER_SETTINGS[str(message.guild.id)]['PREFIX']} set id `チャンネルID`")
                    return
                id = int(content)
                if not id in CHANNELS:
                    await message.channel.send(f"`{content}`は存在しません")
                    print("存在しないチャンネル")
                    return
                name = client.get_channel(id).name
            else:
                id = 0
                #チャンネル名をIDに変換
                for i in CHANNELS:
                    if content == CHANNELS[i]:
                        id = i
                        name = content
                #id == 0 存在しない時
                if id == 0:
                    await message.channel.send(f"`{content}`は存在しません")
                    print("存在しないチャンネル")
                    return
            
            if str(client.get_channel(id).type) == 'voice':
                if(id in SERVER_SETTINGS[str(message.guild.id)]["VOICE"]):
                    await message.channel.send(f"`{name}`はすでに監視対象です")
                    print("すでに監視対象")
                    return
                SERVER_SETTINGS[str(message.guild.id)]["VOICE"].append(id)
                await message.channel.send(f"`{name}`を監視対象に追加しました")
                print("監視対象に追加")
                return
            #引数がテキストチャンネルの場合
            if str(client.get_channel(id).type) == 'text':
                SERVER_SETTINGS[str(message.guild.id)]["TEXT"] = id
                await message.channel.send(f"`{name}`にVC通知を送信します")
                print("送信先変更")
                return
            #VCでもテキストでもない場合
            await message.channel.send(f"`{name}`は定義外のチャンネル`{client.get_channel(id).type}`です\nこれは想定外のエラーです。管理者に報告してください。")
            print("激ヤバエラー")
            return

        #"??remove"の時
        if content.startswith("remove"):
            content = rmprefix(content, "remove")

            if content == '':
                await message.channel.send(f"チャンネルを指定してください\n例) {SERVER_SETTINGS[str(message.guild.id)]['PREFIX']} remove `チャンネル名`")
                return

            if content.startswith("id"):
                content = rmprefix(content, "id")
                if content == '':
                    await message.channel.send(f"IDを指定してください\n例) {SERVER_SETTINGS[str(message.guild.id)]['PREFIX']} set id `チャンネルID`")
                    return
                id = int(content)
                if not id in CHANNELS:
                    await message.channel.send(f"`{content}`は存在しません")
                    print("存在しないチャンネル")
                    return
                name = client.get_channel(id).name
            else:
                id = 0
                #チャンネル名をIDに変換
                for i in CHANNELS:
                    if content == CHANNELS[i]:
                        id = i
                        name = content
                #id == 0 存在しない時
                if id == 0:
                    await message.channel.send(f"`{content}`は存在しません")
                    print("存在しないチャンネル")
                    return

            if str(client.get_channel(id).type) == 'voice':
                for j in range(len(SERVER_SETTINGS[str(message.guild.id)]["VOICE"])):
                    if id == SERVER_SETTINGS[str(message.guild.id)]["VOICE"][j]:
                        SERVER_SETTINGS[str(message.guild.id)]["VOICE"].pop(j)
                        await message.channel.send(f"`{name}`を監視対象から削除")
                        print("監視対象から削除")
                        return
                #SETTINGS["VOICE"]に入ってない時
                await message.channel.send(f"`{name}`は監視対象ではありません")
                print("監視対象ではない")
                return
            #vcじゃなかった時
            await message.channel.send(f"`{name}`はテキストチャンネルです")
            print("テキストチャンネルだった")
            return

        if content == "save":
            save()
            await message.channel.send("現在の設定をサーバーに保存しました")

        if content == "status":
            embed = discord.Embed(title=os.path.basename(__file__),description=f"取得チャンネル数: {len(CHANNELS)}")
            textchannel = ''
            textchannel = f"<#{SERVER_SETTINGS[str(message.guild.id)]['TEXT']}>"
            if textchannel == '<#0>':
                textchannel = "なし"
            embed.add_field(name="通知送信先",value=textchannel,inline=False)
            voicechannel = ''
            for i in SERVER_SETTINGS[str(message.guild.id)]["VOICE"]:
                voicechannel += f"<#{i}> "
            if voicechannel == '':
                voicechannel = "なし"
            embed.add_field(name="監視対象VC",value=voicechannel,inline=False)
            embed.set_footer(text="hyouhyan.com")

            await message.channel.send(embed=embed)
            return
        
        if content == "status id":
            embed = discord.Embed(title=os.path.basename(__file__),description=f"取得チャンネル数: {len(CHANNELS)}")
            textchannel = ''
            textchannel = f"{SERVER_SETTINGS[str(message.guild.id)]['TEXT']}"
            if textchannel == '0':
                textchannel = "なし"
            embed.add_field(name="通知送信先",value=textchannel,inline=False)
            voicechannel = ''
            for i in SERVER_SETTINGS[str(message.guild.id)]["VOICE"]:
                voicechannel += f"{i} "
            if voicechannel == '':
                voicechannel = "なし"
            embed.add_field(name="監視対象VC",value=voicechannel,inline=False)
            embed.set_footer(text="hyouhyan.com")

            await message.channel.send(embed=embed)
            return
        
        if content == "reboot" or content == "shutdown":
            await message.channel.send("シャットダウンしています…")
            exit()
        
        if content.startswith("prefix"):
            content = rmprefix(content, "prefix")
            if content == '':
                await message.channel.send(f'接頭語を指定してください\n例)`{SERVER_SETTINGS[str(message.guild.id)]["PREFIX"]}prefix !!`')
                return
            SERVER_SETTINGS["PREFIX"] = content
            await message.channel.send(f'接頭語を{SERVER_SETTINGS[str(message.guild.id)]["PREFIX"]}に変更しました')
            return

        if content.startswith('suteme'):
            content = rmprefix(content, "suteme")
            BOT_SETTINGS["PLAYING"] = content
            await client.change_presence(activity = discord.Activity(name=str(BOT_SETTINGS["PLAYING"]), type=discord.ActivityType.playing))
            await message.channel.send(f'ステータスを`{BOT_SETTINGS["PLAYING"]}`に変更しました')
            return

        if content.startswith("send"):
            content = rmprefix(content, "send")
            if content == '':
                await message.channel.send(f'{SERVER_SETTINGS[str(message.guild.id)]["PREFIX"]} send `id` `送信する内容`')
                return

            content = content.split(' ')
            id = int(content[0])
            content.pop(0)

            botRoom = client.get_channel(id)
            for i in content:
                new_content = i + ' '

            await botRoom.send(new_content)
            await message.channel.send(f'<#{id}>に`{new_content}`を送信しました')
            return

        if content.startswith("yummy"):
            await message.channel.send('美味しいヤミー❗️✨🤟😁👍✨⚡️感謝❗️🙌✨感謝❗️🙌✨またいっぱい食べたいな❗️🥓🥩🍗🍖😋🍴✨デリシャッ‼️🙏✨ｼｬ‼️🙏✨ ｼｬ‼️🙏✨ ｼｬ‼️🙏✨ ｼｬ‼️🙏✨ ｼｬ‼️🙏✨ ｼｬｯｯ‼😁🙏✨ハッピー🌟スマイル❗️❗️💥✨👉😁👈⭐️')
            return

            
@client.event
async def on_voice_state_update(member, before, after):
 
    # チャンネルへの入室ステータスが変更されたとき（ミュートON、OFFに反応しないように分岐）
    if before.channel != after.channel:
        print("アプデ!!")
        #print(before)
        #print(after)
        send = False

        # 退室通知
        if before.channel is not None and before.channel.id in SERVER_SETTINGS[str(client.get_channel(before.channel.id).guild.id)]["VOICE"]:
            print(f"退出 {member.name} {before.channel}")
            embed = discord.Embed(title=f"{member.display_name}が「{before.channel.name}」から退出しました", color=discord.Colour.red())
            botRoom = client.get_channel(SERVER_SETTINGS[str(client.get_channel(before.channel.id).guild.id)]["TEXT"])
            send = True
        # 入室通知
        if after.channel is not None and after.channel.id in SERVER_SETTINGS[str(client.get_channel(after.channel.id).guild.id)]["VOICE"]:
            print(f"参加 {member.name} {after.channel}")
            embed = discord.Embed(title=f"{member.display_name}が「{after.channel.name}」に参加しました", color=discord.Colour.green())
            botRoom = client.get_channel(SERVER_SETTINGS[str(client.get_channel(after.channel.id).guild.id)]["TEXT"])
            send = True
        if send:
            embed.set_author(name=member.name,icon_url=member.avatar.url)
            embed.set_footer(text=datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
            await botRoom.send(embed=embed)
 
@client.event
async def on_guild_channel_update(before, after):
    print("チャンネル名変わったよー")
    update_channels()

@client.event
async def on_guild_channel_create(channel):
    print("チャンネル作られたよー")
    update_channels()

@client.event
async def on_guild_channel_delete(channel):
    print("チャンネル消されたよー")
    update_channels()
    print(SERVER_SETTINGS[str(channel.guild.id)]["VOICE"])
    if channel.id in SERVER_SETTINGS[str(channel.guild.id)]["VOICE"]:
        for i in range(SERVER_SETTINGS[str(channel.guild.id)]["VOICE"]):
            if SERVER_SETTINGS[str(channel.guild.id)]["VOICE"][i] == channel.id:
                SERVER_SETTINGS[str(channel.guild.id)]["VOICE"].pop(i)

@client.event
async def on_guild_join(guild):
    print(f"{guild}に参加したよー")
    update_guilds()
    update_channels()
    initialize()

@client.event
async def on_guild_remove(guild):
    print(f"{guild}から消されたよー")
    update_guilds()
    update_channels()

client.run(BOT_SETTINGS["TOKEN"])