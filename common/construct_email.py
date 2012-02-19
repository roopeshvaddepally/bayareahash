from string import Template
from common.db import get_data_to_send, get_users_to_send_data
from common.mail import SendEmail

def construct_html_email(email, data):
    result_map = {"html": "<ol>", "plain": ""}

    user_list = get_users_to_send_data()
    data = get_data_to_send()


    #create html
    f = open("templates/email.html", "r")
    text = f.read()
    t = Template(unicode(text, errors='ignore'))
    text = t.substitute(links=result_map["html"] + "</ol>")
    result_map["html"] = text

    send_mail = SendEmail()
    for user in user_list:
        send_mail.send(to=user["email"], html_body="", plain_body=data)

    return result_map
