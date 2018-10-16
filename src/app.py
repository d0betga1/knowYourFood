import sys
from messageForms import *
from flask import Flask, request, jsonify
from envVariables import VERIFY_TOKEN

app = Flask(__name__)


# xác nhận bot hoạt động
@app.route("/", methods=['GET'])
def home():
    return jsonify({
		'env':'development'
		,'contact':'tamtm62@wru.vn'
		,'msg': "Hello World, I'm your 🐱‍👤"
		,'error': {
			'errorCode':0
			,'errorMsg':''
		}
	})


# Thống kê trả về JSON qua GET request
@app.route("/stats", methods=['GET'])
def stats():
    return jsonify({
		'msg':"This 🐱‍🚀 is under development, please come back later! 😉"
	})


# verify webhook và xử lí tin nhắn
@app.route("/webhook", methods=['GET', 'POST'])
def listen():
	"""
	Lắng nghe ở endpoint '/webhook' và điều khiển luồng
	"""
	if request.method == 'GET':
		return verify_webhook(request)	

	if request.method == 'POST':
		payload = request.json
		event = payload['entry'][0]['messaging']
		
		for x in event:
			sender_id = x['sender']['id']
			timestamp = x['timestamp']

			# tùy theo dạng tin nhắn mà xử lí
			if is_text_message(x):
				# mặc định với text thì send ghi nhận
				send_typing_on(sender_id)

				text = x['message']['text']
				send_message(
					sender_id
					,text = 'Your request has been recorded, we will contact you soon'
				)

				# send main menu
				send_quick_reply(
					recipient_id
					,text = "Hi 🖖, What can I do for you?"
					,buttons = [
                		{
                    		"content_type":"text"
                    		,"title":"What to eat NEAR ME?"
                    		,"payload":"EAT_NEAR_ME"
                		},{
                    		"content_type":"text"
                    		,"title":"What to eat TODAY?"
                    		,"payload":"EAT_TODAY"	
                		},{
                    		"content_type":"text"
                    		,"title":"🤔 how to use?"
                    		,"payload":"USER_MANUAL"
                		},{
                    		"content_type":"text"
                    		,"title":"feedback"
                    		,"payload":"ERROR_FEEDBACK"
                		},{
                    		"content_type":"text"
                    		,"title":"about me 😊"
                    		,"payload":"ABOUT_ME"
                		}
            		]
				)

				send_typing_off(sender_id)

				print(
					'\n'
					,'Received message from user {0} at {1} with message {2}'
					.format(
						sender_id
						,timestamp
						,text
						,file=sys.stderr
					)
					,'\n'
				)
			elif is_attachments_message(x):
				attachment = x['message']['attachments']
				print(
					'\n'
					'Received attachment from user {0} at {1} with message {2}'
					.format(
						sender_id
						,timestamp
						,attachment
						,file=sys.stderr
					)
					,'\n'
				)
			elif is_postback(x):	
				print(
					'\n'
					'Received postback from user {0} at {1} with payload {2}'
					.format(
						sender_id
						,timestamp
						,x['postback'].get('payload')
						,file=sys.stderr
					)
					,'\n'
				)
			elif is_quick_reply(x):
				send_typing_on(sender_id)

				qr_payload = x['message']['quick_reply']['payload']
				process_qr_message(
					sender_id
					,qr_payload
				)

				send_typing_off(sender_id)

				print(
					'\n'
					'Received quick reply from user {0} at {1} with payload {2}'
					.format(
						sender_id
						,timestamp
						,qr_payload
						,file=sys.stderr
					)
					,'\n'
				)
			elif is_delivery_confirmation(x):
				pass
			elif is_message_read(x):
				pass
			else:
				print(
					'Received unknown 🧀, format:'
					,'\n'
					, x
				)
		# return "200"
		# nếu không sẽ bị timeout
		return "ok" 


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect verify_token from dotenv"


def process_qr_message(recipient_id, qr_payload):
	if qr_payload == 'PICKING_MAIN_MENU':
		send_quick_reply(
			recipient_id
			,text = "Hi 🖖, What can I do for you?"
			,buttons = [
                {
                    "content_type":"text"
                    ,"title":"What to eat NEAR ME?"
                    ,"payload":"EAT_NEAR_ME"
                },{
                    "content_type":"text"
                    ,"title":"What to eat TODAY?"
                    ,"payload":"EAT_TODAY"	
                },{
                    "content_type":"text"
                    ,"title":"🤔 how to use?"
                    ,"payload":"USER_MANUAL"
                }, {
                    "content_type":"text"
                    ,"title":"feedback"
                    ,"payload":"ERROR_FEEDBACK"
                }, {
                    "content_type":"text"
                    ,"title":"about me 😊"
                    ,"payload":"ABOUT_ME"
                }
            ]
		)
	elif qr_payload == 'EAT_NEAR_ME':
		pass
	elif qr_payload == 'EAT_TODAY':
		pass
	elif qr_payload == 'USER_MANUAL':
		pass
	elif qr_payload == 'ERROR_FEEDBACK':
		pass
	elif qr_payload == 'ABOUT_ME':
		pass
	
		

