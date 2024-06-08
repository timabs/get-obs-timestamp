import obsws_python as obs
import os
import keyboard


# Setup for WebSocket connection to OBS
cl= obs.ReqClient(host='localhost', port=3000, password='morsey', timeout=3)

# Setup for file
timestamps_file  = 'clips.txt'

if not os.path.exists(timestamps_file):
    with open(timestamps_file, 'w') as file:
        file.write('Timestamps: \n ')

def get_timestamp():
    response = cl.get_record_status()
    return response.output_timecode

