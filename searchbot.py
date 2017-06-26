from flask import Flask, request

from jinja2 import Environment, PackageLoader

import requests
import json
import traceback

from jobs import app
from jobs import searches
from jobs.database import db_session
from jobs.config import FACEBOOK_TOKEN, VERIFY_TOKEN
from random import randrange

fbBase = "https://graph.facebook.com/me/messages/?access_token="
token = FACEBOOK_TOKEN

env = Environment(loader=PackageLoader('jobs', 'templates'))
env.filters['jsonify'] = json.dumps
template = env.get_template('example.json')


@app.route('/webhook/701cfd22044c4fc194d1cf860f2a0c4', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            print(data)
            text = data['entry'][0]['messaging'][0]['message']['text']  # Incoming Message Text
            print("text: " + text)
            sender = data['entry'][0]['messaging'][0]['sender']['id']  # Sndr ID

            payload = json.dumps({"recipient": {"id": sender}, "message": {"text": "Θα λάβετε απάντηση σύντομα"}})
            r = requests.post(fbBase + token, headers={"Content-Type": "application/json"}, data=payload)

            readText = text.split(" στην ")

            jobs = searches.saveJobs(readText[0], readText[1], "")

            orderFuncs = {1: "Levenshtein Distance", 2: "Damerau-Levenshtein Distance",
                          3: "Hamming Distance", 4: "Jaro Distance",
                          5: "Jaro-Winkler Distance"}

            order = randrange(1, 6)

            answers = searches.orderByRel(jobs, readText[0], order)

            answers = answers[:3]

            """data2 = []

            for i in range(0, 3):
                data2.append({
                    'title': jobs1[i][0],
                    'url': jobs1[i][1],
                    'site': 'kariera'
                })"""

           #abc = template.render(page=data, sender=sender)

          #  ab = json.loads(abc)

            genBtn1 = {
                      "recipient": {
                        "id": sender
                      },
                      "message": {
                        "attachment": {
                          "type": "template",
                          "payload": {
                            "template_type":"button",
                            "text": answers[0][0],
                            "buttons": [
                              {
                                "type": "web_url",
                                "url": answers[0][1],
                                "title":"Show Job"
                              }
                            ]
                          }
                        }
                      }
                    }

            genBtn2 = {
                      "recipient": {
                        "id": sender
                      },
                      "message": {
                        "attachment": {
                          "type": "template",
                          "payload": {
                            "template_type":"button",
                            "text": answers[1][0],
                            "buttons": [
                              {
                                "type": "web_url",
                                "url": answers[1][1],
                                "title":"Show Job"
                              }
                            ]
                          }
                        }
                      }
                    }

            genBtn3 = {
                      "recipient": {
                        "id": sender
                      },
                      "message": {
                        "attachment": {
                          "type": "template",
                          "payload": {
                            "template_type":"button",
                            "text": answers[2][0],
                            "buttons": [
                              {
                                "type": "web_url",
                                "url": answers[2][1],
                                "title":"Show Job"
                              }
                            ]
                          }
                        }
                      }
                    }


            payload = json.dumps({"recipient": {"id": sender}, "message": {"text": "Ordered with: " + orderFuncs[order]}})  # We're going to send this back
           # print(abc)
            if (text):
                r = requests.post(fbBase + token, headers={"Content-Type": "application/json"}, data=json.dumps(genBtn1))  # Lets send it
                r = requests.post(fbBase + token, headers={"Content-Type": "application/json"}, data=json.dumps(genBtn2))  # Lets send it
                r = requests.post(fbBase + token, headers={"Content-Type": "application/json"}, data=json.dumps(genBtn3))  # Lets send it
                
            
            print(r.json())
           # return "ok", 200

           # print(json.dumps(ab))
        except Exception as e:
            print(traceback.format_exc())  # something went wrong
    elif request.method == 'GET':  # For the initial verification (read local value)
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    
    r = requests.post(fbBase + token, headers={"Content-Type": "application/json"}, data=payload)

    return "Hello World"  # Not Really Necessary


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
