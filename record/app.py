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
        profile = line_bot_api.get_profile(event.source.user_id)
        summary = line_bot_api.get_group_summary(event.source.group_id)

        user_id = profile.user_id
        display_name = profile.display_name
        group_id = summary.group_id
        message_id = event.message.id
        message = event.message.text

        post = Post(
            user_id=user_id,
            display_name=display_name,
            group_id=group_id,
            message_id=message_id,
            message=message
        )
        db.session.add(post)
        db.session.commit()

        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=display_name))
        # TextSendMessage(text=event.message.text))

    return app
