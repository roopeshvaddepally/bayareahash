import logging

from marrow.mailer import Mailer, Message
import datetime
from construct_email import construct_html_email
from settings import email_username, email_password, email_from

username = email_username
password = email_password
from_email = email_from
subject = 'something something'
logging.basicConfig(filename='email.log', level=logging.INFO)

class SendEmail(object):
    def __init__(self):
        self.mailer = Mailer(dict(
            transport = dict(
                use = 'smtp',
                host = 'smtp.gmail.com',
                port = '587',
                username = username,
                password = password,
                tls = 'required',
                debug = False),
            manager = dict()))
        self.mailer.start()

    def send(self, to, html_body, plain_body):
        message = Message(author=from_email, to=to)
        message.subject = subject
        message.plain = plain_body
        message.rich = html_body
        self.mailer.send(message)

    def stop_sending(self):
        self.mailer.stop()

    def send_email(self):
        '''Get the result map, format the email and send out emails'''
        logging.info('Sending emails on: ' + str(datetime.datetime.now()))

        final_result = {"to" : "data"}
        for email, data in final_result.iteritems():
            body = construct_html_email(email, data)
            logging.info('To: '+ email)
            self.send(email, body["html"], body["plain"])

        self.stop_sending()

