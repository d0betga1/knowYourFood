"""
@@ Gửi tin nhắn theo form của Mesenger

POST vào Platform
Sử dụng PAGE_ACCESS_TOKEN và message dạng json 
"""

import requests
from envVariables import FB_API_URL,VERIFY_TOKEN,PAGE_ACCESS_TOKEN


def send_message(recipient_id, text):
    """
    Tin nhắn dạng text
    """
    payload = {
        'message': {
            'text': text
        }
        ,'recipient': {
            'id': recipient_id
        }
    }
    call_send_api(payload)


def send_quick_reply(recipient_id, text, buttons):
    """
    Tin nhắn dạng button lựa chọn nhanh \n
    INPUT \n
    recipient_id: User ID
    text: msg muốn gửi cho user \n
    buttons: [
                {
                    "content_type":"text"
                    ,"title":"Action"
                    ,"payload":"PICKING_ACTION"
                },{
                    "content_type":"text"
                    ,"title":"Comedy"
                    ,"payload":"PICKING_COMEDY"
                },{
                    "content_type":"text"
                    ,"title":"Drama"
                    ,"payload":"PICKING_DRAMA"
                }
            ]
    """
    payload = {
        'message': {
            'text': text
            ,'quick_replies': buttons
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }
    call_send_api(payload)


def send_img_message(recipient_id, img_link):
    """
    Gửi ảnh, có thể là gif hoặc normal img
    """
    payload = {
        'message': {
            'attachment': {
                'type': 'image'
                ,'payload': {
                    'url': img_link
                }
            }
        }
        ,'recipient': {
            'id': recipient_id
        }
    }
    call_send_api(payload)


def send_short_audio_message(recipient_id, audio_link):
    """
    Gửi đoạn âm thanh ngắn
    """
    payload = {
        'message': {
            'attachment': {
                'type': 'audio'
                ,'payload': {
                    'url': audio_link
                }
            }
        }
        ,'recipient': {
            'id': recipient_id
        }
    }
    call_send_api(payload)


def send_short_video_message(recipient_id, video_link):
    """
    Gửi đoạn phim ngắn
    """
    payload = {
        'message': {
            'attachment': {
                'type': 'video'
                ,'payload': {
                    'url': video_link
                }
            }
        }
        ,'recipient': {
            'id': recipient_id
        }
    }
    call_send_api(payload)


def send_button_message(recipient_id, buttons):
    """
    Tin nhắn dạng button dùng postback để xử lí
    mẫu button: [{
            'type': 'web_url'
            ,'url': 'https://www.oculus.com/en-us/rift/'
            ,'title': 'Open web url'
        },{
            'type': 'postback'
            ,'title': 'Trigger Postback'
            ,'payload': 'PICKING_POSTBACK_DEMO'
        },{
            'type': 'phone_number'
            ,'payload': '+01637278181'
            ,'title': 'Call Phone Number'
        }]
    """
    payload = {
        'recipient': {
            'id': recipient_id
        }
        ,'message': {
            'attachment': {
                'type': 'template'
                ,'payload': {
                    'template_type': 'button'
                    ,'text': 'This is test text'
                    ,'buttons': buttons
                }
            }
        }
    }
    call_send_api(payload)


def send_generic_message(recipient_id, elements):
    """
    đây là generic message template
    mẫu elements: [{
            'title': 'rift'
            ,'subtitle': 'Next-generation virtual reality'
            ,'item_url': 'https://www.oculus.com/en-us/rift/'
            ,'image_url': 'https://dustinweb.azureedge.net/image/297233/400/320/oculus-rift-touch-controllers-bundle.jpg'
            ,'buttons': [{
                'type': 'web_url'
                ,'url': 'https://www.oculus.com/en-us/rift/'
                ,'title': 'Open Web URL'
            }, {
                'type': 'postback'
                ,'title': 'Call Postback'
                ,'payload': 'Payload for first bubble'
            }]
        },{
            'title': 'touch'
            ,'subtitle': 'Your Hands, Now in VR'
            ,'item_url': 'https://www.oculus.com/en-us/touch/'
            ,'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Oculus-Rift-CV1-Headset-Front.jpg/300px-Oculus-Rift-CV1-Headset-Front.jpg'
            ,'buttons': [{
                'type': 'web_url'
                ,'url': 'https://www.oculus.com/en-us/touch/'
                ,'title': 'Open Web URL'
            }, {
                'type': 'postback'
                ,'title': 'Call Postback'
                ,'payload': 'Payload for second bubble'
            }]
        }]
    """
    payload = {
        'message': {
            'attachment': {
                'type': 'template'
                ,'payload': {
                    'template_type': 'generic'
                    ,'elements': elements
                }
            }
        }
        ,'recipient': {
            'id': recipient_id
        }
    }
    call_send_api(payload)


def send_read_receipt(recipient_id):
    """
        Seen :)
    """
    payload = {
        'sender_action': 'mark_seen'
        ,'recipient': {
            'id': recipient_id
        }
    }
    call_send_api(payload)


def send_typing_on(recipient_id):
    """
    Bật typing indicator
    """
    payload = {
        'sender_action': 'typing_on'
        ,'recipient': {
            'id': recipient_id
        }
    }
    call_send_api(payload)


def send_typing_off(recipient_id):
    """
    Tắt typing indicator chứ còn gì :)
    """
    payload = {
        'sender_action': 'typing_off'
        ,'recipient': {
            'id': recipient_id
        }
    }
    call_send_api(payload)


def call_send_api(messageData):
    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }
    response = requests.post(
        FB_API_URL,
        params=auth,
        json=messageData
    )
    return response.json()


