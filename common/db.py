from settings import data_dump, sent_data, user_table
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


def admin_query(start_date, end_date):
    cursor = data_dump.find({"date_crawled" : {"$gte": start_date, "$lt": end_date}})
    return list(cursor)


def data_to_send(data_list):
    for data in data_list:
        sent_data.update({"url" : data["url"]},
            {"$set" :
                {"category" : data["category"],
                "url" : data["url"],
                "title" : data["title"],
                "description" : data["description"],
                "thumbnail" : data["thumbnail"],
                "meetup_date" : data["meetup_date"]}}, True)


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
