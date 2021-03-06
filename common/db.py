import sys
from os.path import dirname, abspath, join
here = join(dirname(abspath(__file__)), "..")
sys.path.append(here)

from settings import (data_dump, sent_data, user_table, admin_table,
                      hackathon_table, polls_table)
from common.time import get_next_week
try:
    from  pymongo.objectid import ObjectId
except ImportError as ie:
    print "pymongo.objectid.ObjectId is from 1.7 version, trying to import 2.3"
    from bson.objectid import ObjectId
import hashlib


def subscribe_email(email):
    m = hashlib.md5()
    m.update(email)
    token = m.hexdigest()
    user_table.update({"email": email}, {
        "$set": {
            "token": token,
            "subscribed": False
        }
    }, True)
    return token


def confirm(token):
    user = user_table.find_one({"token": token}, {"token": 1})
    if user['token'] == token:
        user_table.update({"token": token}, {"$set": {"subscribed": True}})


def unsubscribe(email):
    user_table.update({"email": email}, {"$set": {"subscribed": False}})


def admin_query():
    times = get_next_week()
    cursor = data_dump.find({
        "date_crawled": {
            "$gte": times[0],
            "$lt": times[1]
         }
    })
    arr = list(cursor)
    for k in arr:
        if len(k['description']) > 75:
            k['description'] = k['description'][:75] + ".."
        k["_id"] = str(k["_id"])
        k["date_crawled"] = k["date_crawled"].strftime('%d%b%Y')
        k["DT_RowId"] = str(k["_id"])
    return arr


def set_data_to_send(data_list):
    for data in data_list:
        sent_data.update({
            "url": data["url"]
        }, {
            "$set": {
                "category": data["category"],
                "url": data["url"],
                "title": data["title"],
                "description": data["description"],
                "thumbnail": data["thumbnail"],
                "meetup_date": data["meetup_date"]
            }
        }, True)


def filter_ids_based_on(ids):
    i = [ObjectId(each) for each in ids]
    cursor = data_dump.find({"_id": {"$in": i}})
    return list(cursor)


def get_data_to_send():
    c = sent_data.find().sort("$natural", -1).limit(1)
    return list(c)


def get_users_to_send_data():
    c = user_table.find({}, {"email": 1})
    return list(c)


def track_url_link(user_email, visited_links):
    user_table.update({"email": user_email}, {"$push": {
        "visited_links": visited_links
    }})


def add_data(date, data_list):
    for data in data_list:
        data_dump.update({
            "url": data["url"]
        }, {
            "$set": {
                  "category": data["category"],
                  "url": data["url"],
                  "title": data["title"],
                  "description": data["description"],
                  "thumbnail": data["thumbnail"],
                  "meetup_date": data["meetup_date"],
                  "date_crawled": date
             }
        }, True)


def get_admin_for_authentication(user):
    admin = admin_table.find_one({"user": user}, {"password": 1}) or {}
    return admin



def get_hackthon_polls(hackathon_title):
    hackathon = hackathon_table.find_one({"title" : hackathon_title}) or {}
    return hackathon.get("polls", [])

def get_all_hackathons():
    return list(hackathon_table.find({}, {"title": 1}))

def get_hackthon_polls_by_name(hackathon_title, poll_name):
    polls = polls_table.find_one({"hackathon_title" : hackathon_title, "poll_title" : poll_name}) or {}
    return polls.get("polls", [])


def create_hackathon(title, description):
    return hackathon_table.insert({
        "title": title,
        "description": description,
        "polls": []
    })


def add_poll_to_hackthon(hackathon_title, poll_title, option_list):
    """
        hackathon_title = String
        poll_title = String
        option_list = [String, String, ... n]
    """
    return _add_poll(hackathon_title, Poll(poll_title, option_list))


def _add_poll(title, poll):
    hackathon_table.update({
        "title": title,
    }, {
        "$addToSet": {
            "polls": poll.title
        }
    })

    polls_table.insert({
        "hackathon_title": title,
        "poll_title": poll.title,
        "polls": poll.option_list
    }, )


def upvote_poll_option(hackathon_title, poll_title, option):
    """
        hackathon_title = String
        poll_title = String
        option =  String
    """
    _update_poll_option(hackathon_title, poll_title, option, 1);


def _update_poll_option(hackathon_title, poll_title, option, up_down):
    """
        hackathon_title = String
        poll_title = String
        option =  String
        up_down = 1/-1
    """

    return polls_table.update({
        'hackathon_title': hackathon_title,
        'poll_title': poll_title,
        'polls.option': option
    }, {
        '$inc': {
            "polls.$.count": up_down
        }
    })

class Poll:
    def __init__(self, title, option_list):
        self.title = title
        self.option_list = [dict(option=k, count=0) for k in option_list]

