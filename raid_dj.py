import tailhead
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
    
        while 1:
            for line in tailhead.follow_path(log_loc):
                if line is not None:
                    if ("ENCOUNTER_START" in line):
                        if debug: print('\rfound encounter start: ' + line)
                    elif ("ENCOUNTER_END" in line):
                        if debug: print('\rfound encounter end: ' + line)

                        if int(line[-1]) == 0:
                            await client.get_channel(channel_id).send("You wiped :(")
                        else:
                            await client.get_channel(channel_id).send("You did the thing! :D")

                        await client.get_channel(channel_id).send(str(command))

                        if debug:
                            await client.get_channel(channel_id).send(line)
                        
                else:
                    if debug: sys.stdout.write('\r' + "waiting for log event " + next(spinner))
                    time.sleep(1)

client.loop.create_task(my_background_task())
client.run(token)

# for reference here is an "encounter end" log entry
# '7/26 23:39:14.320  ENCOUNTER_END,651,"Magtheridon",4,25,0\n'
# '2/21 22:06:27.449  ENCOUNTER_START,1853,"Nythendra",16,20,1520\n'
# '2/21 22:06:41.548  ENCOUNTER_END,1853,"Nythendra",16,20,0\n'