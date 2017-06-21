from flask import Flask, request

from jinja2 import Environment, PackageLoader

import requests
import json
import traceback

from jobs import app
from jobs import searches
from jobs.database import db_session


fbBase = "https://graph.facebook.com/me/messages/?access_token="
token = "EAALdO1loEXUBAA5zpoqn8jjaDI3ZAorlqPKrZBeOD38LTybLLdyZ"
token += "CNh7l5SvPZBZCIKgM2KANqMgu5xc0VIjMSUnIKAGirIsnCbiA3hKHskHhcWfptlNOGO"
token += "8TrQI3DEty9W7iTWTc5LRNYkFrsrNSiti3ZCxqN2AkZAYdflQWXMZCwZDZD"

env = Environment(loader=PackageLoader('jobs', 'templates'))
env.filters['jsonify'] = json.dumps
template = env.get_template('example.json')

# https://github.com/hartleybrody/fb-messenger-bot/blob/master/app.py#L24

@app.route('/webhook/701cfd22044c4fc194d1cf860f2a0c4', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            print(data)
            text = data['entry'][0]['messaging'][0]['message']['text']  # Incoming Message Text
            print("text: " + text)
            sender = data['entry'][0]['messaging'][0]['sender']['id']  # Sndr ID
            jobs1 = searches.searchKariera("Λογιστής", "Αθήνα")

            data2 = []

            for i in range(0, 3):
                data2.append({
                    'title': jobs1[i][0],
                    'url': jobs1[i][1],
                    'site': 'kariera'
                })

           #abc = template.render(page=data, sender=sender)

          #  ab = json.loads(abc)

            genBtn = {
                      "recipient": {
                        "id": sender
                      },
                      "message": {
                        "attachment": {
                          "type": "template",
                          "payload": {
                            "template_type":"button",
                            "text": jobs1[0][0],
                            "buttons": [
                              {
                                "type": "web_url",
                                "url": jobs1[0][1],
                                "title":"Show Job"
                              }
                            ]
                          }
                        }
                      }
                    }

            #payload = json.dumps({"recipient": {"id": sender}, "message": {"text": "Hello World"}})  # We're going to send this back
           # print(abc)
            r = requests.post(fbBase + token, headers={"Content-Type": "application/json"}, data=json.dumps(genBtn))  # Lets send it

            print(r.json())
            return "ok", 200

           # print(json.dumps(ab))
        except Exception as e:
            print(traceback.format_exc())  # something went wrong
    elif request.method == 'GET':  # For the initial verification
        if request.args.get('hub.verify_token') == '35cb23076a':
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Hello World"  # Not Really Necessary


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
