import config
import requests
from datetime import datetime, timedelta
from flask import Blueprint, abort, request, jsonify
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# from liff.db.command import db
from liff.db.models import User, NannyAttandence
from liff.db.choices import LeaveType, AttendanceType
from app import db


configuration = Configuration(access_token=config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LIFF_CHANEL_SECRET)


liff_app_api = Blueprint("liff_app_api", __name__)


# /liff/app/call-off
@liff_app_api.route("/call-off", methods=["POST"])
def call_off():
    data = request.get_json()
    start_time = datetime.fromisoformat(data["start_time"])
    end_time = datetime.fromisoformat(data["end_time"])
    leave_type = data["leave_type"]
    token = data["token"]
    response = requests.get(
        f"https://api.line.me/oauth2/v2.1/verify?access_token={token}"
    )
    response.raise_for_status()
    response = response.json()
    if response["client_id"] != config.LINE_CHANEL_ID:
        raise Exception("Invalid user token")
    if response["expires_in"] <= 0:
        raise Exception("Expired token")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.line.me/v2/profile", headers=headers)
    response.raise_for_status()
    response = response.json()
    user_id = response["userId"]
    display_name = response["displayName"]

    user = User.query.filter_by(line_user_id=user_id).first_or_404()
    row_id = user.id
    if not user:
        new_user = User(name="display_name", line_user_id=user_id)
        db.session.add(new_user)
        db.session.commit()
        row_id = new_user.id

    if None in (start_time, end_time, leave_type):
        raise Exception("start_time, end_time, leave_type cannot be null")
    if end_time < start_time:
        raise Exception("Start time exceeds end time")

    # Calculate the time difference in hour
    time_difference = (end_time - start_time).total_seconds() / 60 / 60
    # round off floating digits to the nearest 0.5
    round_off_hours = round(time_difference * 2) / 2
    new_record = NannyAttandence(
        source_id=AttendanceType.leave.value,
        source_type=LeaveType[leave_type].value,
        is_valid=True,
        start_date=start_time,
        end_date=end_time,
        off_hours=round_off_hours,
        creator=row_id,
        last_modifier=row_id
        # create_date=datetime.now(),
        # last_modified_date=datetime.now(),
    )
    db.session.add(new_record)
    db.session.commit()

    return jsonify("OK"), 200


@liff_app_api.route("/call-off/delete", methods=["DELETE"])
def delete_call_off():
    pass


# 監聽所有來自 /callback 的 Post Request
@liff_app_api.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    print(body)
    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)],
            )
        )
