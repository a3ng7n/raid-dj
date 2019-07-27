from pygtail import Pygtail
import time
import os
import discord
import asyncio

client = discord.Client()

# general = 225860068661264394
# bot_test = 604066168155799687

async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed():
        while 1:
            
            with open("C:\Program Files (x86)\World of Warcraft\_retail_\Logs\WoWCombatLog.txt") as fh:
                last_event = None
                
                char = None
                
                
                while "\n" not in char:
                    fh.seek(-1,pos)
                    char = fh.read(1)
                
                fh.seek(0, os.SEEK_END)
                size = fh.tell()
                block_size = min(size, 4096)
                block_position = size - block_size
                fh.seek(block_position, os.SEEK_SET)
                
                while block_position != 0:
                    line_position = fh.tell()
                    line = fh.readline()
                    while line_position < (block_position - block_size):
                        if ("ENCOUNTER_START" in line):
                            last_event = ["ENCOUNTER_START", line]
                        elif ("ENCOUNTER_END" in line):
                            last_event = ["ENCOUNTER_END", line]
                        line_position = fh.tell()
                        line = fh.readline()
                    
                    if last_event:
                        await client.get_channel(225860068661264394).send(str(last_event))
                        await asyncio.sleep(1)  # task runs every 60 seconds
                        await client.get_channel(225860068661264394).send(str(last_event))
                        return

@client.event
async def on_message(message):
    print("message seen")

@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(activity=discord.Game(name="The Waiting Game"))

client.loop.create_task(my_background_task())
client.run("NTU0MTU5OTg3MDM1ODY1MDg5.D2YnuQ.W_aqR4MijleEMgwFPzmHL9LEjcY")