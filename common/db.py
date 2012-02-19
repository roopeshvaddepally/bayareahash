from settings import data_dump, sent_data, user_table
import hashlib

def subscribe_email(email):
    m = hashlib.md5()
    m.update(email)
    token = m.digest()
    user_table.update({"email": email}, {"$set": {
        "token": token,
        "subscribed": False
    }}, True)
    return token

def confirm(email, token):
    user = user_table.find_one({"email": email}, {"token": 1})
    if user.token == token:
        user_table.update({"email": email}, {"subscribed": True})

def unsubscribe(email):
    user_table.update({"email": email}, {"$set": {"subscribed": False}})

def admin_query(start_date, end_date):
    data = data_dump.find()


def add_data(date, data_list):
    for data in data_list:
        data_dump.insert({"category": ""})
