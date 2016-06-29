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

@app.route('/')
def hello():
    return 'Hello World'

@app.route('/privacypolicy/')
def privacy():
    return render_template('privacy-policy.html')

def send_image(recipient_id, image):
    access_token = "EAAIPDYHtMsoBAOYf6CfnA6dKsTWQQzZBO1Pq0rLxgmDLBEh5RCV4Slvne2swN0YVhkZCe9PyhZC9Imu43hHQITN1p5x71incdH5cv5alWkjKoqFfJE1pPwthSjcZA0GC4MfRZCzrlHizlsReusPi29s7iI9xZARyFNC9L6IpaZAcQZDZD"
    base_url = (
            "https://graph.facebook.com"
            "/v2.6/me/messages?access_token={0}"
        ).format(access_token)

def send_text_message(recipient_id, text):
    print "RECIPIENT ID ", recipient_id
    images = [i for i in giphy.search(text, limit=20) if i.filesize < MAX_IMAGE_SIZE]
    if not images or images is []:
        "No Images"
        return None
    image = images[0]
    print image.media_url

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
    result = send_blank_msg(recipient_id, image.media_url)
    print "RESULT IS ", result
    return result

def send_blank_msg(recipient_id, message):
    access_token = "EAAYy5xTcEToBAFlPJ5xn1axZB5ln34ZCuw1setBcGxSGo89YurkEbqgCHWa10RM5LwAptwXlXwYFD0mLx6RYy7TTB6tVcJv4CwI0jD8sRJWwCByyDSv8feJ5ipJUXJSB3Ma8yvXgKICZBx23BOmF97nVVWXppKgH716qBrntQZDZD"
    base_url = (
            "https://graph.facebook.com"
            "/v2.6/me/messages?access_token={0}"
        ).format(access_token)
    payload = {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            "attachment": {
                "type": "image",
                    "payload":{
                        "url":message
                }
            }
        }
    }
    print recipient_id, message
    result = requests.post(base_url, json=payload).json()
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
                    value = send_text_message(recipient_id, message)
                    print "VALUE IS ", value
                    if value is None:
                        print "in messages"
                        send_blank_msg(recipient_id, "http://media1.giphy.com/media/IHOOMIiw5v9VS/giphy.gif")
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
