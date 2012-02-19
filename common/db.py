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
    cursor = data_dump.find({"date" : {"$gte": start_date, "$lt": end_date}})
    return list(cursor)

#This function takes a list of map
def add_data(date, data_list):
    for data in data_list:
        data_dump.update({"url" : data["url"]},
         {"$set":
                {"category": data["category"],
                 "url" : data["url"],
                 "title" : data["title"],
                 "description" : data["description"],
                 "thumbnail" : data["thumbnail"],
                  "date" : date}}, True)
