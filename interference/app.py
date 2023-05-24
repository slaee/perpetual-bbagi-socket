import os
import time
import json
import random

from g4f import Models, ChatCompletion, Providers
from flask import Flask, request

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

class website:
    def __init__(self) -> None:
        self.routes = {
            '/chat/completions': {
                'function': self.chat_completions,
                'methods': ['POST', 'GET']
            }
        }

        self.config = {
            'host': '0.0.0.0',
            'port': 1337,
            'debug': True
        }

    def chat_completions(self):
        streaming = request.json.get('stream', False)
        model = request.json.get('model', 'gpt-3.5-turbo')
        messages = request.json.get('messages')

        models = {
            'gpt-3.5-turbo': 'gpt-3.5-turbo-0301'
        }

        response = ChatCompletion.create(model=Models.gpt_35_turbo, stream=streaming,
                messages=messages)
        
        if not streaming:

            completion_timestamp = int(time.time())
            completion_id = ''.join(random.choices(
                'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))

            return {
                'id': 'chatcmpl-%s' % completion_id,
                'object': 'chat.completion',
                'created': completion_timestamp,
                'model': models[model],
                'usage': {
                    'prompt_tokens': None,
                    'completion_tokens': None,
                    'total_tokens': None
                },
                'choices': [{
                    'message': {
                            'role': 'assistant',
                            'content': response
                            },
                    'finish_reason': 'stop',
                    'index': 0
                }]
            }

        def stream():
            for token in response:
                completion_timestamp = int(time.time())
                completion_id = ''.join(random.choices(
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))

                completion_data = {
                    'id': f'chatcmpl-{completion_id}',
                    'object': 'chat.completion.chunk',
                    'created': completion_timestamp,
                    'model': 'gpt-3.5-turbo-0301',
                    'choices': [
                        {
                            'delta': {
                                'content': token
                            },
                            'index': 0,
                            'finish_reason': None
                        }
                    ]
                }
                yield 'data: %s\n\n' % json.dumps(completion_data, separators=(',' ':'))
                time.sleep(0.1)

        return app.response_class(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    website = website()

    for route in website.routes:
        app.add_url_rule(
            route,
            view_func=website.routes[route]['function'],
            methods=website.routes[route]['methods']
        )

    app.run(**website.config)