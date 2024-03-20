#Import of the project packages
from flask import Flask,redirect,url_for,render_template,flash
app=Flask(__name__)# initiliaze app and configure the secret key

""" Routes to render our html pages"""
@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)