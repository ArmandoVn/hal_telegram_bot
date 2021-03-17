import requests
import json
# Credentials
from encuestas_hal.local_settings import TOKEN, URL, CHAT_ID

def get_url(url):
    response = requests.get(url)
    content = response.text
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates?allowed_updates=[\“message\”]"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message_bot(text):
    print(text)
    r = requests.post(URL + '/sendMessage',
        data={'chat_id': CHAT_ID, 'text': text})
    print(r.text)