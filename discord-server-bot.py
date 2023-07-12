import discord
from discord import Option
import boto3
import sys
import os
import keep_alive

# 環境変数から情報を取得
try:
    TOKEN = os.environ['TOKEN']
    DISCORD_SERVER_IDS = int(os.environ['DISCORD_SERVER_IDS'])
    SERVER_CHANNEL = int(os.environ['DISCORD_SERVER_CHANNEL'])
    AWSAccessKeyId = os.environ['AWS_ACCESSKEY_ID']
    AWSSecretKey = os.environ['AWS_SECRET_KEY']
    AWSInstanceID = os.environ['AWS_INSTANCE_ID']
except KeyError as e:
     print(f"{e} : 環境変数の取得に失敗しました。環境変数が設定されているか確認してください。")

ec2 = boto3.resource('ec2',
        aws_access_key_id = AWSAccessKeyId,
        aws_secret_access_key = AWSSecretKey ,
        region_name ='ap-northeast-1'
)
instance = ec2.Instance(AWSInstanceID)
 
keep_alive.keep_alive()
client = discord.Bot()
 
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    await client.get_channel(SERVER_CHANNEL).send(f"BOTがオンラインになりました")
    print(f"{client.user} コマンド待機中...")
 
# サーバ起動コマンド
@client.slash_command(description="サーバ起動コマンド", guild_ids=[DISCORD_SERVER_IDS])
async def start(
    ctx: discord.ApplicationContext,
):
    name = ctx.author.name
    await ctx.respond(f"Hi {name} ! \n GNMK's 7Days to Dieサーバを起動します。")
    try:
        ins_state_code = instance.state.get('Code')
        ins_state_name = instance.state.get('Name')
        # インスタンスのステートが停止であればサーバ起動処理を実施する。
        if instance.state.get('Code') == 80:
            instance.start()
            instance.wait_until_running()
            ip = instance.public_ip_address
            await ctx.respond(f"サーバが起動しました！ \n サーバ名：GNMK_7DtD_Serverか \n IP：{ip}で接続してね！")
        elif instance.state.get('Code') == 0:
            # インスタンスのステートが保留中
            await ctx.respond(f"現在サーバを起動している途中だよ！ \n もう少し待ったらBOTから反応があるよ！")
        elif instance.state.get('Code') == 16:
            # インスタンスのステートが起動済み
            ip = instance.public_ip_address
            await ctx.respond(f"すでにサーバが起動してるよ！ \n サーバ名：GNMK_7DtD_Serverか \n IP：{ip}で接続してね！")
        elif instance.state.get('Code') == 64:
            # インスタンスのステートが停止中
            await ctx.respond(f"現在サーバを停止している途中だよ！ \n サーバを起動したい場合は少し待ってから「/start」してね！")
        else:
            # それ以外はインスタンスが削除されている可能性があるためその旨を返却
            await ctx.respond(f"サーバが削除されている可能性があります！ \n mixelPooooooに問い合わせてね。 \n Error! state:{ins_state_name}")
    except:
            await ctx.respond(f"サーバの起動に失敗しました…。mixelPooooooに問い合わせてね。")
    return

# サーバ停止コマンド
@client.slash_command(description="サーバ停止コマンド", guild_ids=[DISCORD_SERVER_IDS])
async def stop(
    ctx: discord.ApplicationContext,
):
    name = ctx.author.name
    await ctx.respond(f"Hi {name} ! \n GNMK's 7Days to Dieサーバを停止します。")
    try:
        # インスタンスのステートが停止であればサーバ起動処理を実施する。
        if instance.state.get('Code') == 16:
            instance.stop()
            instance.wait_until_stopped()
            await ctx.respond(f"サーバが停止しました！ \n ご利用ありがとうございました！")
        else:
            await ctx.respond(f"サーバが停止中か既に停止されています！ \n そのためもう停止を行う必要はありません！")
    except:
            await ctx.respond(f"サーバの停止に失敗しました…。mixelPooooooに問い合わせてね。")
    return
 
client.run(TOKEN)