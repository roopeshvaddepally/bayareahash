# import logging

from marrow.mailer import Mailer, Message
from settings import email_user, email_password, email_from
from common.db import get_data_to_send, get_users_to_send_data

username = email_user
password = email_password
from_email = email_from
subject = 'something something'
# logging.basicConfig(filename='email.log', level=logging.INFO)


class SendEmail(object):
    def __init__(self):
        self.mailer = Mailer(dict(
            transport=dict(
                use='smtp',
                host='smtp.gmail.com',
                port='587',
                username=username,
                password=password,
                tls='required',
                debug=False),
            manager=dict()))
        self.mailer.start()

    def send(self, to, html_body, plain_body):
        message = Message(author=from_email, to=to)
        message.subject = subject
        message.plain = plain_body
        message.rich = html_body
        self.mailer.send(message)

    def stop_sending(self):
        self.mailer.stop()

    def construct_html_email(self):
        user_list = get_users_to_send_data()
        data = get_data_to_send()

        #create html
        #f = open("templates/email.html", "r")
        #text = f.read()
        #t = Template(unicode(text, errors='ignore'))
        #text = t.substitute(links=result_map["html"] + "</ol>")
        #result_map["html"] = text

        for user in user_list:
            self.send(to=user["email"], html_body="%s" % data,
                      plain_body="data_plain")