def is_text_message(message):
    """
    Kiểm tra định dạng tin nhắn là text hay không?
	Mẫu text:
	{
	    "object": "page",
	    "entry": [
	        {
	            "id": "2175752579115647",
	            "time": 1538965812484,
	            "messaging": [
	                {
	                    "sender": {
	                        "id": "1841575415878403"
	                    },
	                    "recipient": {
	                        "id": "2175752579115647"
	                    },
	                    "timestamp": 1538965788154,
	                    "message": {
	                        "mid": "TDYskuSLxZk9QAwELJ_BANcxr7SCfamOxl72kjcXKRABF8QV4TRpVTP_fUrTTQuJr_ETg-c2cZIaFxskEn4Mwg",
	                        "seq": 645944,
	                        "text": "hi"
	                    }
	                }
	            ]
	        }
	    ]
	}
    """
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo") and
			not message['message'].get("quick_reply"))


def is_attachments_message(message):
	"""
	{
	    "object": "page",
	    "entry": [
	        {
	            "id": "2175752579115647",
	            "time": 1538989261390,
	            "messaging": [
	                {
	                    "sender": {
	                        "id": "1841575415878403"
	                    },
	                    "recipient": {
	                        "id": "2175752579115647"
	                    },
	                    "timestamp": 1538989260829,
	                    "message": {
	                        "mid": "v5pKYtaW1w1MMaTY9TUkqdcxr7SCfamOxl72kjcXKRA6l1ok07_Vi5KwH7E8oec4hVBTJYLDTfwiXRd3UJxJSQ",
	                        "seq": 646859,
	                        "sticker_id": 369239263222822,
	                        "attachments": [
	                            {
	                                "type": "image",
	                                "payload": {
	                                    "url": "https://scontent.xx.fbcdn.net/v/t39.1997-6/39178562_1505197616293642_5411344281094848512_n.png?_nc_cat=1&_nc_ad=z-m&_nc_cid=0&oh=02bbd329c59b516cd606324f12892cc7&oe=5C192C75",
	                                    "sticker_id": 369239263222822
	                                }
	                            }
	                        ]
	                    }
	                }
	            ]
	        }
	    ]
	}
	"""
	return (message.get('message') and
            message['message'].get('attachments') and
            not message['message'].get("is_echo") and 
			not message['message'].get("quick_reply"))
	

def is_postback(message):
	"""
	Kiểm tra xem có phải postback hay không?
	Mẫu postback:
	{
	    "object": "page",
	    "entry": [
	        {
	            "id": "2175752579115647",
	            "time": 1538966533328,
	            "messaging": [
	                {
	                    "recipient": {
	                        "id": "2175752579115647"
	                    },
	                    "timestamp": 1538966533328,
	                    "sender": {
	                        "id": "1841575415878403"
	                    },
	                    "postback": {
	                        "payload": "PICKING_REVIEW",
	                        "title": "Đánh giá 👍"
	                    }
	                }
	            ]
	        }
	    ]
	}
	"""
	return (message.get('postback') and
            message['postback'].get('payload'))


def is_quick_reply(message):
	"""
	Kiểm tra xem có phải tin nhắn chứa playload từ quick reply
	Mẫu tin nhắn khi user nhấn nút từ quick reply
	{
	    "object": "page",
	    "entry": [
	        {
	            "id": "2175752579115647",
	            "time": 1538994715363,
	            "messaging": [
	                {
	                    "sender": {
	                        "id": "1841575415878403"
	                    },
	                    "recipient": {
	                        "id": "2175752579115647"
	                    },
	                    "timestamp": 1538994714831,
	                    "message": {
	                        "quick_reply": {
	                            "payload": "PICKING_COMEDY"
	                        },
	                        "mid": "fwrgFbWKu5Z8NmiLpkmOzNcxr7SCfamOxl72kjcXKRD64nvTDmcXeAMdvwyCo4iITOoQxlyOf7m7IyLhy7am1g",
	                        "seq": 647412,
	                        "text": "Comedy"
	                    }
	                }
	            ]
	        }
	    ]
	}
	"""
	return (message.get('message') and
            message['message'].get('quick_reply') and
            not message['message'].get("is_echo"))


def is_delivery_confirmation(message):
	"""
	Thông báo rằng tin nhắn đã được gửi 
	Mẫu delivery confirmation:
	{
	    "object": "page",
	    "entry": [
	        {
	            "id": "2175752579115647",
	            "time": 1538988498914,
	            "messaging": [
	                {
	                    "sender": {
	                        "id": "1841575415878403"
	                    },
	                    "recipient": {
	                        "id": "2175752579115647"
	                    },
	                    "timestamp": 1538988498897,
	                    "delivery": {
	                        "mids": [
	                            "-X4dUC1sdXd4zV4t44bVMtcxr7SCfamOxl72kjcXKRDpwrLuOXKDVI5DQ3dag9XaAVs75kKiK9TwiugqzpcioQ"
	                        ],
	                        "watermark": 1538988498427,
	                        "seq": 0
	                    }
	                }
	            ]
	        }
	    ]
	}
	"""
	return (message.get('delivery') and
            message['delivery'].get('watermark'))

def is_message_read(message):
	"""
	{
	    "object": "page",
	    "entry": [
	        {
	            "id": "2175752579115647",
	            "time": 1538988510721,
	            "messaging": [
	                {
	                    "sender": {
	                        "id": "1841575415878403"
	                    },
	                    "recipient": {
	                        "id": "2175752579115647"
	                    },
	                    "timestamp": 1538988510716,
	                    "read": {
	                        "watermark": 1538988498427,
	                        "seq": 0
	                    }
	                }
	            ]
	        }
	    ]
	}
	"""
	return (message.get('read') and
            message['read'].get('watermark'))


if __name__ == '__main__':
  app.run(debug=True)


