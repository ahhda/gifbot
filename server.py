from flask import Flask, request
import requests
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'

@app.route('/webhook/')#, methods = ['POST'])
def verify():
    try:
        ok = request.json.get('hub.verify_token')
        if ok == 'my_voice_is_my_password_verify_me':
            return request.json.get('hub.challenge')
    except:
        pass
    return 'Yeah Fine, verified'

if __name__ == '__main__':
    print "RUNNING APP"
    app.run(debug=True)
