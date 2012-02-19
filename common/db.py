import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def subscribe_email(email):
    pass

def confirm(email):pass

def unsubscribe(email):pass

def admin_query(start_date, end_date):pass
