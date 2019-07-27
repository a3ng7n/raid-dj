from pygtail import Pygtail
import time
import os
import sys
import itertools
import discord
import asyncio
import time

try:
    import raid_dj_defaults
    
    if not hasattr(raid_dj_defaults, 'token') or not raid_dj_defaults.token:
        raid_dj_defaults.token = input('Your raid dj needs a token: ')
    
    if not hasattr(raid_dj_defaults, 'channel_id') or not raid_dj_defaults.channel_id:
        raid_dj_defaults.channel_id = int(input('Your raid dj needs channel id to join: '))

    if not hasattr(raid_dj_defaults, 'log_loc') or not raid_dj_defaults.log_loc:
        raid_dj_defaults.log_loc = input('Your raid dj needs path/to/WoWCombatLog.txt (no need for quotes): ')
    
    if not hasattr(raid_dj_defaults, 'command') or not raid_dj_defaults.command:
        raid_dj_defaults.command = input('Your raid dj needs a command message to resume audio playback: ')
    
    if not hasattr(raid_dj_defaults, 'debug') or not raid_dj_defaults.debug:
        raid_dj_defaults.debug = bool(input('Enable debug output? 0 = No, 1 = Yes: '))
    
    token = raid_dj_defaults.token
    channel_id = raid_dj_defaults.channel_id
    log_loc = raid_dj_defaults.log_loc
    command = raid_dj_defaults.command
    debug = raid_dj_defaults.debug
except ImportError:
    token = input('Your raid dj needs a token: ')
    channel_id = int(input('Your raid dj needs channel id to join: '))
    log_loc = input('Your raid dj needs path/to/WoWCombatLog.txt (no need for quotes): ')
    command = input('Your raid dj needs a command message to resume audio playback: ')
    debug = bool(input('Enable debug output? 0 = No, 1 = Yes: '))

file = open('raid_dj_defaults.py', 'w')
file.write("token = \'" + token + "\'\n")
file.write("channel_id = " + str(channel_id) + "\n")
file.write("log_loc = \'" + log_loc + "\'\n")
file.write("command = \'" + command + "\'\n")
file.write("debug = " + str(debug) + "\n")
file.close()

client = discord.Client()

spinner = itertools.cycle(['-', '/', '|', '\\'])

async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed():
        print("The bot is ready!")
        
        log_events = []
    
        while 1:
        
            for line in Pygtail(filename=log_loc,
                                read_from_end=True):
                if ("ENCOUNTER_START" in line):
                    log_events.append(["ENCOUNTER_START", line, time.time()])
                    if debug: print('found encounter start')
                elif ("ENCOUNTER_END" in line):
                    log_events.append(["ENCOUNTER_END", line, time.time()])
                    if debug: print('found encounter end')
        
            if log_events:
                check_time = time.time()
                if (check_time - log_events[-1][2]) > 2:
                    if int(log_events[-1][1][-2]) == 0:
                        await client.get_channel(channel_id).send("You wiped :(")
                    else:
                        await client.get_channel(channel_id).send("You did the thing! :D")
                
                    await client.get_channel(channel_id).send(str(command))
                    if debug:
                        await client.get_channel(channel_id).send(str(log_events))
                    log_events = []
                else:
                    if debug: print('found event, but not waiting long enough '+str(check_time)+' '+str(log_events[-1][2]))
            else:
                if debug: sys.stdout.write('\r' + "waiting for log event " + next(spinner))
        
            time.sleep(1)

client.loop.create_task(my_background_task())
client.run(token)

# for reference here is an "encounter end" log entry
# '7/26 23:39:14.320  ENCOUNTER_END,651,"Magtheridon",4,25,0\n'