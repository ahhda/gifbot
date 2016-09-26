from flask import Flask, request
import json
import giphypop
import requests
import config
import os
from flask import render_template

app = Flask(__name__)
giphy = giphypop.Giphy(api_key=config.giphy['key'])
MAX_IMAGE_SIZE = 3072 * 1024
access_token = config.fb['access_token']
base_url = (
        "https://graph.facebook.com"
        "/v2.6/me/messages?access_token={0}"
    ).format(access_token)

@app.route('/')
def hello():
    return 'Hello World'

def send_normal_message(recipient_id, message):
    payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': message,
            }
        }
    result = requests.post(base_url, json=payload).json()
    return result

def send_image_message(recipient_id, message):
    payload = {
        'recipient': {
            'id': str(recipient_id)
        },
        'message': {
            "attachment": {
                "type": "image",
                    "payload":{
                        "url": message
                }
            }
        }
    }
    result = requests.post(base_url, json=payload).json()
    return result

def send_image(recipient_id, text):
    images = [i for i in giphy.search(text, limit=20) if i.filesize < MAX_IMAGE_SIZE]
    if not images or images is []:
        return None
    image = images[0]
    result = send_image_message(recipient_id, image.media_url)
    return result

@app.route('/webhook/', methods=['GET', 'POST'])
def verify():
    if request.method == 'GET':
        try:
            ok = request.args.get('hub.verify_token')
            if ok == 'my_voice_is_my_password_verify_me':
                return request.args.get('hub.challenge')
        except:
            pass
        return 'Yeah Fine, verified'
    if request.method == 'POST':
        try:
            output = request.json
            event = output['entry'][0]['messaging']
            for x in event:
                if (x.get('message') and x['message'].get('text')):
                    message = x['message']['text']
                    recipient_id = x['sender']['id']
                    value = send_image(recipient_id, message)
                    if value is None:
                        # No Gif found for the search term. Return a funny gif"
                        send_normal_message(recipient_id, "No GIF found. :(")
                        send_image_message(recipient_id, "http://media1.giphy.com/media/IHOOMIiw5v9VS/giphy.gif")
                else:
                    pass
            return "Success"
        except Exception, e:
            print e
            return "Failed"

if __name__ == '__main__':
    app.run(debug=True)
