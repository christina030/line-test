from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

from message import check_handle_message
from rep import create_tables

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

create_tables()

shared_folder = 'shared'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('""" InvalidSignatureError """')
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('""" handle message """')
    check_handle_message(event, line_bot_api, shared_folder)

@handler.add(PostbackEvent)
def handle_postback(event):
    print('""" handle message """')
    check_handle_message(event, line_bot_api, shared_folder)
    # ts = event.postback.data
    # print(ts)
    # keyword = ts[7:]
    # print(keyword)
    # if ts[7:] == '{}'.format(keyword):

    #     text_message = TextSendMessage(text='訊息{}'.format(keyword))

    #     line_bot_api.reply_message(event.reply_token, text_message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
