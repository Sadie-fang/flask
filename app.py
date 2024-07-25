from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os
import schedule
import time
from threading import Thread

app = Flask(__name__)

LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

if LINE_CHANNEL_SECRET is None or LINE_CHANNEL_ACCESS_TOKEN is None:
    print("Please set LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.")
    exit(1)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #group_id = event.source.group_id if hasattr(event.source, 'group_id') else None
    #if group_id:
    #    print("Group ID: ", group_id)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def job():

    with open("output.txt", "r") as f:
        content = f.read()
    
    line_bot_api.push_meisage(
        'YOUR_GROUP_ID',
        TextSendMessage(text=content)
    )

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

#schedule.every().day.at("09:03").do(job)
#schedule.every().day.at("12:03").do(job)
#schedule.every().day.at("15:03").do(job)
#schedule.every().day.at("18:03").do(job)

#t= Thread(target=run_schedule)
#t.start()

if __name__ == "__main__":
    app.run()

