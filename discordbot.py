import os
import discord
from discord import app_commands

token = os.environ['DISCORD_BOT_TOKEN']

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await tree.sync()


@tree.command(name="ping", description="Ping pong!")
async def ping(interaction: discord.Interaction, arg: int):
    await interaction.response.send_message("pong!\n" * arg)


@tree.command(name="join", description="通話チャンネルに接続")
async def join(interaction: discord.Interaction):
    guild = interaction.guild
    if guild.voice_client:
        await guild.voice_client.disconnect()
    if interaction.author.voice is None:
        await interaction.response.send_message("通話チャンネルに接続してください")
        return
    await interaction.author.voice.channel.connect()
    await interaction.response.send_message("接続しました")


@tree.command(name="leave", description="通話チャンネルから退出")
async def leave(interaction: discord.Interaction):
    guild = interaction.guild
    if guild.voice_client:
        await guild.voice_client.disconnect()
        await interaction.response.send_message("退出しました")
    else:
        await interaction.response.send_message("通話チャンネルに接続していません")

@tree.command(name="play", description="こんにちは")
async def play(interaction: discord.Interaction):
    voice_client = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if voice_client and voice_client.is_connected():
        audio_source = discord.FFmpegPCMAudio("/home/azureuser/audio.wav")
        voice_client.play(audio_source)

@client.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return
    if before.channel is None and after.channel is not None:
        await after.channel.connect()
    if before.channel is not None and after.channel is None:
        if len(before.channel.members) == 1 and before.channel.guild.voice_client:
            await before.channel.guild.voice_client.disconnect()

client.run(token)
