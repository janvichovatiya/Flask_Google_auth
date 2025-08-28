from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
    timeout=30000,
)


@app.route("/")
def index():
    if "google_token" in session:
        resp = google.get("https://www.googleapis.com/oauth2/v3/userinfo")
        return resp.json()
    return '<a href="/login">Login with Google</a>'


@app.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/authorize")
def authorize():
    token = google.authorize_access_token()
    session["google_token"] = token
    resp = google.get("https://www.googleapis.com/oauth2/v3/userinfo")
    return resp.json()


@app.route("/logout")
def logout():
    session.pop("google_token", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
