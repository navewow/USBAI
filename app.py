import os
import sys
import json

import requests
import urllib2
from flask import Flask, request
from datetime import datetime
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

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

    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                if messaging_event.get("message"):  # someone sent us a message
                    msg = messaging_event["message"]["text"]  # the message's text
                    process_message(msg,sender_id)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    payload = messaging_event.get("postback")["payload"]
                    log(payload)
                    send_message(sender_id, payload)

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    showTyping = json.dumps({"recipient": {"id": recipient_id },"sender_action":"typing_on"})
    waitForAMoment = json.dumps({"recipient": {"id": recipient_id },"message":"Please wait for a moment."})

    params = {
        "access_token": 'EAAZAgx2FZBzKoBANUwLGzEiEXKuWrZAas32YTW5sQt9v9AtURPnrQD5wlzt5JFbJ3k5dyZBiZBZC7DAv4mwOJdSCRxYmDw2vzyr8oYeIqcyt8blL3TDYjKXEM02LU5PBUbZBxp0lQcXe2uJXW11uWa1WZC6dEhoYkrcM5vxuGeHQF6bd3Bsu9mUF'
    }
    headers = {
        "Content-Type": "application/json"
    }
    if "Level-1-Menu" in message_text or "Main Menu" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements":[
                        {
                            "title":"How may I help you?",
                            "subtitle":"Please type your question or choose from the below option or slide right for more options.",
                            "buttons":[
                              {
                                "type":"postback",
                                "title":"Balance Check",
                                "payload":"balance_check"
                              },
                              {
                                "type":"postback",
                                "title":"Transaction History",
                                "payload":"transaction_history"
                              },
                              {
                                "type":"postback",
                                "title":"Card Operations",
                                "payload":"card_operations"
                              }
                            ]
                        },
                        {
                            "title":"Other Queries",
                            "buttons":[
                              {
                                "type":"postback",
                                "title":"Let me Type",
                                "payload":"other_queries"
                              }]
                        },
                        {
                            "title":"Connect with Live Agent",
                            "subtitle":"A live agent will assist you for your queries",
                            "buttons":[
                              {
                                "type":"postback",
                                "title":"Connect Me",
                                "payload":"live_agent_connect"
                              }]
                        }
                    ]
                  }
                }
            }
        })
    elif "transaction_history" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements":[
                     {
                        "title":"Your Transaction History (A4) as of " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " CT",
                        "buttons":[
                          {
                            "type":"postback",
                            "title":" -$159.90" + " on 12/01 Web Author",
                            "payload":"Main Menu"
                          },
                          {
                            "type":"postback",
                            "title":" -$19.98" + " on 12/01 Debit Purc",
                            "payload":"Main Menu"
                          },
                          {
                            "type":"postback",
                            "title":" +$856.45" + " on 12/02 Electronic",
                            "payload":"Main Menu"
                          }
                        ]
                     }
                    ]
                  }
                }
            }
        })

    elif "balance_check" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements":[
                     {
                         "title":"Your Balance as of " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " CT",
                         "buttons":[
                             {
                                "type":"postback",
                                "title":"Checking ...xxx356:" + " $382.57",
                                "payload":"Main Menu"
                             },
                             {
                                "type":"postback",
                                "title":"Savings ...xxx432:" +" $655.63",
                                "payload":"Main Menu"
                             },
                             {
                                "type":"postback",
                                "title":"Transactions",
                                "payload":"transactions"
                             }
                           ]
                     }
                    ]
                  }
                }
            }
        })
    elif "transactions" in message_text:
         data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements":[
                     {
                         "title":"Choose Account Type:",
                         "buttons":[
                             {
                                "type":"postback",
                                "title":"Checking Account",
                                "payload":"transaction_history"
                             },
                             {
                                "type":"postback",
                                "title":"Savings Account",
                                "payload":"transaction_history"
                             }
                         ]
                      }
                    ]
                  }
                }
            }
        })
    elif "transaction_receipt" in message_text:
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
                    "order_url":"https://lh6.ggpht.com/O0BQpKIbn8c6b67tF4h4VKytKXlUZWrWIdnL06d4LtrUvdUuGr8VF4y7i8ziGAyo23lF=w170",
                    "timestamp":"1428444852",
                    "elements":[
                      {
                        "title":"12/01/16 Web Author",
                        "subtitle":"Debit",
                        "quantity":1,
                        "price":159.90,
                        "currency":"USD",
                        "image_url":"http://info.unionleasing.com/hs-fs/hub/371325/file-1922303652-png/Blog_Icons/Payment.png"
                      },
                      {
                        "title":"U.S. Bank - BAL @ 12/02/16 9:28am CT",
                        "subtitle":"Customer's Account In A4: $382.57  Savings A6: $655.63",
                        "quantity":1,
                        "price":0,
                        "currency":"USD",
                        "image_url":"https://lh3.ggpht.com/JPaCdWVnY-F8HBcBXvA68MTy-AFnGQPfXcj2MDIEuMSZdkVa0bM92eBcFxoj8EGiACMR=w300"
                      },
                      {
                        "title":"12/01/16 Debit Purc",
                        "subtitle":"Debit",
                        "quantity":1,
                        "price":19.98,
                        "currency":"USD",
                        "image_url":"http://info.unionleasing.com/hs-fs/hub/371325/file-1922303652-png/Blog_Icons/Payment.png"
                      },
                      {
                        "title":"12/02/16 Electronic",
                        "subtitle":"Credit",
                        "quantity":1,
                        "price":856.45,
                        "currency":"USD",
                        "image_url":"https://www.rcu.org/sites/default/files/money_icon_6.jpg"
                      }
                    ],
                    "summary":{
                      "total_cost":328.57
                    }
                  }
                }
            }
        })
    elif "card_operations" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"button",
                    "text":"Select one option",
                    "buttons":[
                      {
                        "type":"postback",
                        "title":"Card Activation",
                        "payload":"activate_card"
                      },
                      {
                        "type":"postback",
                        "title":"Block Card",
                        "payload":"block_card"
                      },
                      {
                        "type":"postback",
                        "title":"Card Cancellation",
                        "payload":"cancel_card"
                      }
                    ]
                  }
                }
            }
        })
    elif "activate_card" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements":[
                     {
                         "title":"Please Choose the Card",
                         "buttons":[
                             {
                                "type":"postback",
                                "title":"Card No:xxxxxxxx2314",
                                "payload":"activate"
                             },
                             {
                                "type":"postback",
                                "title":"Card No:xxxxxxxx3698",
                                "payload":"activate"
                             },
                             {
                                "type":"postback",
                                "title":"Card No:xxxxxxxx2547",
                                "payload":"activate"
                             }
                           ]
                     }
                    ]
                  }
                }
            }
        })
    elif "branch_locate" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                    "text":"Please share your location Or enter your zip code",
                    "quick_replies":[
                      {
                        "content_type":"location",
                      },
                      {
                        "content_type":"text",
                        "title:": "Enter Zip Code",
                        "payload":"zip_entry"
                      }
                    ]
            }
        })
    elif "zip_entry" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                    "text":"Please enter 5 digits in this format. zip:xxxx",
            }
        })
    elif "activate" in message_text:
        requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=waitForAMoment)
        requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=showTyping)
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text":"Card has been Activated"
            }
        })
    elif "other_queries" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": "Sure"
            }
        })
    elif "live_agent_connect" in message_text:
        requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=waitForAMoment)
        requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=showTyping)
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": "Hi, This is Alison. A live agent. How can I help you?"
            }
        })
    elif "zip_entered" in message_text:
        requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=waitForAMoment)
        requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=showTyping)
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": "Please find the details here: https://www.usbank.com/locations/locator-results.html?stringquery="+message_text+"&branch=y&atm=y"
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

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

    return r.status_code;

