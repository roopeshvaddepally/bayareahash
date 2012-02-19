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
    html_body = render_template("confirmation.html", email=email, token=token)
    text_body = render_template("confirmation.txt", email=email, token=token)
    mailer.send(email, html_body, text_body)
    return ''


@app.route("/admin")
def admin():
    return "admin panel"

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
