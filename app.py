import os
import sys
import json

import requests
import urllib2
from flask import Flask, request

app = Flask(__name__)


@app.route('/bot', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    token = request.args.get('hub.verify_token')
    if token == "123":
        return request.args.get('hub.challenge')
    else:
        return "error"


@app.route('/bot', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    data = request.get_json()
##  print data
    log(data)  # you may not want to log every incoming message in production, but it's good for testing
##  value=request.data
##  jsonResponse=json.loads(value)
##  jsonData=jsonResponse["message"]["text"]
##  print jsonData
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    process_message(message_text,sender_id)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass


    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": 'EAAZAgx2FZBzKoBANUwLGzEiEXKuWrZAas32YTW5sQt9v9AtURPnrQD5wlzt5JFbJ3k5dyZBiZBZC7DAv4mwOJdSCRxYmDw2vzyr8oYeIqcyt8blL3TDYjKXEM02LU5PBUbZBxp0lQcXe2uJXW11uWa1WZC6dEhoYkrcM5vxuGeHQF6bd3Bsu9mUF'
    }
    headers = {
        "Content-Type": "application/json"
    }
    if "template" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                  "type":"template",
                  "payload":{
                    "template_type":"receipt",
                    "recipient_name":"Stephane Crozatier",
                    "order_number":"12345678902",
                    "currency":"USD",
                    "payment_method":"Visa 2345",
                    "order_url":"http://petersapparel.parseapp.com/order?order_id=123456",
                    "timestamp":"1428444852",
                    "elements":[
                      {
                        "title":"U.S. Bank",
                        "subtitle":"BAL @ 12/02/16 9:28am CT\nCustomer's Account In A4: $382.57 \nSavings A6: $655.63",
                        "quantity":1,
                        "price":0,
                        "currency":"USD",
                        "image_url":"http://petersapparel.parseapp.com/img/whiteshirt.png"
                      },
                      {
                        "title":"Transaction History",
                        "subtitle":"A4 at 12/02/16 9:28am CT",
                        "quantity":1,
                        "price":0,
                        "currency":"USD",
                        "image_url":"http://petersapparel.parseapp.com/img/grayshirt.png"
                      },
                      {
                        "title":"12/01/16 Web Author",
                        "subtitle":"Debit",
                        "quantity":1,
                        "price":159.90,
                        "currency":"USD",
                        "image_url":"http://petersapparel.parseapp.com/img/grayshirt.png"
                      },
                      {
                        "title":"12/01/16 Debit Purc",
                        "subtitle":"Debit",
                        "quantity":1,
                        "price":19.98,
                        "currency":"USD",
                        "image_url":"http://petersapparel.parseapp.com/img/grayshirt.png"
                      },
                      {
                        "title":"12/02/16 Electronic",
                        "subtitle":"Credit",
                        "quantity":1,
                        "price":856.45,
                        "currency":"USD",
                        "image_url":"http://petersapparel.parseapp.com/img/grayshirt.png"
                      }
                    ],
                    "balance":{
                      "total_cost":756.14
                    }
                  }
                }
            }
        })
    else:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })
    print data
##  value=request.data
##  output=''
##  jsonResponse=json.loads(data)
##  jsonData = jsonResponse['message']['text']
##  if ("block" in jsonData.lower()):
##      output='card blocked'
##  print output

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    return r.status_code;

def process_message(text,sender_id):
    text=text.lower()
    if "hi" in text:
        send_message(sender_id, "Hi,How can I help you?")
    elif "block" in text:
        if "not" not in text and "dont" not in text and "unblock" not in text:
            send_message(sender_id, "Your card has been blocked successfully.")
        else:
            send_message(sender_id, "Your card will not be blocked.")
    elif "activate" in text and "card" in text:
        send_message(sender_id, "Card has been Activated")
    elif "last" in text and "transaction" in text:
        send_message(sender_id, "template")
    elif "cancel" in text and "transaction" in text:
           if "not" not in text and "dont" not in text:
               send_message(sender_id, "Your last transaction has been cancelled")
           else:
               send_message(sender_id, "Your last transaction will not be cancelled")
    else:
        send_message(sender_id, "Sorry.I am not able to understand.I'll call you")



def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
