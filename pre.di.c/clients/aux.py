#!/usr/bin/env python3

# Copyright (c) 2018 Rafael Sánchez
# This file is part of pre.di.c
# pre.di.c, a preamp and digital crossover
# Copyright (C) 2018 Roberto Ripio
#
# pre.di.c is based on FIRtro https://github.com/AudioHumLab/FIRtro
# Copyright (c) 2006-2011 Roberto Ripio
# Copyright (c) 2011-2016 Alberto Miguélez
# Copyright (c) 2016-2018 Rafael Sánchez
#
# pre.di.c is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pre.di.c is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pre.di.c.  If not, see <https://www.gnu.org/licenses/>.

""" A module interface that runs miscellaneous local tasks. 
    This module is ussually called from a listening server.
"""

import yaml
import subprocess as sp
import os
HOME = os.path.expanduser("~")

import basepaths as bp

#######  CONFIG HERE SOME GLOBALS #######
MACROS_FOLDER = bp.main_folder + 'clients/www/macros'
LOUDNESS_CTRL = bp.main_folder + '.loudness_control'

# Reading some user configs for auxilary tasks
try:
    with open( f'{bp.config_folder}/aux.yml' , 'r' ) as f:
        cfg = yaml.load( f.read() )
    AMP_ON_CMDLINE =  cfg['amp_on_cmdline']
    AMP_OFF_CMDLINE = cfg['amp_off_cmdline']
except:
    AMP_ON_CMDLINE =  'echo For amp switching please configure config/aux.yml'
    AMP_OFF_CMDLINE = 'echo For amp switching please configure config/aux.yml'


def do(task):
    """
        This do() is the entry interface function from a listening server.
        Only certain 'tasks' will be validated and processed,
        then returns back some useful info to the asking client.
    """

    # First clearing the new line
    task = task.replace('\n','')

    ### SWITCHING ON/OFF AN AMPLIFIER
    # notice: subprocess.check_output(cmd) returns bytes-like,
    #         but if cmd fails an exception will be raised, so used with 'try'
    if task == 'amp_on':
        try:
            sp.Popen( AMP_ON_CMDLINE.split() )
            return b'done'
        except:
            return b'error'
    elif task == 'amp_off':
        try:
            sp.Popen( AMP_OFF_CMDLINE.split() )
            return b'done'
        except:
            return b'error'

    ### USER MACROS
    # Macro files are named this way: 'N_macroname',
    # so N will serve as button keypad position on the web control page.
    # The task phrase syntax must be like: 'macro_N_macroname',
    # that is prefixed with the reserved word 'macro_'
    elif task[:6] == 'macro_':
        try:
            cmd = f'{MACROS_FOLDER}/{task[6:]}'
            sp.run( "'" + cmd + "'", shell=True ) # needs shell to user bash scripts to work
            return b'done'
        except:
            return b'error'

    ### LOUDNESS MONITOR RESET
    elif task == 'loudness_monitor_reset':
        try:
            with open(LOUDNESS_CTRL, 'w') as f:
                f.write('reset')
            return b'done'
        except:
            return b'error'

    ### CHANGE TARGET
    elif task[:10] == 'set_target':
        try:
            # it comes only the magnitude filename
            pattern = task[11:]
            sp.Popen( [ f'{HOME}/bin/predic_change_target.sh', pattern ] )
            print( f'(aux.py) changing target to {pattern}' )
            # change also the phase
            pattern = pattern.replace('_mag', '_pha')
            sp.Popen( [ f'{HOME}/bin/predic_change_target.sh', pattern ] )
            print( f'(aux.py) changing target to {pattern}' )
            return b'done'
        except:
            return b'error'

    ### JACKMINIMIX
    # If you run jackminimix, you can control the mixer input's gain
    # https://www.aelius.com/njh/jackminimix/
    elif task[:6] == 'mixer ':
        try:
            cmd = f'{bp.main_folder}/clients/jackminimix_ctrl.py { task[6:] }'
            sp.run( cmd.split() )
            return b'done'
        except:
            return b'error'

    ### MONITOR LOUDSPEAKER VOLUME CONTROL
    elif task[:10] == 'mon_volume':
        vol = task[10:].strip()
        # I don't know why but '+' is missing :-/
        if vol[0] != '-':
            vol = '+' + vol
        try:
            # (i) clients/MON_volume.sh needs to be adjusted to point to
            #     the real script that controls your monitor loudspeaker.
            cmd = f'{bp.main_folder}/clients/MON_volume.sh {vol}'
            sp.run( cmd.split() )
            return b'done'
        except:
            return b'error'

