import obsws_python as obs
import os
import keyboard
from datetime import datetime

# Setup for WebSocket connection to OBS
cl= obs.ReqClient(host='localhost', port=3000, password='morsey', timeout=3)

# Setup for file
timestamps_file  = 'clips.txt'
prev_date = None

def check_file_setup(file_name):
    if not os.path.exists(timestamps_file):
        with open(timestamps_file, 'w') as file:
            file.write('Timestamps: \n')
    with open(file_name, 'r') as file:
        lines = file.readlines()
    if lines and lines[0].strip() == "Timestamps":
        return
    lines.insert(0, "Timestamps: \n")
    with open(file_name, 'w') as file:
        file.writelines(lines)

def get_date():
    today = datetime.today()
    formatted_date = today.strftime("%B %d, %Y")
    return formatted_date

def get_timestamp():
    response = cl.get_record_status()
    return response.output_timecode

def write_timestamp_to_file(timestamp):
    global prev_date
    cur_date = get_date()
    with open(timestamps_file, 'a') as file:
        if cur_date != prev_date:
            file.write(cur_date + '\n')
            prev_date = cur_date
        file.write(f'    {timestamp} \n')

def get_and_write_timestamp():
    check_file_setup(timestamps_file)
    timestamp_text = get_timestamp()
    write_timestamp_to_file(timestamp_text)
print(f'Press ALT + T to grab your timestamp. Press ESC to exist the program')
keyboard.add_hotkey('alt + t', get_and_write_timestamp)
keyboard.wait('esc')