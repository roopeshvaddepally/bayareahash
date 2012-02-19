from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def store_email(email): pass
def send_email(email, token): pass

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/subscribe")
def subscribe():
	email = request.values.get("email")
	token = store_email(email)
	send_email(email, token)
	return ''

@app.route("/subscribed")
def subscribed():
	return "thanks for subscribing"

if __name__ == '__main__':
	app.run(debug=True)
