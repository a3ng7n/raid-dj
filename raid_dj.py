from pygtail import Pygtail
import time
import os
import discord
import asyncio
import time

import raid_dj_defaults

if not raid_dj_defaults.token:





client = discord.Client()

# general = 225860068661264394
# bot_test = 604066168155799687

async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed():
        log_events = []
        
        while 1:
            
            for line in Pygtail(filename="C:\Program Files (x86)\World of Warcraft\_retail_\Logs\WoWCombatLog.txt",
                                read_from_end=True):
                if ("ENCOUNTER_START" in line):
                    log_events.append(["ENCOUNTER_START", line, time.time()])
                    print('found encounter start')
                elif ("ENCOUNTER_END" in line):
                    log_events.append(["ENCOUNTER_END", line, time.time()])
                    print('found encounter end')
            
            if log_events:
                check_time = time.time()
                if (check_time - log_events[-1][2]) > 2:
                    await client.get_channel(604066168155799687).send(str(log_events))
                    log_events = []
                else:
                    print('found event, but not waiting long enough '+str(check_time)+' '+str(log_events[-1][2]))
            else:
                print('no log event found')
            
            time.sleep(1)

@client.event
async def on_message(message):
    print("message seen")

@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(activity=discord.Game(name="The Waiting Game"))

client.loop.create_task(my_background_task())
client.run('NTU0MTU5OTg3MDM1ODY1MDg5.XTvcyg.Fzt_geDx2qE2DsenLLlc9GC_GY8')