import os
import json
import time
import subprocess

url = 'https://you.com'
model = 'gpt-3.5-turbo'

def _create_completion(model: str, messages: list, **kwargs):

    path = os.path.dirname(os.path.realpath(__file__))
    config = json.dumps({
        'messages': messages}, separators=(',', ':'))
    
    cmd = ['python3', f'{path}/helpers/you.py', config]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in iter(p.stdout.readline, b''):
        yield line.decode('utf-8')[:-1]