def process_message(text,sender_id):
        text=text.lower()
        output="Level-1-Menu"
        ps = PorterStemmer()
        words=word_tokenize(text)
        tokens=nltk.word_tokenize(text)
        tagged=nltk.pos_tag(tokens)
        entities=nltk.ne_chunk(tagged)
        print words
        for w in words:
                if(ps.stem(w).lower()=='enrol'):
                        if 'online' in str(words).lower() and 'banking' in str(words).lower():
                            output='Enroll to online banking at https://www.usbank.com/index.html'
                elif(ps.stem(w).lower()=='block'):
                        if 'my' in str(words).lower() and 'card' in str(words).lower():
                            output="Card has been blocked"
                elif(ps.stem(w).lower()=='activate'):
                            output="Card has been Activated"
                elif(ps.stem(w).lower()=='transaction'):
                        if 'cancel' in str(words).lower():
                            output="Your last transaction has been cancelled"
                        elif 'last' in str(words).lower():
                            output="transaction_receipt"
                elif(ps.stem(w).lower()=='balance_check'):
                        output="balance_check"
                elif(ps.stem(w).lower()=='zip:'):
                        output="zip_entered"
                elif(ps.stem(w).lower()=='branch' or ps.stem(w).lower()=='atm'):
                    if 'locat' in str(words).lower() or 'find' in str(words).lower() or 'search' in str(words).lower():
                        output="branch_locate"
        send_message(sender_id, output)



def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True)
