from flask import Flask, render_template, request
from common.db import subscribe_email
from common.mail import send_email

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/subscribe")
def subscribe():
    email = request.values.get("email")
    token = subscribe_email(email)
    send_email(email, token)
    return ''


@app.route("/admin")
def admin():
    return "admin panel"

@app.route("/l")
def track():
    return "the URL tracker"

if __name__ == '__main__':
    app.run(debug=True)
