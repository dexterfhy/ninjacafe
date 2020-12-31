from beans.item import Item
from beans.user import User


# Returns given string if it is not None or blank, else return default value provided
def default_if_blank(s, default):
    if is_not_blank(s):
        return s
    else:
        return default


# Executes a given lambda if all string params are not None or blank
def call_if_all_inputs_not_blank(*string, func):
    if is_not_blank(string):
        return func()


# Extracts user id from Telegram request
def get_user_from_request(req_body):
    if 'callback_query' in req_body:
        req_from = req_body.get('callback_query', {}).get('from', {})
        return User(req_from.get('id', ''), __get_req_from_name(req_from))
    elif 'message' in req_body:
        req_from = req_body.get('message', {}).get('from', {})
        return User(req_from.get('id', ''), __get_req_from_name(req_from))
    else:
        return ''


# Extracts user's name from Telegram request
def __get_req_from_name(req_from):
    first_name = req_from.get('first_name')
    last_name = req_from.get('last_name')
    if is_not_blank(first_name, last_name):
        return first_name + ' ' + last_name
    elif is_not_blank(first_name):
        return first_name
    else:
        return ''


# Extract's user's input (text or button click) from Telegram request
def get_user_input_from_request(req_body):
    if 'callback_query' in req_body:
        return req_body.get('callback_query', {}).get('data', '')
    elif 'message' in req_body:
        return req_body.get('message', {}).get('text', '')
    else:
        return ''


# Checks where one or more string params provided are None or blank
def is_not_blank(*string):
    return all(s is not None and s for s in string)


# Extracts list of Item objects from intent result that were captured from response
def get_items_from_response(intent_result):
    return __get_numbered_entries_from_response(intent_result.output_contexts[0])\
       + __get_regular_entries_from_response(intent_result.output_contexts[0])


def __get_numbered_entries_from_response(context):
    entries = []

    for captured_item in context.parameters['cafe-order-entry']:
        entries.append(Item(captured_item['menu-item'], int(captured_item['item-number'])))

    return entries


def __get_regular_entries_from_response(context):
    entries = []

    for captured_item in context.parameters['cafe-menu-item']:
        entries.append(Item(captured_item, 1))

    return entries
