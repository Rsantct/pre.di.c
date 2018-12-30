#!/usr/bin/env python3
""" Launch 'librespot', a Spotify Connect player client
    
    use:    librespot.py   start | stop
"""

import sys
from subprocess import run

import basepaths

def start():
    # 'librespot' binary prints out the playing track and some info to stdout/stderr.
    # We redirect the print outs to a temporary file that will be periodically
    # read from a player control daemon.

    cmd =  '/usr/bin/librespot --name rpi3clac --bitrate 320 --backend alsa' + \
           ' --device jack --disable-audio-cache --initial-volume=99'

    logFileName = f'{basepaths.main_folder}/.librespot_events'

    with open(logFileName, 'w') as logfile:
        run( cmd.split(), stdout=logfile, stderr=logfile )

def stop():
    """ harakiri """
    run( 'pkill -f librespot'.split() )

if sys.argv[1:]:
    try:
        option = {
            'start' : start,
            'stop'  : stop
            }[ sys.argv[1] ]()
    except:
        print('(librespot.py) bad option')
else:
    print(__doc__)
