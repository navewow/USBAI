import os
import sys
import json

import requests
import urllib2
import uuid

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
    
from flask import Flask, request
from datetime import datetime
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

app = Flask(__name__)
CLIENT_ACCESS_TOKEN = '64a9a332b5834a73b61b860b885def02'

#@app.route('/GetMethod', methods=['Get'])
def GetMethod(strUserQuery):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    #request.lang = 'de'  # optional, default value equal 'en'

    request.session_id = str(uuid.uuid4())

    request.query = str(strUserQuery)

    response = request.getresponse()
    
    strResponse =  str(response.read())
    
    print("GetMethodResponse")

    print (strResponse)
    
    return strResponse

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

    #if data["object"] == "page":

    for entry in data["entry"]:
        for messaging_event in entry["messaging"]:

            sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
            recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
            if messaging_event.get("message"):  # someone sent us a message
                for text in messaging_event["message"]:
##                    log("ext val" + text)
                    if text in "text":
##                        log("in if 1")
                        msg = messaging_event["message"]["text"]  # the message's text
                        strResponse = GetMethod(msg)
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
    hereTheResults = json.dumps({"recipient": {"id": recipient_id },"message":"Here are the results.."})
    locFinderUrl="https://publicrestservice.usbank.com/public/ATMBranchLocatorRESTService_V_8_0/GetListATMorBranch/LocationSearch/StringQuery?application=parasoft&transactionid=7777777d-8946-4f88-a958-4bdbcf0bed6f&output=json&searchtype=E&branchfeatures=BOP&stringquery="

    params = {
        "access_token": 'EAARneTfc3AYBAE2why15aJStTsMZCvLKNZBS6dUvXLccMWGuOjYxyk7PBTDLYzdQ4AT6PIHTSp7Of1oTaICX5Ma5ntrMCrVT32kIlui143FytI5ZC0o4bTWerGkaI9B3ZAzgtwrny8PqtLsxvgGtYUSMaEnX0PjQSE7ZBGWizY6vUodha8XGp'
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
    elif "transaction_history_1" in message_text:
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
                        "title":"Your Transaction History as of " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " CT",
                        "subtitle":"Account No:...xxx356:",
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

    elif "transaction_history_2" in message_text:
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
                        "title":"Your Transaction History as of " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " CT",
                        "subtitle":"Account No:...xxx432:",
                        "buttons":[
                          {
                            "type":"postback",
                            "title":" -$3459.90" + " on 11/01 Macy",
                            "payload":"Main Menu"
                          },
                          {
                            "type":"postback",
                            "title":" -$239.98" + " on 11/01 Sears",
                            "payload":"Main Menu"
                          },
                          {
                            "type":"postback",
                            "title":" -$2000.00" + " on 11/02 Transfer",
                            "payload":"Main Menu"
                          }
                        ]
                     }
                    ]
                  }
                }
            }
        })

    elif "transaction_history_3" in message_text:
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
                        "title":"Your Transaction History as of " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " CT",
                        "subtitle":"Account No:...xxx478:",
                        "buttons":[
                          {
                            "type":"postback",
                            "title":" +$1,450,000.00" + " on 10/01 Deposit",
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
                         "title":"Your Balance as of :" +datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " CT",
                         "subtitle":"Checking xxx356: $15,382.57",
                         "buttons":[
                             {
                                "type":"postback",
                                "title":"Transactions",
                                "payload":"transaction_history_1"
                             }
                           ]
                     },
                     {
                         "title":"Savings xxx432:",
                         "subtitle":"$4655.00",
                         "buttons":[
                             {
                                "type":"postback",
                                "title":"Transactions",
                                "payload":"transaction_history_2"
                             }
                           ]
                     },
                     {
                         "title":"CD xxx478:",
                         "subtitle":"$1,22,500.00",
                         "buttons":[
                             {
                                "type":"postback",
                                "title":"Transactions",
                                "payload":"transaction_history_3"
                             }
                           ]
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
                         "title":"Choose Account Type:",
                         "buttons":[
                             {
                                "type":"postback",
                                "title":"Checking xxx356",
                                "payload":"transaction_history_1"
                             },
                             {
                                "type":"postback",
                                "title":"Savings xxx432",
                                "payload":"transaction_history_2"
                             },
                             {
                                "type":"postback",
                                "title":"CD xxx478",
                                "payload":"transaction_history_3"
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
                    "text":"Please share your location Or enter your 5 digit zip code",
                    "quick_replies":[
                      {
                        "content_type":"location",
                      }
                    ]
            }
        })
    elif message_text.isdigit() and len(str(message_text))==5 :
       # op="No details found. Please try again with another zip code."
        requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=waitForAMoment)
        requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=showTyping)
        requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=hereTheResults)

        log('Finding location:'+locFinderUrl+message_text);
        results = requests.get(locFinderUrl+message_text)
        resultsJson = json.loads(results.text)
       # op=str(resultsJson['GetListATMorBranchReply']['ATMList'][0]['LocationIdentifier']['Address']['AddressLine1'])
        #log(resultsJson.GetListATMorBranchReply.BranchList[0].LocationIdentifier.PhoneNumber)
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
                            "title":"Top 5 ATMs are fetched.",
                            "image_url":"https://pbs.twimg.com/profile_images/2559525113/USBankCareersAvatar6158.png",
                            "subtitle":"Please slide right to see the list.",
                        },
                        {
                            "title":"Dist: "+resultsJson['GetListATMorBranchReply']['ATMList'][0]['Distance']+" miles,  "+resultsJson['GetListATMorBranchReply']['ATMList'][0]['CommonLocationName'],
                            "subtitle":resultsJson['GetListATMorBranchReply']['ATMList'][0]['LocationIdentifier']['Address']['AddressLine1']+", "+resultsJson['GetListATMorBranchReply']['ATMList'][0]['LocationIdentifier']['Address']['City']+", "+resultsJson['GetListATMorBranchReply']['ATMList'][0]['LocationIdentifier']['Address']['ZipCode'],
                            "buttons":[
                                  {
                                    "type":"web_url",
                                    "url":"https://www.google.com/maps/place/"+resultsJson['GetListATMorBranchReply']['ATMList'][0]['LocationIdentifier']['GeocodeLocation']['Latitude']+","+resultsJson['GetListATMorBranchReply']['ATMList'][0]['LocationIdentifier']['GeocodeLocation']['Longitude'],
                                    "title":"Locate in Map"
                                  }
                            ]
                        },
                        {
                            "title":"Dist: "+resultsJson['GetListATMorBranchReply']['ATMList'][1]['Distance']+" miles,  "+resultsJson['GetListATMorBranchReply']['ATMList'][0]['CommonLocationName'],
                            "subtitle":resultsJson['GetListATMorBranchReply']['ATMList'][1]['LocationIdentifier']['Address']['AddressLine1']+", "+resultsJson['GetListATMorBranchReply']['ATMList'][1]['LocationIdentifier']['Address']['City']+", "+resultsJson['GetListATMorBranchReply']['ATMList'][1]['LocationIdentifier']['Address']['ZipCode'],
                            "buttons":[
                                  {
                                    "type":"web_url",
                                    "url":"https://www.google.com/maps/place/"+resultsJson['GetListATMorBranchReply']['ATMList'][1]['LocationIdentifier']['GeocodeLocation']['Latitude']+","+resultsJson['GetListATMorBranchReply']['ATMList'][1]['LocationIdentifier']['GeocodeLocation']['Longitude'],
                                    "title":"Locate in Map"
                                  }
                            ]
                        },
                        {
                            "title":"Dist: "+resultsJson['GetListATMorBranchReply']['ATMList'][2]['Distance']+" miles,  "+resultsJson['GetListATMorBranchReply']['ATMList'][0]['CommonLocationName'],
                            "subtitle":resultsJson['GetListATMorBranchReply']['ATMList'][2]['LocationIdentifier']['Address']['AddressLine1']+", "+resultsJson['GetListATMorBranchReply']['ATMList'][2]['LocationIdentifier']['Address']['City']+", "+resultsJson['GetListATMorBranchReply']['ATMList'][2]['LocationIdentifier']['Address']['ZipCode'],
                            "buttons":[
                                  {
                                    "type":"web_url",
                                    "url":"https://www.google.com/maps/place/"+resultsJson['GetListATMorBranchReply']['ATMList'][2]['LocationIdentifier']['GeocodeLocation']['Latitude']+","+resultsJson['GetListATMorBranchReply']['ATMList'][2]['LocationIdentifier']['GeocodeLocation']['Longitude'],
                                    "title":"Locate in Map"
                                  }
                            ]
                        },
                        {
                            "title":"Dist: "+resultsJson['GetListATMorBranchReply']['ATMList'][3]['Distance']+" miles,  "+resultsJson['GetListATMorBranchReply']['ATMList'][3]['CommonLocationName'],
                            "subtitle":resultsJson['GetListATMorBranchReply']['ATMList'][3]['LocationIdentifier']['Address']['AddressLine1']+", "+resultsJson['GetListATMorBranchReply']['ATMList'][3]['LocationIdentifier']['Address']['City']+", "+resultsJson['GetListATMorBranchReply']['ATMList'][3]['LocationIdentifier']['Address']['ZipCode'],
                            "buttons":[
                                  {
                                    "type":"web_url",
                                    "url":"https://www.google.com/maps/place/"+resultsJson['GetListATMorBranchReply']['ATMList'][3]['LocationIdentifier']['GeocodeLocation']['Latitude']+","+resultsJson['GetListATMorBranchReply']['ATMList'][3]['LocationIdentifier']['GeocodeLocation']['Longitude'],
                                    "title":"Locate in Map"
                                  }
                            ]
                        },
                        {
                            "title":"Dist: "+resultsJson['GetListATMorBranchReply']['ATMList'][4]['Distance']+" miles,  "+resultsJson['GetListATMorBranchReply']['ATMList'][4]['CommonLocationName'],
                            "subtitle":resultsJson['GetListATMorBranchReply']['ATMList'][4]['LocationIdentifier']['Address']['AddressLine1']+", "+resultsJson['GetListATMorBranchReply']['ATMList'][4]['LocationIdentifier']['Address']['City']+", "+resultsJson['GetListATMorBranchReply']['ATMList'][4]['LocationIdentifier']['Address']['ZipCode'],
                            "buttons":[
                                  {
                                    "type":"web_url",
                                    "url":"https://www.google.com/maps/place/"+resultsJson['GetListATMorBranchReply']['ATMList'][4]['LocationIdentifier']['GeocodeLocation']['Latitude']+","+resultsJson['GetListATMorBranchReply']['ATMList'][4]['LocationIdentifier']['GeocodeLocation']['Longitude'],
                                    "title":"Locate in Map"
                                  }
                            ]
                        }
                    ]
                  }
                }
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
    elif "login_menu" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message":{
              "attachment":{
                 "type":"template",
                  "payload":{
                     "template_type":"generic",
                     "elements":[
                      {
                          "title":"If you are an existing client, please login.",
                          "buttons":[
                             {
                                "type":"account_link",
                                "url":"https://usblogin.herokuapp.com/login.php",
                             }
                         ]
                      }
                    ]
                  }
              }
            }
        })
    elif "log_out" in message_text:
        data = json.dumps({
            "recipient":{
              "id":recipient_id
            },
            "message":{
              "attachment":{
                 "type":"template",
                 "payload":{
                 "template_type":"generic",
              "elements":[
               {
                  "title":"Logout",

                  "buttons":[
                     {
                        "type":"account_unlink"
                     }
                  ]
                }
                ]
              }
            }
          }
       })
    elif "phone" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": "Please enter the 4 digit OTP"
            }
        })
    elif "otp" in message_text:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": "Welcome !You are logged Successfully"
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
        words = text.split(" ")
        output="Level-1-Menu"
        ps = PorterStemmer()
        #words=word_tokenize(text)
        #tokens=nltk.word_tokenize(text)
        #tagged=nltk.pos_tag(tokens)
        #entities=nltk.ne_chunk(tagged)
        print words
        for w in words:
                #print w
                print w
                #print w.lower()
                if(w.lower()=='enrol'):
                        if 'online' in str(words).lower() and 'banking' in str(words).lower():
                            output='Enroll to online banking at https://www.usbank.com/index.html'
                elif(w.lower()=='block'):
                        if 'my' in str(words.lower() and 'card' in str(words).lower():
                            output="login"
                elif(w.lower()=='activat'):
                    output="Card has been Activated"
                elif(w.lower()=='balanc' or w.lower()=='summari'):
                    output="balance_check"
                elif(w.lower()=='histori' or w.lower()=='transact'):
                    if 'cancel' in str(words).lower():
                        output="transaction_receipt"
                    elif 'last' in str(words).lower():
                        output="transaction_history"
                elif(w.lower()=='thanks' or w.lower()=='thank'):
                    output="You are Welcome!"
                 elif(w.lower().isdigit() and len(str(w))):
                    #output="Please find the details here: https://www.usbank.com/locations/locator-results.html?stringquery="+w)+"&branch=y&atm=y"
                    output=w.lower()
                elif(w.lower()=='branch' or w.lower()=='atm'):
                    if 'locat' in str(words.lower() or 'find' in str(words).lower() or 'search' in str(words).lower():
                        output="branch_locate"
                elif(w.lower()=='login'):
                        output="login_menu"
                elif(w.lower()=='log'):
                    if 'out' in str(words).lower():
                        output="log_out"
        send_message(sender_id, output)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug=True)
