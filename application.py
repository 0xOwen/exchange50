from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/trade")
def trade():
    return render_template("currency.html")

@app.route("/dashboard")
def dashboard():
    return render_template("user_dashboard.html")

if __name__ == "__main__":
    app.debug = True
    app.run()