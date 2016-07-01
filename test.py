from flask import Flask, request
import json
import giphypop
import requests
import config
import os
from flask import render_template

def send_blank_msg(recipient_id, message):
    access_token = "EAAYy5xTcEToBAFlPJ5xn1axZB5ln34ZCuw1setBcGxSGo89YurkEbqgCHWa10RM5LwAptwXlXwYFD0mLx6RYy7TTB6tVcJv4CwI0jD8sRJWwCByyDSv8feJ5ipJUXJSB3Ma8yvXgKICZBx23BOmF97nVVWXppKgH716qBrntQZDZD"
    base_url = (
            "https://graph.facebook.com"
            "/v2.6/me/messages?access_token={0}"
        ).format(access_token)
    payload = {
        'recipient': {
            'id': "1109558182441367"
        },
        'message': {
            "attachment": {
                "type": "image",
                    "payload":{
                        "url": "http://media1.giphy.com/media/IHOOMIiw5v9VS/giphy.gif"
                }
            }
        }
    }
    print recipient_id, message
    result = requests.post(base_url, json=payload).json()
    return result

res = send_blank_msg("1109558182441367", "http://media1.giphy.com/media/IHOOMIiw5v9VS/giphy.gif")
print res
