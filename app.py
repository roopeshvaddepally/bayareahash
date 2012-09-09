from flask import Flask, render_template, request, jsonify, abort
from common.db import (subscribe_email, admin_query, filter_ids_based_on,
                       set_data_to_send, confirm, unsubscribe, create_hackathon, add_poll_to_hackthon,
                       upvote_poll_option, get_hackthon_polls, get_hackthon_polls_by_name, get_all_hackathons)
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




#HackerBuddy app
@app.route("/hackerbuddy")
def hacker_buddy_home(methods=['GET']):
    return jsonify(result=get_all_hackathons())

@app.route("/hackerbuddy/<hackathon_name>/polls/", methods=['GET'])
def hackathon_polls(hackathon_name):
    return jsonify(result=get_hackthon_polls(hackathon_name))

@app.route("/hackerbuddy/<hackathon_name>/<poll_name>", methods=['GET'])
def poll_details(hackathon_name, poll_name):
    return jsonify(result=get_hackthon_polls_by_name(hackathon_name, poll_name))

@app.route("/hackerbuddy/hackathon/create", methods=['POST'])
def create_new_hackathon():
    hackathon_title = request.form['title']
    hackathon_desc = request.form['desc']
    print("Create poll for: " + hackathon_title + " and options: " + hackathon_desc)
    create_hackathon(hackathon_title, hackathon_desc)

    return jsonify(result="SUCCESS")

@app.route("/hackerbuddy/poll/create", methods=['POST'])
def create_poll():
    hackathon_title = request.form['hackathon_title']
    poll_title = request.form['poll_title']
    poll_options = request.form.getlist('option')
    print("Create poll for: " + poll_title + " and options: " + str(poll_options))

    add_poll_to_hackthon(hackathon_title, poll_title, poll_options)

    return jsonify(result="SUCCESS")


@app.route("/hackerbuddy/poll/vote", methods=['POST'])
def vote_on_poll():
    hackathon_title = request.form['hackathon_title']
    poll_title=request.form['poll_title']
    option = request.form['option']
    print("Update poll:" + poll_title + " and option: " + option)

    upvote_poll_option(hackathon_title, poll_title, option)

    return jsonify(result="SUCCESS")


if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0", 5000, debug=True)
