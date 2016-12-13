from flask import Flask, request, json
import urllib2
import time
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import mysql.connector
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
        try:
                out_msg = 'How may i help you?'
                flag = 'N'
                json_data_final=''
                ps = PorterStemmer()
                data = request.data
                dataDict = json.loads(data)
                print dataDict
                sender_id= dataDict["entry"][0]["messaging"][0]["sender"]["id"]
                json_data_typing_on={"recipient": {"id": sender_id}, "sender_action": "typing_on"}
                postingMessage(json_data_typing_on);
                db = mysql.connector.connect(host="57d6c12f89f5cf3b4200023e-trialchatbot.rhcloud.com", port=55276, user="admin71gRStw", passwd="26FaVvBK24dr", db="chatbot")
                cur = db.cursor()
                cur.execute('SELECT count(*) from fb_chatbot where sender_id=%s'%sender_id)
                data = cur.fetchone()
                print data[0]
                if data[0] == 0:
                        cur.execute('insert into fb_chatbot(sender_id) values(%s)'%sender_id)
                cur.execute('SELECT question from fb_chatbot where sender_id=%s'%sender_id)
                question=cur.fetchone()[0]
                cur.execute('SELECT status from fb_chatbot where sender_id=%s'%sender_id)
                status=cur.fetchone()[0]
                postbak_msg = dataDict["entry"][0]["messaging"][0]

                if('message' not in postbak_msg):
                        if('postback' not in postbak_msg):
                                link_status=dataDict["entry"][0]["messaging"][0]["account_linking"]["status"]
                                if(link_status=='linked'):
                                        auth_code=dataDict["entry"][0]["messaging"][0]["account_linking"]["authorization_code"]
                                        cur.execute('update fb_chatbot set auth_code=%s where sender_id=%s',(auth_code,sender_id))
                                        cur.execute('select u.username from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                        dataname=cur.fetchone()
                                        print dataname[0]
                                        name = dataname[0]
                                        out_msg = 'Welcome %s'%name
                                elif(link_status=='unlinked'):
                                        cur.execute('update fb_chatbot set auth_code="" where sender_id=%s'%sender_id)
                                        out_msg = 'Logged out successfully'
                        else:
                                if(status=='Y' and question=='BLOCK'):
                                        cardno = dataDict["entry"][0]["messaging"][0]["postback"]["payload"]
                                        cardnumber = "'"+cardno+"'"
                                        cur.execute('update card set card_status="INACTIVE" where card_num=%s'%cardnumber)
                                        cur.execute('update fb_chatbot set status="",question="" where sender_id=%s'%sender_id)
                                        out_msg = 'Card number %s has been blocked successfully'%cardno
                                else:
                                        out_msg=dataDict["entry"][0]["messaging"][0]["postback"]["payload"]
                else:
                        msg = dataDict["entry"][0]["messaging"][0]["message"]
                        if 'text' not in msg:
                                type = dataDict["entry"][0]["messaging"][0]["message"]["attachments"][0]["type"]
                                if type =="image":
                                        out_msg = dataDict["entry"][0]["messaging"][0]["message"]["attachments"][0]["payload"]["url"]
                                elif type =="location":
                                        out_msg = dataDict["entry"][0]["messaging"][0]["message"]["attachments"][0]["title"]
                        else:
                                txt_msg=dataDict["entry"][0]["messaging"][0]["message"]["text"]
                                words = word_tokenize(txt_msg)
                                tokens = nltk.word_tokenize(txt_msg)
                                tagged = nltk.pos_tag(tokens)
                                entities = nltk.ne_chunk(tagged)
                                print entities
                                for w in words:
                                        if(ps.stem(w).lower()=='enrol'):
                                                if 'online' in str(words).lower() and 'banking' in str(words).lower():
                                                        out_msg = 'Enroll to online banking at https://www.newgenbank.com/enroll/olb'
                                        if(ps.stem(w).lower()=='login'):
                                                cur.execute('select u.username from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                                if cur.fetchone():
                                                        out_msg='You already logged into the account.'
                                                else:
                                                        flag='Y'
                                                        json_data_final={"recipient":{"id":sender_id},"message": {"attachment": {"type": "template","payload": {"template_type": "generic","elements": [{"title": "If you are an existing client, please logon for bot banking.","image_url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/resources/images/bank-logo.png","buttons": [{"type": "account_link","url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/login"}]}]}}}}

                                        if(ps.stem(w).lower()=='log'):
                                                if 'me' in str(words).lower() and 'out' in str(words).lower():
                                                        cur.execute('select u.username from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                                        if cur.fetchone():
                                                                flag='Y'
                                                                json_data_final={"recipient":{"id":sender_id},"message": {"attachment": {"type": "template","payload": {"template_type": "generic","elements": [{"title": "Logout","image_url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/resources/images/bank-logo.png","buttons": [{"type": "account_unlink"}]}]}}}}
                                                        else:
                                                                out_msg='You already logged out the account.'
                                        if(ps.stem(w).lower()=='pay'):
                                                cur.execute('select u.username from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                                if cur.fetchone():
                                                        person_name=''
                                                        amount=''
                                                        for subtree in entities.subtrees():
                                                                if subtree.label() == 'PERSON':
                                                                        person_name = "'"+subtree.leaves()[0][0]+"'"
                                                                for leaves in subtree.leaves():
                                                                        if leaves[1] == 'CD':
                                                                                amount = leaves[0]
                                                                if person_name:
                                                                        if amount:
                                                                                cur.execute('select u.olb_id from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                                                                olb_id=cur.fetchone()[0]
                                                                                print 'olb_id%s'%olb_id
                                                                                print 'name%s'%person_name
                                                                                cur.execute('select payee_id from payee_details where nickname=%s and olb_id=%s'%(person_name,olb_id))
                                                                                if cur.fetchone():
                                                                                        cur.execute('select payee_id from payee_details where nickname=%s'%person_name)
                                                                                        payee_id=cur.fetchone()[0]
                                                                                        cur.execute('select p2p_email_id from payee_details where nickname=%s'%person_name)
                                                                                        email_id=cur.fetchone()[0]
                                                                                        print 'payee id%s'%payee_id
                                                                                        cur.execute('insert into transaction_details values(%s,"231456",%s,"Payment",%s,%s)'%(olb_id,"'"+time.strftime('%Y-%m-%d')+"'",amount,payee_id))
                                                                                        cur.execute('update fb_chatbot set status="Y",question="OTP" where sender_id=%s'%sender_id)
                                                                                        out_msg = 'Please enter a OTP sent to your mobile'
                                                                                else:
                                                                                        out_msg = 'Payee nickname not found.'

                                                                        else:
                                                                                out_msg = 'Please enter a amount'
                                                                else:
                                                                        out_msg = 'Please enter a payee name'
                                                else:
                                                        flag='Y'
                                                        json_data_final={"recipient":{"id":sender_id},"message": {"attachment": {"type": "template","payload": {"template_type": "generic","elements": [{"title": "If you are an existing client, please logon for bot banking.","image_url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/resources/images/bank-logo.png","buttons": [{"type": "account_link","url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/login"}]}]}}}}
                                        if(ps.stem(w).lower()=='transact'):
                                                cur.execute('select u.username from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                                if cur.fetchone():
                                                        number=''
                                                        for subtree in entities.subtrees():
                                                                for leaves in subtree.leaves():
                                                                        if leaves[1] == 'CD':
                                                                                number = leaves[0]
                                                                print 'Nu,ber%s'%number
                                                                cur.execute('select u.olb_id from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                                                olb_id=cur.fetchone()[0]
                                                                if number:
                                                                        print '1'
                                                                        cur.execute('select td.date,td.tran_amount,td.tran_desc from transaction_details td,payee_details pd where td.payee_id=pd.payee_id and td.olb_id=%s LIMIT %s'%(olb_id,number))
                                                                        if cur.fetchall():
                                                                                cur.execute('select td.date,td.tran_amount,td.tran_desc from transaction_details td,payee_details pd where td.payee_id=pd.payee_id and td.olb_id=%s LIMIT %s'%(olb_id,number))
                                                                                data=cur.fetchall()
                                                                                print '2'
                                                                                print data
                                                                                string_result = ''
                                                                                string_result +='Date   Amount  Description'+'\n'
                                                                                for row in data:
                                                                                        sringout= str(row).replace("(", "").replace(")","").split(',')
                                                                                        outstring = ''
                                                                                        for index in range(len(sringout)):
                                                                                                if(index==1):
                                                                                                        tempString = str(sringout[index]).replace("u","").replace("'","").replace(" ", "")
                                                                                                        outstring += " $"+tempString
                                                                                                else:
                                                                                                        outstring += str(sringout[index]).replace("u","").replace("'","")
                                                                                        print outstring
                                                                                        string_result += outstring + '\n'
                                                                                print string_result
                                                                                out_msg = string_result
                                                                        else:
                                                                                out_msg = 'No transactions.'

                                                                else:
                                                                        out_msg = 'Please enter a no of transactions'
                                                else:
                                                        flag='Y'
                                                        json_data_final={"recipient":{"id":sender_id},"message": {"attachment": {"type": "template","payload": {"template_type": "generic","elements": [{"title": "If you are an existing client, please logon for bot banking.","image_url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/resources/images/bank-logo.png","buttons": [{"type": "account_link","url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/login"}]}]}}}}
                                        if(ps.stem(w).lower()=='balanc'):
                                                cur.execute('select u.username from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                                if cur.fetchone():
                                                        cur.execute('select ab.available_bal from user u,fb_chatbot fb,account_balance ab where ab.olb_id=u.olb_id and u.auth_code=fb.auth_code and ab.acct_type="Checking" and fb.sender_id=%s'%sender_id)
                                                        balance=cur.fetchone()[0]
                                                        out_msg = 'Checking account balance is $%s'%balance
                                                else:
                                                        flag='Y'
                                                        json_data_final={"recipient":{"id":sender_id},"message": {"attachment": {"type": "template","payload": {"template_type": "generic","elements": [{"title": "If you are an existing client, please logon for bot banking.","image_url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/resources/images/bank-logo.png","buttons": [{"type": "account_link","url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/login"}]}]}}}}

                                        if(ps.stem(w).lower()=='spent'):
                                                cur.execute('select u.username from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                                if cur.fetchone():
                                                        cur.execute('select u.olb_id from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                                        olb_id=cur.fetchone()[0]
                                                        descstring = []
                                                        string_result = ''
                                                        string_result +='Please find the below details'+'\n\n'
                                                        for subtree in entities.subtrees():
                                                                for leaves in subtree.leaves():
                                                                        if leaves[1] == 'NNP':
                                                                                descstring.append(leaves[0])
                                                                break
                                                        if not descstring:
                                                                out_msg = 'Please specify the shop or payment description'
                                                        else:
                                                                for desc in descstring:
                                                                        querystring="'%"+desc.lower()+"%'"
                                                                        cur.execute('select sum(tran_amount) from transaction_details where olb_id = %s and tran_desc like %s'%(olb_id,querystring))
                                                                        balance=cur.fetchone()[0]
                                                                        if balance is None:
                                                                                balance = 0
                                                                        string_result += 'You spent $%s on %s'%(balance,desc)+'\n'
                                                                out_msg = string_result
                                                else:
                                                        flag='Y'
                                                        json_data_final={"recipient":{"id":sender_id},"message": {"attachment": {"type": "template","payload": {"template_type": "generic","elements": [{"title": "If you are an existing client, please logon for bot banking.","image_url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/resources/images/bank-logo.png","buttons": [{"type": "account_link","url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/login"}]}]}}}}

                                        if(ps.stem(w).lower()== 'atm'):
                                                for subtree in entities.subtrees():
                                                        if subtree.label() == 'GPE':
                                                                print subtree.label()
                                                                print "if"
                                                                location = subtree.leaves()[0][0]
                                                                if(location.lower()=="raleigh"):
                                                                        flag='Y'
                                                                        json_data_final={"recipient": {"id": sender_id}, "message":{"attachment": {"type": "template", "payload": {"template_type":"button","text":"List Of ATM's in Raleigh","buttons":[{"type":"web_url","url":"http://maps.google.com/?q=35.785878,-78.661062","title":"Oberlin Road"},{"type":"web_url","url":"http://maps.google.com/?q=35.836635,-78.645072","title":"North Hills"},{"type":"web_url","url":"http://maps.google.com/?q=35.805156,-78.647335","title":"Fairview Road"}]}}}}
                                                                else:
                                                                        out_msg="We don't have any ATM'S in this loaction."
                                                        else:
                                                                print "else"
                                                                cur.execute('update fb_chatbot set status="Y",question="LOCATION" where sender_id=%s'%sender_id)
                                                                out_msg="Plese enter a location."
                                        if(ps.stem(w).lower()=='block'):
                                                cur.execute('select u.username from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                                if cur.fetchone():
                                                        cur.execute('select u.olb_id from user u,fb_chatbot fb where u.auth_code=fb.auth_code and fb.sender_id=%s'%sender_id)
                                                        olb_id=cur.fetchone()[0]
                                                        print olb_id
                                                        cur.execute('select card_num from card where olb_id=%s'%olb_id)
                                                        data=cur.fetchall()
                                                        print data
                                                        stringcard=''
                                                        stringcard+='{"recipient": {"id": '+sender_id+'}, "message":{"attachment": {"type": "template", "payload": {"template_type":"button","text":"Please choose the card","buttons":['
                                                        for row in data:
                                                                card_num=str(row).replace("u","").replace("'","").replace(",","").replace("(","").replace(")","")
                                                                stringcard+='{"type":"postback","title":"'+card_num+'","payload":"'+card_num+'"},'
                                                        finalstr=stringcard[:-1]
                                                        finalstr+=']}}}}'
                                                        print finalstr
                                                        flag='Y'
                                                        json_data_final=json.loads(finalstr)
                                                        cur.execute('update fb_chatbot set status="Y",question="BLOCK" where sender_id=%s'%sender_id)
                                                else:
                                                        flag='Y'
                                                        json_data_final={"recipient":{"id":sender_id},"message": {"attachment": {"type": "template","payload": {"template_type": "generic","elements": [{"title": "If you are an existing client, please logon for bot banking.","image_url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/resources/images/bank-logo.png","buttons": [{"type": "account_link","url": "https://chatbot-trialchatbot.rhcloud.com/SpringMVCloginExample/login"}]}]}}}}

                                if(status=="Y" and question=="LOCATION"):
                                        for subtree in entities.subtrees():
                                                if subtree.label() == 'GPE':
                                                        print subtree.label()
                                                        location = subtree.leaves()[0][0]
                                                        if(location.lower()=="raleigh"):
                                                                out_msg="ATM list in Raleigh"
                                                                flag='Y'
                                                                json_data_final={"recipient": {"id": sender_id}, "message":{"attachment": {"type": "template", "payload": {"template_type":"button","text":"List Of ATM's in Raleigh","buttons":[{"type":"web_url","url":"http://maps.google.com/?q=35.785878,-78.661062","title":"Oberlin Road"},{"type":"web_url","url":"http://maps.google.com/?q=35.836635,-78.645072","title":"North Hills"},{"type":"web_url","url":"http://maps.google.com/?q=35.805156,-78.647335","title":"Fairview Road"}]}}}}
                                                        else:
                                                                out_msg="We don't have any ATM'S in this loaction."
                                                        cur.execute('update fb_chatbot set status="",question="" where sender_id=%s'%sender_id)
                                if(status=="Y" and question=="OTP"):
                                        cur.execute('select p2p_email_id from payee_details where nickname="John"')
                                        email_id=cur.fetchone()[0]
                                        out_msg = 'Payment completed successfully to %s'%email_id
                    cur.execute('update fb_chatbot set status="",question="" where sender_id=%s'%sender_id)
                print "sender id %s" %sender_id
                json_data_typing_off={"recipient": {"id": sender_id}, "sender_action": "typing_off"}
                postingMessage(json_data_typing_off);
                if(flag=='N'):
                        json_data_final={"recipient": {"id": sender_id}, "message": {"text": out_msg}}

                postingMessage(json_data_final);
                db.commit()
                cur.close()
                db.close()
        except Exception as e:
                print(str(e))
        return "ok"

def postingMessage(json_data):
        req = urllib2.Request('https://graph.facebook.com/v2.6/me/messages?access_token=EAAWZA5iaZAErIBAAMnGkbZCDQyQJSHFqls0sVshQrRrPtBCoARBiJj5cZA7OxHwGbJjR9IBgdB3c84UaIBPDTbR7LAWGnbfmMYqUX09duaO5hKlTyrXN1h5NEwqtpR0ijIKXlCrjP4adQRAL8ZA91LJ8iYZB9GwpZAItsyOQqkvTgZDZD')
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(json_data))
        return response;

if __name__ == '__main__':
        app.run()
