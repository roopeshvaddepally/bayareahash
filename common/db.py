import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
namespace = "area42:bahashed:"
data_table = namespace+"datadump:"
sent_table = namespace+"sent:"
user_table = namespace+"user:"

def subscribe(email):
	pass

def confirm(email):pass

def unsubscribe(email):pass

def admin_query(start_date, end_date):pass
