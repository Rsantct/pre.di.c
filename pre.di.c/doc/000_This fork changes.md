## This fork main changes versus the official repository

### 2019-Jan:

- Minor changes on run level options into `stopaudio.py` and `startaudio.py`.
- Minor code under `startaudio.py` to able Jack to run under Pulseaudio desktop machines.
- Minor code mod under `start_pid()` at `predic.py` to able processes (e.g. mplayer) to redirect his stdout and stderr to a file that could be read later from others process.
- `DVB.py` has been rewritten.
- New server mechanism
- Code arrangement ( issue #29 ), including `scripts` folder renamed to `init` and scripts inside init folder leaving the `.py` or `.sh` extension.

    ```
    $HOME/
        ├── cdda_fifo   dvb_fifo    ...
        │    
        ├── bin/     (user bin folder including some pre.di.c tools)
        │    
        ├── pre.di.c/
            │
            ├── bin
            │   │   basepaths.py    peq_control.py  startaudio.py
            │   └── control.py      predic.py       stopaudio.py
            │       getconfigs.py   server.py
            │
            ├── init
            │   └── alsa_loop       mpd     ...     ...
            │
            ├── clients
            │   │
            │   ├── bin
            │   │   └── aux         players         mouse_volume     ...
            │   │
            │   ├── macros
            │   │   └── 1_RNE       2_R.Clasica     ...     ...
            │   │
            │   └── www   (the web page, server side and client side code)
    ```

## New server

It has been rewritten the `server.py` code in order to leave it as a general purpose server script that can run specific service modules.

The most important service is the implemented under the **`control.py`** module (formerly `server_process.py`).

This way the server can runs also other general interest service modules.

So, if we wanna run the server that will listen for pre.di.c management, we run:

  `server.py control`

If wanna run another server for auxiliary tasks:

  `server.py aux`

The arguments `control` or `aux` will indicates to `server.py` to IMPORT these module names to work.

The addresses and ports mapping to run each service are specified under `config/config.yml`

Any service module intended to be used under `server.py` must provide an interfacing function named `do()`.

Also, an optimization has been done regarding the original `server.py` mechanism: it has been omitted the status dict when calling `process_commands()` because status is already read by default when calling this function.

## DVB.py

    Starts and stops Mplayer for DVB-T playback.
    Also used to change on the fly the played stream.
    DVB-T tuned channels are ussually stored at
        ~/.mplayer/channels.conf
    User settings (presets, default) can be configured into:
        config/DVB-T.yml
    Usage:   DVB.py     start  [ <preset_num> | <channel_name> ]
                        stop
                        prev  (load previous from recent presets)
                        preset <preset_num>
                        name   <channel_name>

Now `DVB.py` uses a unique `config/DVB-T.yml` file for user presets configuration and also for recent used presets to be persistent, so `config/DVB-T_state.yml` is not used anymore.

I have switched to the YAML parser `ruamer.yaml` that preserves comments and the order of yaml items when dumping.
