import xbmcaddon
import xbmcgui
import xbmc
import os
import subprocess
import json
import time
 
# Open dialog box through the duration of the script
dialog = xbmcgui.DialogProgressBG()
dialog.create( 'Please wait...', 'Turning off streaming' )

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addonpath   = addon.getAddonInfo('path')
 
# Read in configuration options
config_file = addonpath + '/resources/config.json'
config = None
try:
    with open( config_file, 'r' ) as f:
        config_str = f.read()

    # parse json settings for config settings
    # this is Python 2 so no need to decode to utf-8
    config = json.JSONDecoder().decode( config_str )
except:
    None	# config will remain None

# Stop anything playing as we will be suspending audio engine 
#xbmc.Player.stop() # needs an argument!

# Suspend audio engine for Kodi to release PulseAudio
xbmc.audioSuspend()

# Run PulseAudio setup commands
subprocess.call('systemctl restart pulseaudio', shell=True)

# Disable PulseAudio output so Kodi can use its native audio output
#subprocess.call(['pactl', 'load-module', 'module-null-sink', 'sink_name=auto_null'])
#time.sleep(5)

# Resume audio engine again
xbmc.audioResume()

# Close the dialog box
dialog.close()
