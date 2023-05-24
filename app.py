from g4f import ChatCompletion, Providers, Models
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(message):
    response = ChatCompletion.create(model=Models.gpt_4, provider=Providers.You, messages=[
                                     {"role": "system", "content": "You are a helpful assistant that generates math problems with format PROBLEM: and SOLUTION: and don't say anythin just the math problem directly."},
                                     {"role": "user", "content": message}], stream=True)
    gptMessage = ""

    for message in response:
        gptMessage += message

    emit('message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)