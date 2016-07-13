from flask import Flask, request
import requests
import json
from pprint import pprint


app = Flask(__name__)

token = ""

VERIFY_TOKEN = "test_token"


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  text = None
  if request.method == 'POST':
    data = json.loads(request.data)
    handle_messeging(data)
  elif request.method == 'GET': # For the initial verification
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
      return request.args.get('hub.challenge')
    return "Wrong Verify Token"
  return "No idea what you are talking about."


def handle_messeging(data):
  pprint(data['entry'][0]['messaging'][0], indent=4, depth=4)
  text = data['entry'][0]['messaging'][0]['message']['text'] # Incoming Message Text
  reply = create_reply(text)
  sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID
  payload = {'recipient': {'id': sender}, 'message': {'text': reply}} # We're going to send this back
  r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload) # Lets send it


def create_reply(type):
  type_lower = type.lower()
  if ("hello" in type_lower) or ("hi" in type_lower):
    return "Hi! Type help to see what we can talk about."
  elif type_lower == "help":
    return "There are three options: help, headlines, breaking"
  elif type_lower == "headlines":
    return """These are headlines:\n
              1. Donald Trump claims his hair is not fake\n
              2. Adel calls Momtaz for inspiration\n
              3. Americans officially love guns more than their moms
            """
  elif type_lower == "breaking":
    return "The Queen of England just had her lunch."
  else:
    return "I don't know what to say to that. Type help to see the keywords."


if __name__ == '__main__':
  app.run(debug=True)
