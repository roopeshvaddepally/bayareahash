import sys
from os.path import dirname, abspath, join
here = join(dirname(abspath(__file__)), "..")
sys.path.append(here)

from settings import data_dump, sent_data, user_table
from common.time import get_next_week
import hashlib


def subscribe_email(email):
    m = hashlib.md5()
    m.update(email)
    token = m.hexdigest()
    user_table.update({"email": email}, {"$set": {
        "token": token,
        "subscribed": False
    }}, True)
    return token


def confirm(token):
    user = user_table.find_one({"token": token}, {"token": 1})
    if user['token'] == token:
        user_table.update({"token": token}, {"$set": {"subscribed": True}})


def unsubscribe(email):
    user_table.update({"email": email}, {"$set": {"subscribed": False}})


def admin_query():
    times = get_next_week()
    cursor = data_dump.find({"date_crawled" : {"$gte": times[0], "$lt": times[1]}})
    arr = list(cursor)
    for k in arr:
        k["description"] = (k["description"][:75] + '..') if len(k["description"]) > 75 else k["description"]
        k["_id"] = str(k["_id"])
        k["date_crawled"] = k["date_crawled"].strftime('%d%b%Y')
    return arr


def set_data_to_send(data_list):
    for data in data_list:
        sent_data.update({"url" : data["url"]},
            {"$set" :
                {"category" : data["category"],
                "url" : data["url"],
                "title" : data["title"],
                "description" : data["description"],
                "thumbnail" : data["thumbnail"],
                "meetup_date" : data["meetup_date"]}}, True)


def get_data_to_send():
    c = sent_data.find().sort("$natural", -1).limit(1)
    return list(c)


def get_users_to_send_data():
    c = user_table.find({}, {"email": 1})
    return list(c)


def track_url_link(user_email, visited_links):
    user_table.update({"email": user_email}, {"$push" : {"visited_links" : visited_links}})


def add_data(date, data_list):
    for data in data_list:
        data_dump.update({"url" : data["url"]},
         {"$set":
                {"category": data["category"],
                 "url" : data["url"],
                 "title" : data["title"],
                 "description" : data["description"],
                 "thumbnail" : data["thumbnail"],
                 "meetup_date" : data["meetup_date"],
                 "date_crawled" : date}}, True)
