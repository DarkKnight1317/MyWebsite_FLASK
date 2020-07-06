from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import time


app = Flask(__name__)
app.secret_key = "hellokey"
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("Login Successful")
        return redirect(url_for("user"))

    else:
        if "user" in session:
            flash("Already Logged In!!!")
            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash(f"You have been successfully logged out!!")
    time.sleep(2)
    return redirect(url_for("login"))


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        usr = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Your email is in session now.")
            return render_template("view.html", email=email, name=usr)
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in.  Please login to continue")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
