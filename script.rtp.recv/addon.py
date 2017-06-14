import xbmcaddon
import xbmcgui
import xbmc
import os
import subprocess
import json
import time
 
# Open dialog box through the duration of the script
dialog = xbmcgui.DialogProgressBG()
dialog.create( 'Please wait...', 'Turning streaming on' )

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
subprocess.call(['pactl', 'load-module' , 'module-udev-detect'])
time.sleep(2)
subprocess.call(['pactl', 'load-module' , 'module-rtp-recv'])
time.sleep(5)

# Can't assume that either of these settings were loaded
#xbmcgui.Dialog().ok(addonname, 
#    'pactl'+'set-card-profile'+config['card-profile']+'output:'+config['card-output'])
#xbmcgui.Dialog().ok(addonname, 
#    'pactl'+'set-default-sink'+config['default-sink'])

try:
    subprocess.call(['pactl', 'set-card-profile',
                     config['card-profile'],
                     'output:' + config['card-output']])
except: Pass
time.sleep(2)

try:
    subprocess.call(['pactl', 'set-default-sink', config['default-sink']])
except: Pass
time.sleep(2)

# Resume audio engine again
xbmc.audioResume()

# get all settings and options
settings = xbmc.executeJSONRPC( '{"jsonrpc":"2.0",' +
		'"method":"Settings.GetSettings", "id":1}' )

# parse json settings for audio options
# this is Python 2 so no need to decode to utf-8
settings = json.JSONDecoder().decode( settings )
settings = settings['result']['settings']

# audio devices are item 120 with 'options' key
# extract just the labels for display purposes
labels = [ l['label'] for l in settings[120]['options'] ]

line = '\n'.join(labels)

# Close the dialog box
dialog.close()
