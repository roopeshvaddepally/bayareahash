from settings import data_dump, sent_data, user_table

def subscribe_email(email):
    token = "abcdef" # TODO: use a md5 hash here
    user_table.insert({
        "email": email,
        "token": token,
        "subscribed": False
    })
    return token

def confirm(email, token):
    user = user_table.find_one({"email": email}, {"token": 1})
    if user.token == token:
        user_table.update({
            "email": email
        }, {
            "subscribed": True
        })

def unsubscribe(email):pass

def admin_query(start_date, end_date):pass
