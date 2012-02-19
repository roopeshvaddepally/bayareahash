from pymongo import Connection

c = Connection()

data_dump = c.bayareahash.data_dump
sent_data = c.bayareahash.sent_data
user_table = c.bayareahash.user_table

email_user = "something"
email_password = "something else"
email_from = "r@v.com"


try:
    from local_settings import *
except ImportError as e:
    print "Inside email importing"
    print e
