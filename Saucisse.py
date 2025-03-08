import os
from typing import Final
import discord
from dotenv import load_dotenv
from responses import get_response
from rythme_function import get_video,get_video_with_link,download_video
import asyncio

"""
déclaration des variables 
"""
code_path =  'C:/Users/Malo/Documents/bot_Saucisse/ '
queue = []
n= 0
vc = 0
voice_channel = ''
play_status = 'off'
ffmpeg_path = "C:/Users/Malo/Desktop/ffmpeg-n7.0-latest-win64-lgpl-7.0/bin/ffmpeg.exe"

load_dotenv()
token = os.getenv('DISCORD_TOKEN')


# set up the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


#messages functionality
async def send_message(message,user_message):
    if not user_message:
        print('message was empty becaus intents were not enabled probably')
        return
    if is_private := (user_message[:3] == '///' or user_message == 'help') :
        if user_message[:3] == '///':
            user_message = user_message[3:]
    try:
        response = get_response(user_message)
        if response != '':
            await message.author.send(response) if is_private else await message.channel.send(response)
    
    except Exception as e:
        print(e)

async def skip(message):
    global n,queue,play_status,vc
    voice_channel = message.author.voice.channel
    await vc.disconnect()
    vc = await voice_channel.connect()
    await jouer_queue(vc)
    n = 0
    queue = []
    play_status = 'off'
    await vc.disconnect()


async def del_cur_song(message,index):
    global n,queue,play_status,vc
    voice_channel = message.author.voice.channel
    os.remove(queue[index-1])
    queue.pop(index-1)
    n-=1
    await vc.disconnect()
    vc = await voice_channel.connect()
    await jouer_queue(vc)
    n = 0
    queue = []
    play_status = 'off'
    await vc.disconnect()

async def in_channel(message,command):
    global queue,n,vc,play_status
    if command == "!!skip":
        await skip(message)
    elif queue != [] and len(queue)==1 and play_status=='off':
        play_status = 'on'
        print('play status : ' + play_status)
        voice_channel = message.author.voice.channel
        vc = await voice_channel.connect()
        print('cinnected')
        await jouer_queue(vc)
        print('nique')
        n = 0
        queue = []
        await vc.disconnect()
        play_status = 'off'
    elif command == '!!n':
        await message.channel.send(n)
    elif command == '!!quite':
        await quit_queue()
    elif command == '!!clear':
        clear_queue()
    elif command == '!!off':
        play_status == '!!off'
    elif command == '!!loop':
        play_status = 'loop'
        for i in range(n):
            download_video(queue[i])
    elif command == '!!state':
        await message.channel.send(play_status)
    elif command[:8] == '!!remove':
        try:
            index = int(command[8:])
            
            if index == n+1:
                await del_cur_song(message,index)
            elif index > n+1:
                os.remove(queue[index-1])
                queue.pop(index-1)
            if play_status == 'loop':
                if index < n+1:
                    os.remove(queue[index-1])
                    queue.pop(index-1)
                    n-=1
            else:
                if index < n+1:
                    queue.pop(index-1)
                    n-=1
            
        except Exception as e:
            print(e)


async def quit_queue():
        global n,queue,play_status
        await vc.disconnect()
        if play_status == 'loop':
            for i,j in enumerate(queue):
                os.remove(j)
        else:
            if n != len(queue):
                for i,j in enumerate(queue[1:]):
                    os.remove(j)
        n = 0
        queue = []
        play_status = 'off'

def clear_queue():
    global queue,n
    queue = []
    n = 0

async def connect_to_a_channel(channel):
    vc = await channel.connect()
    await jouer_queue(vc)
    global queue
    queue = []
    n = 0
    await vc.disconnect()


async def ajouter_queue(ctx,user_message):
    if user_message[:6] == '!!play':
        user_message =  user_message[6:]
        for i,j in enumerate (user_message):
            if j == ' ':
                user_message = user_message[:i] + '+'+ user_message[i+1:] 
        path = get_video(user_message)
        queue.append(path)
        await ctx.channel.send(f' **{path[37:-4]}** ajouté a la queue!!')
        voice_channel = ctx.author.voice.channel
        if voice_channel == None:
            await ctx.send("entre dans un vc enculé")
            return False
        print(queue)
        return voice_channel
    elif user_message[:6] == '!!link':
        user_message =  user_message[6:]
        path = get_video_with_link(user_message)
        queue.append(path)
        await ctx.channel.send(f' **{path[37:-4]}** ajouté a la queue!!')
        voice_channel = ctx.author.voice.channel
        if voice_channel == None:
            await ctx.send("entre dans un vc enculé")
            return False
        print(queue)
        return voice_channel

async def play_salom(message, user_message):
    global play_status
    if user_message[:7] == '!!salom':
        if play_status=='on':
            quit_queue()
        play_status = 'on'
        voice_channel = message.author.voice.channel
        vc = await voice_channel.connect()
        audio = get_video_with_link('https://www.youtube.com/watch?v=4Fge4EPiKA0')
        vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_path,source= audio))
        while vc.is_playing():
            await asyncio.sleep(1)
        os.remove(audio)
        await vc.disconnect()
        play_status = 'off'





async def jouer_queue(vc):
    global n 
    print("ok on joue la queue")
    if len(queue) == n and play_status == 'on':
        print("exit")
        return
    elif len(queue) == n and play_status == 'loop':
        n = 0
    audio = f'{queue[n]}'
    vc.play(discord.FFmpegPCMAudio(executable=ffmpeg_path,source= audio))
    while vc.is_playing():
        await asyncio.sleep(1)
    if play_status != 'loop':
        os.remove(audio)
    if play_status != 'off':
        n+=1    
    await jouer_queue(vc)

async def print_queue(message,user_message):
    if user_message == '!!queue':
        str = 'queue\n'
        for  i,j in enumerate(queue):
            str += f"""* ***{i+1} ---> {j[37:-4]}***\n"""
        await message.channel.send(str)
    
#reactiuon functionality

async def send_reacion(message,user_message):
    if 'saucisse' in user_message:
        await message.channel.send('<:saucisse:1184936192496648326>')

#step 3 handeling the startup for our bot
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

#step 4 handeling incoming messages 

@client.event
async def on_message(message):
    global voice_channel
    if message.author == client.user:
        return 
    username= str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f'[{channel}] {username} : {user_message}')


    await send_message(message,user_message)
    await send_reacion(message, user_message)
    voice_channel = await ajouter_queue(message,user_message)
    await in_channel(message,user_message)
    await print_queue(message,user_message)
    await play_salom(message,user_message)


#step 5 main entry point 
def main():
    client.run(token)


if __name__ == '__main__':
    main()