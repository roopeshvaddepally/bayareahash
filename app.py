from flask import Flask, render_template, request, jsonify
from common.db import subscribe_email
#from common.mail import send_email

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
    return render_template("admin.html")


@app.route("/isadmin")
def isAdmin():
    name = request.values.get("n")
    if (name == "Dhaval" or name == "Roopesh" or name == "Utkarsh"):
        print(name)
        return "true"
    else:
        return "false"


@app.route("/curate")
def curate():
    return jsonify(aaData = [dict(username='g.user',email="g.user.email",id="g.user.id"), dict(username='g.user',email="g.user.email",id="g.user.id"),dict(username='g.user',email="g.user.email",id="g.user.id"),dict(username='g.user',email="g.user.email",id="g.user.id")])


@app.route("/filtered")
def admin():
    ids = request.values.get("ids")
    return "true"


if __name__ == '__main__':
    app.run(debug=True)
