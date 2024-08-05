
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('sSNOXtlLZBqfShUWVZ+8E9G6vJ8oJ6DeCko6W3JMtuJ0LCX34nN5vZmR4clLSfjPOxJEYzxDcYiaRKKEambzjzBHE1HkkypKXmvVjyFhwcsSmiq1wbpg5/9rXGQp+DxA7i9T40E0DLJXvQut4N2z9wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1b50c8991709b0e4d6a9de7f131e7f81')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    plate_number = event.message.text
    parking_spot, image_url = get_parking_spot_and_image(plate_number)
    
    if parking_spot and image_url:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=f'?牌? {plate_number} ??的?位?是: {parking_spot}'),
                ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
            ]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='未找到??的?位?或?片')
        )

def get_parking_spot_and_image(plate_number):
    database = {
        'ABC123': ('P1', 'https://example.com/parking_spot_1.jpg'),
        'XYZ789': ('P2', 'https://example.com/parking_spot_2.jpg'),
    }
    return database.get(plate_number)

if __name__ == "__main__":
    app.run(debug=True)

