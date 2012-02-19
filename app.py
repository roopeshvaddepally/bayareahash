from flask import Flask, render_template, request, redirect, url_for
from common.db import subscribe
from common.mail import send_email

app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/subscribe")
def subscribe():
	email = request.values.get("email")
	token = subscribe(email)
	send_email(email, token)
	return ''


if __name__ == '__main__':
	app.run(debug=True)
