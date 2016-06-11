from flask import Flask, request
import json
import requests
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'

def send_text_message(recipient_id, message):
    payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': message
            }
        }
    print "Got Message, ", message
    access_token = "EAAIPDYHtMsoBAOYf6CfnA6dKsTWQQzZBO1Pq0rLxgmDLBEh5RCV4Slvne2swN0YVhkZCe9PyhZC9Imu43hHQITN1p5x71incdH5cv5alWkjKoqFfJE1pPwthSjcZA0GC4MfRZCzrlHizlsReusPi29s7iI9xZARyFNC9L6IpaZAcQZDZD"
    base_url = (
            "https://graph.facebook.com"
            "/v2.6/me/messages?access_token={1}"
        ).format(access_token)
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
        except:
            return "Failed"

if __name__ == '__main__':
    print "RUNNING APP"
    app.run(debug=True)
