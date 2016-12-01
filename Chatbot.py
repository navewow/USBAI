from flask import Flask, request, json
import urllib2

app = Flask(__name__)


@app.route('/ChatBot', methods=['GET'])
def verify():
        token = request.args.get('hub.verify_token')
        if token == "123":
                return request.args.get('hub.challenge')
        else:
                return "error"


@app.route('/ChatBot', methods=["POST"])
def webhook():       
	out_msg = 'How may i help you?'
	data = request.get_json()
	print data
	return "Hello World"
##	json_data_final={"recipient": {"id": sender_id}, "message": {"text": out_msg}}                                        
##	postingMessage(json_data_final);
##                
##
##def postingMessage(json_data):
##        req = urllib2.Request('https://graph.facebook.com/v2.6/me/messages?access_token=EAAWZA5iaZAErIBAAMnGkbZCDQyQJSHFqls0sVshQrRrPtBCoARBiJj5cZA7OxHwGbJjR9IBgdB3c84UaIBPDTbR7LAWGnbfmMYqUX09duaO5hKlTyrXN1h5NEwqtpR0ijIKXlCrjP4adQRAL8ZA91LJ8iYZB9GwpZAItsyOQqkvTgZDZD')
##        req.add_header('Content-Type', 'application/json')
##        response = urllib2.urlopen(req, json.dumps(json_data))
##        return response;

if __name__ == '__main__':
        app.r12:36 PM 11/25/2016un()
