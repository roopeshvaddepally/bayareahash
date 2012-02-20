from flask import Flask, render_template, request, jsonify
from common.db import (subscribe_email, admin_query, filter_ids_based_on,
                       set_data_to_send, confirm, unsubscribe)
from common.mail import SendEmail
import os

app = Flask(__name__)

mailer = SendEmail()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/subscribe")
def subscribe():
    email = request.values.get("email")
    token = subscribe_email(email)
    html_body = render_template("confirmation.html", email=email, token=token)
    text_body = render_template("confirmation.txt", email=email, token=token)
    mailer.send(email, html_body, text_body)
    return ''


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/isadmin")
def isAdmin():
    name = request.values.get("n")
    if (name == "Dhaval" or name == "Roopesh" or name == "Utkarsh"):
        return "true"
    else:
        return "false"


@app.route("/curate")
def curate():
    data = admin_query()
    return jsonify(aaData = data)


@app.route("/filtered")
def filtered():
    ids = request.values.get("ids")
    filtered = filter_ids_based_on(ids.split(","))
    set_data_to_send(filtered)
    return "true"

@app.route("/l")
def track():
    return "the URL tracker"

@app.route("/confirm")
def confirmation():
    token = request.values.get("token")
    confirm(token)
    return "confirmed. Thanks"


@app.route("/unsubscribe")
def unsubscribe_email():
    email = request.values.get("email")
    unsubscribe(email)

@app.route("/trigger")
def trigger():
    os.system("python common/run.py &")
    return "Your request has been submitted, sending out emails now!"

if __name__ == '__main__':
    app.debug = True
    app.run()
