import discord
import random
import asyncio
import morse_talk as morse
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

fullTab = pd.read_csv('tab.csv')
pd.options.display.float_format = '{:.0f}'.format

log_text = 'logs.txt'

@client.event
async def on_ready():
    print(f"Bot has been lunched as {client.user}")
@client.event
async def on_message(message):
    sent_date = message.created_at
    formatted_date = sent_date.strftime("%Y-%m-%d %H:%M:%S")
    global reminder_switch

    if message.author.bot:
        return
    with open(log_text, 'a', encoding='utf-8') as file:
        file.write(f'[{message.guild.id}]({message.guild.name}) in [{message.channel.id}]:({message.channel.name}) at {formatted_date} | [{message.author.id}]:{message.author.name} => {message.content}\n')
    if message.content.startswith('??encode'):
        args = message.content.split("::")
        result = args[1]
        await message.reply(morse.encode(result))
    if message.content.startswith('??decode'):
        args = message.content.split("::")
        result = args[1]
        await message.reply(morse.decode(result))
    if message.content.startswith('!ball'):
        rep = ['yes', 'no', 'probably', 'nchallah']
        if (message.content == '!ball'):
            await message.reply('please include an additional argument')
        else:
            await message.reply(f"""
            > {rep[random.randint(0, len(rep) - 1)]}
            """)
    if message.content.startswith('!T>'):
        args = message.content.split(' ')
        if(len(args) < 5):
            await message.reply('Missing arguments')
        gangChannel = client.get_channel(int(args[4]))
        reminder_switch = True
        await message.reply(f'reminder set! will start in {args[1]} secs and loops each {args[2]} secs, {args[3]} times.')
        await asyncio.sleep(int(args[1]))
        if reminder_switch:
            for i in range(int(args[3])):
                await gangChannel.send('@everyone BigData!')
                await gangChannel.send(f'{int(args[3])-(i+1)} reminds remaining')
                if not reminder_switch:
                    break
                await asyncio.sleep(int(args[2]))
        await gangChannel.send('End of reminders')
    elif message.content.startswith('!S>'):
        reminder_switch = False
        await message.reply('stop reminders command executed successfully')
    if message.content == '??help':
        await message.reply(
        """
        Search by serial number:
        `??searchbyserial::query` ex: `??searchbyserial::1919` (You can input full serial)
        
        Search by name:
        `??searchbyname::query` ex: `??searchbyserial::faiz` (You can input something like: "fai" in case you don't remember their name correctly)
        
        Search by surname:
        `??searchbysurname::query` ex: `??searchbysurname::tchekiken` (You can input something like: "tch" in case you don't remember their surname correctly)
        
        Search by group:
        `??searchbygroup::query` ex: `??searchbygroup::1`
        """
        )
    if message.content.startswith('??searchbyserial'):
        args = message.content.split("::")
        query = args[1]
        print(type(query), query)
        fullTab['matricule'] = fullTab['matricule'].astype(str)
        for i in range(0, len(fullTab[fullTab['matricule'].str.contains(query)]), 5):
            chunk = fullTab[fullTab['matricule'].str.contains(query)][i:i+5]
            print(chunk)
            await message.reply(chunk)
    if message.content.startswith('??searchbysurname'):
        args = message.content.split("::")
        query = args[1]
        await message.reply(fullTab[fullTab['nom'].str.contains(query.upper())])
    if message.content.startswith('??searchbyname'):
        args = message.content.split("::")
        query = args[1]
        await message.reply(fullTab[fullTab['prenom'].str.contains(query.upper())])
    if message.content.startswith('??searchbygroup'):
        args = message.content.split("::")
        query = args[1]
        for i in range(0, len(fullTab.query(f"groupe == {int(query)}")), 5):
            chunk = fullTab.query(f"groupe == {int(query)}")[i:i + 5]
            await message.reply(chunk)


client.run(TOKEN)

