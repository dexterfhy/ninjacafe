from flask import request

from api.dialogflowApi import detect_intent_via_text
from beans.user import User
from cache import get_current_session_id
from handlers import INTENT_HANDLERS
from main import app
from utils import get_user_from_request, get_user_input_from_request, call_if_all_inputs_not_blank, default_if_blank


@app.route('/')
def hello_world():
    return 'Hello, World!'


# Validates incoming webhook request to make sure required fields are present, before processing request
@app.route('/telegram/webhook', methods=['POST'])
def webhook():
    req_body = request.get_json()

    if req_body is None:
        return "ERROR: No request body", 400

    user = get_user_from_request(req_body)
    session_id = get_current_session_id(user)
    user_input = get_user_input_from_request(req_body)

    call_if_all_inputs_not_blank(user.id, session_id, user_input,
                                 func=lambda: process_request(user, session_id, user_input))

    return ''


# Calls Dialogflow API to trigger an intent match
# Calls the corresponding function handler for the intent result action if present
def process_request(user: User, session_id, user_input):
    intent_result = detect_intent_via_text(session_id, user_input)

    intent_action = default_if_blank(intent_result.action, '')

    call_if_all_inputs_not_blank(intent_action,
                                 func=lambda: INTENT_HANDLERS.get(intent_action, lambda x, y, z: None)(user,
                                                                                                       intent_result,
                                                                                                       session_id))
