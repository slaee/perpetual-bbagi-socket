unstable g4f-v2 early-beta, only for developers !!

### interference opneai-proxy api (use with openai python package)    

run server:
```sh
python3 -m interference.app
```

```py
import openai

openai.api_key = ''
openai.api_base = 'http://127.0.0.1:1337'

chat_completion = openai.ChatCompletion.create(stream=True,
    model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': 'write a poem about a tree'}])

#print(chat_completion.choices[0].message.content)

for token in chat_completion:
    
    content = token['choices'][0]['delta'].get('content')
    if content != None:
        print(content)
```

### simple usage:

providers:
```py
g4f.Providers.Openai # need to be logged in in browser
g4f.Providers.Bing # need to be logged in in browser
g4f.Providers.You
g4f.Providers.Ails
g4f.Providers.Phind
g4f.Providers.Yqcloud

# usage:
response = g4f.ChatCompletion.create(..., provider=g4f.Providers.ProviderName)
```

```py
import g4f


print(g4f.Providers.Ails.params) # supported args

# Automatic selection of provider

# streamed completion
response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', messages=[
                                     {"role": "user", "content": "Hello world"}], stream=True)

for message in response:
    print(message)

# normal response
response = g4f.ChatCompletion.create(model=g4f.Models.gpt_4, messages=[
                                     {"role": "user", "content": "hi"}]) # alterative model setting

print(response)


# Set with provider
response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Providers.Openai, messages=[
                                     {"role": "user", "content": "Hello world"}], stream=True)

for message in response:
    print(message)
```

### Dev

(more instructions soon)
the `g4f.Providers`class

default:

`./g4f/Providers/ProviderName.py`:
```python
import os


url: str = 'https://{site_link}'
model: str = 'gpt-[version]'

def _create_completion(prompt: str, args...):
    return ...
    or
    yield ...


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
```
