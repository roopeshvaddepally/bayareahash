from flask import Flask, render_template, request, jsonify, abort
from common.db import (subscribe_email, admin_query, filter_ids_based_on,
                       set_data_to_send, confirm, unsubscribe)
from common.mail import SendEmail
from common.authentication import authenticate_user
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
    return jsonify(aaData=data)


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


@app.route("/admin_login", methods=['POST', 'GET'])
def admin_login():
    if request.method == "POST":
        user, password = request.form.get("username"), request.form.get("password")
        is_authed = authenticate_user(user, password)
        if is_authed:
            return "logged in"
        else:
            return abort(401)
    elif request.method == "GET":
        return render_template("admin_login.html")

@app.route("/hackerbuddy")
def hacker_buddy_home(methods=['GET']):
    return "home"

@app.route("/hackerbuddy/<hackathon_name>/", methods=['GET'])
def hackathon_details(hackathon_name):
    return "hackathon details"

@app.route("/hackerbuddy/<hackathon_name>/polls/", methods=['GET'])
def hackathon_polls(hackathon_name):
    return "all polls (%s)" % hackathon_name

@app.route("/hackerbuddy/<hackathon_name>/<poll_id>", methods=['GET'])
def poll_details(hackathon_name, poll_id):
    return "poll details for (%s)" % poll_id

@app.route("/hackerbuddy/poll/create", methods=['POST'])
def create_poll():
    poll_title = request.form['title'];
    poll_options = request.form['options'];
    return "Create poll for: " + poll_title + " and options: " + poll_options;


@app.route("/hackerbuddy/poll/vote", methods=['POST'])
def vote_on_poll():
    poll_id=request.form['id'];
    option_id = request.form['option']
    return "Update poll:" + poll_id + " and option: " + option_id;


if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0", 5000, debug=True)
