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
from forms import AddUserFrom
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
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "shhhhhhhh")
toolbar = DebugToolbarExtension(app)

connect_db(app)


####################### Sign Up, Login, Logout routes ####################


@app.before_request
def g_user():

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def login(user):

    session[CURR_USER_KEY] = user.id


def logout():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Creates user adds user to DB and sends back to homepage"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = AddUserFrom()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                date_of_brith=form.date_of_brith.data,
                email=form.email.data,
                fav_brewery=form.fav_brewery.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError as error:
            flash("Username is already taken", 'danger')
            return render_template('users/signup.html', form=form)

        login(user)

        return redirect('/')

    else:
        return render_template('users/signup.html', form=form)


@app.route("/")
def base():
    return render_template("base.html")
