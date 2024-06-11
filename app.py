from flask import Flask, request, jsonify
import obsws_python as obs
import os
import json
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

obs_host = os.getenv('OBS_HOST')
obs_port = os.getenv('OBS_PORT')
obs_password = os.getenv('OBS_PASSWORD')
cl= obs.ReqClient(host=obs_host, port=int(obs_port), password=obs_password, timeout=3)
# Setup for file
timestamps_file = 'clips.txt'
json_file = 'date.json'
prev_date = None


def check_json():
    global prev_date
    if not os.path.exists(json_file):
        with open(json_file, 'w') as file:
            json.dump({'prev_date': None}, file, indent=4)
    else:
        with open(json_file, 'r') as file:
            data = json.load(file)
            prev_date = data.get('prev_date')

def update_json_date(new_date):
    with open(json_file, 'w') as file:
        json.dump({'prev_date': new_date}, file, indent=4)

def check_file_setup():
    if not os.path.exists(timestamps_file):
        with open(timestamps_file, 'w') as file:
            file.write('Timestamps: \n')
    with open(timestamps_file, 'r') as file:
        lines = file.readlines()
    if lines and lines[0].strip() == "Timestamps:":
        return
    else:
        lines.insert(0, "Timestamps: \n")
        with open(timestamps_file, 'w') as file:
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
    check_file_setup()
    timestamp_text = get_timestamp()
    write_timestamp_to_file(timestamp_text)

@app.route('/timestamp', methods=['POST'])
def timestamp():
    check_json()
    get_and_write_timestamp()
    return jsonify({'status':'success', 'message': 'Timestamp recorded'}), 200

if __name__ == '__main__':
    app.run(port=5000)