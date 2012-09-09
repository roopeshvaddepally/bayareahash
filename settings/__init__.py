from pymongo import Connection

c = Connection()

data_dump = c.bayareahash.data_dump
sent_data = c.bayareahash.sent_data
user_table = c.bayareahash.user_table
admin_table = c.bayareahash.admin_table

hackathon_table = c.hackerbuddy.hackathon
polls_table = c.hackerbuddy.polls_table

email_user = "something"
email_password = "something else"
email_from = "r@v.com"


try:
    # import setting from local file, assert for satisying pyflakes
    from local_settings import email_user, email_password, email_from
    assert email_user
    assert email_password
    assert email_from
except ImportError as e:
    print "Inside email importing"
    print e
