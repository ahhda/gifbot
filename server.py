from flask import Flask, request
import json
import giphypop
import requests
import config
import os

app = Flask(__name__)
giphy = giphypop.Giphy(api_key=config.giphy['key'])
MAX_IMAGE_SIZE = 3072 * 1024

class Element(object):

    __acceptable_keys = ['title', 'item_url', 'image_url', 'subtitle']
    def __init__(self, **kwargs):
        for key in self.__acceptable_keys:
            setattr(self, key, kwargs.get(key))

    def to_json(self):
        data = {}
        for key in self.__acceptable_keys:
            data[key] = getattr(self, key)
        return json.dumps(data)

@app.route('/')
def hello():
    return 'Hello World'

def send_text_message(recipient_id, text):
    print "RECIPIENT ID ", recipient_id

    access_token = "EAAIPDYHtMsoBAOYf6CfnA6dKsTWQQzZBO1Pq0rLxgmDLBEh5RCV4Slvne2swN0YVhkZCe9PyhZC9Imu43hHQITN1p5x71incdH5cv5alWkjKoqFfJE1pPwthSjcZA0GC4MfRZCzrlHizlsReusPi29s7iI9xZARyFNC9L6IpaZAcQZDZD"
    base_url = (
            "https://graph.facebook.com"
            "/v2.6/me/messages?access_token={0}"
        ).format(access_token)

    images = [i for i in giphy.search(text, limit=20) if i.filesize < MAX_IMAGE_SIZE]
    if not images or images is []:
        "No Images"
        return None
    image = images[0]

    # elements = []ia_url), subtitle="subtitle", item_url=str(image.media_url))
    # elements.append(element)
    print image.media_url
    payload = {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            "attachment": {
                "type": "image",
                    "payload":{
                        "url":image.media_url
                }
            }
        }
    }
    # payload = {
    #     'recipient': {
    #         'id': recipient_id
    #     },
    #     'message': {
    #         "attachment": {
    #             "type": "template",
    #             "payload": {
    #                 "template_type": "generic",
    #                 "elements": [{
    #                     "title": text,
    #                     "image_url": image.media_url,
    #                     "item_url": image.media_url
    #                 }]
    #             }
    #         }
    #     }
    # }
    print "DOING JSON"
    result = requests.post(base_url, json=payload).json()
    print "RESULT IS ", result
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
                    send_text_message(recipient_id, message)
                else:
                    print "Nothing"
                    pass
            return "Success"
        except Exception, e:
            print e
            return "Failed"

if __name__ == '__main__':
    print "RUNNING APP"
    app.run(debug=True)
