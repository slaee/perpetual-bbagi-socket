import sys
import ssl
import uuid 
import json
import random
import asyncio
import certifi
import requests
import websockets
import browser_cookie3

config = json.loads(sys.argv[1])

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

conversationstyles = {
    'gpt-4': [ #'precise'
        "nlu_direct_response_filter",
        "deepleo",
        "disable_emoji_spoken_text",
        "responsible_ai_policy_235",
        "enablemm",
        "h3imaginative",
        "travelansgnd",
        "dv3sugg",
        "clgalileo",
        "gencontentv3",
        "dv3sugg",
        "responseos",
        "e2ecachewrite",
        "cachewriteext",
        "nodlcpcwrite",
        "travelansgnd",
        "nojbfedge",
    ],
    'balanced': [
        "nlu_direct_response_filter",
        "deepleo",
        "disable_emoji_spoken_text",
        "responsible_ai_policy_235",
        "enablemm",
        "galileo",
        "dv3sugg",
        "responseos",
        "e2ecachewrite",
        "cachewriteext",
        "nodlcpcwrite",
        "travelansgnd",
        "nojbfedge",
    ],
    'gpt-3.5-turbo': [ #'precise'
        "nlu_direct_response_filter",
        "deepleo",
        "disable_emoji_spoken_text",
        "responsible_ai_policy_235",
        "enablemm",
        "galileo",
        "dv3sugg",
        "responseos",
        "e2ecachewrite",
        "cachewriteext",
        "nodlcpcwrite",
        "travelansgnd",
        "h3precise",
        "clgalileo",
        "nojbfedge",
    ]
}

def format(msg: dict) -> str:
    return json.dumps(msg) + '\x1e'

def get_token():
    try:
        cookies = {c.name: c.value for c in browser_cookie3.edge(domain_name='bing.com')}
        return cookies['_U']
    except:
        print('Error: could not find bing _U cookie in edge browser.')
        exit(1)

class AsyncCompletion:
    async def create(
        prompt     : str = None,
        optionSets : list = None,
        token     : str = get_token()):
        
        create = requests.get('https://edgeservices.bing.com/edgesvc/turing/conversation/create', 
            headers = {
                'host'       : 'edgeservices.bing.com',
                'authority'  : 'edgeservices.bing.com',
                'cookie'     : f'_U={token}',
                'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
            }
        )

        conversationId        = create.json()['conversationId']
        clientId              = create.json()['clientId']
        conversationSignature = create.json()['conversationSignature']

        wss: websockets.WebSocketClientProtocol or None = None

        wss = await websockets.connect('wss://sydney.bing.com/sydney/ChatHub', max_size = None, ssl = ssl_context,
            extra_headers = {
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/json',
                'sec-ch-ua': '"Not_A Brand";v="99", Microsoft Edge";v="110", "Chromium";v="110"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"109.0.1518.78"',
                'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.192", "Not A(Brand";v="24.0.0.0", "Microsoft Edge";v="110.0.1587.69"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': "",
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"15.0.0"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'x-ms-client-request-id': str(uuid.uuid4()),
                'x-ms-useragent': 'azsdk-js-api-client-factory/1.0.0-beta.1 core-rest-pipeline/1.10.0 OS/Win32',
                'Referer': 'https://www.bing.com/search?q=Bing+AI&showconv=1&FORM=hpcodx',
                'Referrer-Policy': 'origin-when-cross-origin',
                'x-forwarded-for': f'13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}'
            }
        )

        await wss.send(format({'protocol': 'json', 'version': 1}))
        await wss.recv()

        struct = {
            'arguments': [
                {
                    'source': 'cib', 
                    'optionsSets': optionSets, 
                    'isStartOfSession': True, 
                    'message': {
                        'author': 'user', 
                        'inputMethod': 'Keyboard', 
                        'text': prompt, 
                        'messageType': 'Chat'
                    }, 
                    'conversationSignature': conversationSignature, 
                    'participant': {
                        'id': clientId
                    }, 
                    'conversationId': conversationId
                }
            ], 
            'invocationId': '0', 
            'target': 'chat', 
            'type': 4
        }
        
        await wss.send(format(struct))
        
        base_string = ''
        
        final = False
        while not final:
            objects = str(await wss.recv()).split('\x1e')
            for obj in objects:
                if obj is None or obj == '':
                    continue
                
                response = json.loads(obj)
                if response.get('type') == 1 and response['arguments'][0].get('messages',):
                    response_text = response['arguments'][0]['messages'][0]['adaptiveCards'][0]['body'][0].get('text')
                    
                    yield (response_text.replace(base_string, ''))
                    base_string = response_text
        
                elif response.get('type') == 2:
                    final = True
        
        await wss.close()

async def run(optionSets, messages):
    async for value in AsyncCompletion.create(prompt=messages[-1]['content'], 
                                              optionSets=optionSets):
        
        print(value, flush=True)

optionSet = conversationstyles[config['model']]
asyncio.run(run(optionSet, config['messages']))