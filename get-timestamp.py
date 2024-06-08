import obsws_python as obs
import os
import keyboard
import json
from datetime import datetime

# Setup for WebSocket connection to OBS
cl= obs.ReqClient(host='localhost', port=3000, password='morsey', timeout=3)

# Setup for file
timestamps_file  = 'clips.txt'
json_file = 'date.json'
prev_date = None


def check_json(json_file):
    global prev_date
    if not os.path.exists(json_file):
        with open(json_file, 'w') as file:
            json.dump({'prev_date': None}, file, indent=4)
    else:
        with open(json_file, 'r') as file:
            data = json.load(file)
            prev_date = data.get('prev_date')
def update_json_date(new_date):
    with open (json_file, 'w') as file:
        json.dump({'prev_date': new_date}, file, indent=4)


def check_file_setup(file_name):
    if not os.path.exists(timestamps_file):
        with open(timestamps_file, 'w') as file:
            file.write('Timestamps: \n')
    with open(file_name, 'r') as file:
        lines = file.readlines()
    if lines and lines[0].strip() == "Timestamps:":
        return
    else:
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
            update_json_date(cur_date)
        file.write(f'    {timestamp} \n')

def get_and_write_timestamp():
    check_file_setup(timestamps_file)
    timestamp_text = get_timestamp()
    write_timestamp_to_file(timestamp_text)
check_json(json_file)
print(f'Press ALT + T to grab your timestamp. Press ESC to exist the program')
keyboard.add_hotkey('alt + t', get_and_write_timestamp)
keyboard.wait('esc')