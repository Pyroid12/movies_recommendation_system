from flask import Flask, render_template, request, redirect, session
from model.recommender import recommend
import pandas as pd

app = Flask(__name__)

app.secret_key = "supersecretkey"


movies = pd.read_csv("model/movies.csv")

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    if request.method == "POST":
        movie = request.form["movie"]
        recommendations = recommend(movie)
    return render_template("index.html",
                           movies=movies["title"].values,
                           recommendations=recommendations)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["user"] = username
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
