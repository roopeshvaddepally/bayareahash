from flask import Flask, render_template, request, jsonify
from common.db import subscribe_email, confirm, unsubscribe, admin_query
from common.time import get_next_week
from common.mail import SendEmail
import json

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
    datetimes = get_next_week()
    data = admin_query()
    return jsonify(aaData = data)


@app.route("/filtered")
def filtered():
    ids = request.values.get("ids")
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


if __name__ == '__main__':
    app.run(debug=True)
