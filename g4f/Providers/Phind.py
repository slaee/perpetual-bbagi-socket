import os
import json
import time
import subprocess

url = None
model = None
    
def _create_completion(model: str, messages: list, **kwargs):

    path = os.path.dirname(os.path.realpath(__file__))
    config = json.dumps({
        'messages': messages}, separators=(',', ':'))

    cmd = ['python3', f'{path}/helpers/phind.py', config]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in iter(p.stdout.readline, b''):
        if b'<title>Just a moment...</title>' in line:
            os.system('clear' if os.name == 'posix' else 'cls')
            yield 'Clouflare error, please try again...'
            os._exit(0)
        
        else:
            if b'ping - 2023-' in line:
                continue
            
            yield line.decode('utf-8')[:-1]