import obsws_python as obs
import os
import keyboard
import datetime

# Setup for WebSocket connection to OBS
cl= obs.ReqClient(host='localhost', port=3000, password='morsey', timeout=3)

# Setup for file
timestamps_file  = 'clips.txt'

if not os.path.exists(timestamps_file):
    with open(timestamps_file, 'w') as file:
        file.write('Timestamps: \n')

def get_timestamp():
    response = cl.get_record_status()
    return response.output_timecode

def write_timestamp_to_file(timestamp):
    with open(timestamps_file, 'a') as file:
        file.write(f'{timestamp} \n')

def get_and_write_timestamp():
    timestamp_text = get_timestamp()
    write_timestamp_to_file(timestamp_text)
print(f'Press ALT + T to grab your timestamp. Press ESC to exist the program')
keyboard.add_hotkey('alt + t', get_and_write_timestamp)
keyboard.wait('esc')