import os
from flask import Flask, request, abort

from .models import Post
from .extentions import db


from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(CHANNEL_SECRET)

    @app.route("/callback", methods=['POST'])
    def callback():
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)

        return 'OK'

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        user_id = event.source.user_id
        msg_body = event.message.text

        post = Post(
            line_user_id=user_id,
            message=msg_body
        )
        db.session.add(post)
        db.session.commit()

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_id))
        # TextSendMessage(text=event.message.text))

    return app
