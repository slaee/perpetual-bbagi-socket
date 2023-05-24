import socketio
from BABYAGI import baby_agi
from g4f import ChatCompletion, Providers, Models

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
async def prompt(sid, data):
    response = ChatCompletion.create(stream=True, provider=Providers.You,
    model='gpt-4', messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates problems with format PROBLEM: and SOLUTION: for each problem without numbering it and don't say anything just the problems directly"},
                    {"role": "user", "content": "Goal 1: "+ data +  "Goal 2: The problems must be in concised not to much texts and please check if the problem generated is repeated and regenarate. Goal 3: 4 Problems only to be generated. Goal 4: Anaylze the problems and find the solution"},
                ])
    responseMessage = ""

    for message in response:
        responseMessage += message

    baby_agi({"objective": responseMessage})

    obj = []
    for problem in responseMessage.split("PROBLEM:"):
        if "SOLUTION:" in problem:
            contxt = problem.split("SOLUTION:")[0]
            solution = problem.split("SOLUTION:")[1]
            obj.append({
                'context': contxt,
                'solution': solution
            })
    
    await sio.emit('prompt', obj)
