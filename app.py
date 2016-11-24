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
##	json_data_final='{"recipient": {"id": sender_id}, "message": {"text": out_msg}}'
##	req = urllib2.Request('https://graph.facebook.com/v2.6/me/messages?access_token=EAAZAgx2FZBzKoBANeLcN8OcYJ8UZApCZBXYjpO29pZC4rQ2xGuJLdBHzmgOOkD22efYJn1OmdAUvYlWBNYZApOjLO167WH0UIA7jYvqsPy3FTKdn4ZBMZAWlenyYFdhKVu5PjzzESrB5wmjXwTZBjThJ2PVhGJbL0CrOJZBI1S82kWlFqMe7de4GRl')
##	req.add_header('Content-Type','application/json')
####	response = urllib2.urlopen(req, json.dumps(json_data_final))
##	response = urllib2.urlopen(req)
##	return '123'
##postingMessage(json_data_final);
                

def postingMessage(json_data):
        req = urllib2.Request('https://graph.facebook.com/v2.6/me/messages?access_token=EAAZAgx2FZBzKoBANeLcN8OcYJ8UZApCZBXYjpO29pZC4rQ2xGuJLdBHzmgOOkD22efYJn1OmdAUvYlWBNYZApOjLO167WH0UIA7jYvqsPy3FTKdn4ZBMZAWlenyYFdhKVu5PjzzESrB5wmjXwTZBjThJ2PVhGJbL0CrOJZBI1S82kWlFqMe7de4GRl')
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(json_data))
        return response;

if __name__ == '__main__':
        app.run()
