from pymongo import Connection

c = Connection()

data_dump = c.bayareahash.data_dump
sent_data = c.bayareahash.sent_data
user_table = c.bayareahash.user_table
