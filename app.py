from flask import (
    Flask,
    render_template,
    redirect,
    request,
    flash,
    session,
    g,
    abort,
    url_for,
)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import User, Like, Brewery, db, connect_db
import os

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.jinja_env.filters["zip"] = zip

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///brewery"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
