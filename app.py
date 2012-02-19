from flask import Flask, render_template, request
from common.db import subscribe_email, confirm, unsubscribe
from common.mail import SendEmail

app = Flask(__name__)

mailer = SendEmail()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/subscribe")
def subscribe():
    email = request.values.get("email")
    token = subscribe_email(email)
    mailer.send_email(email, token)
    return ''


@app.route("/admin")
def admin():
    return "admin panel"


if __name__ == '__main__':
    app.run(debug=True)
