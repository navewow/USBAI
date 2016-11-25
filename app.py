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
##	sender_id='123'
	data = request.get_json()
	print data
	return "Welcome"


if __name__ == '__main__':
        app.run()
