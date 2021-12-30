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
from forms import AddUserFrom, LoginForm, StateForm
# from api import get_api_response
import os
import requests


CURR_USER_KEY = "curr_user"
API_URL = "https://api.openbrewerydb.org/breweries"

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


def login_user(user):

    session[CURR_USER_KEY] = user.id


def logout_user():

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
            user = User.sign_up(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                date_of_birth=form.date_of_birth.data,
                email=form.email.data,
                fav_brewery=form.fav_brewery.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username is already taken", 'danger')
            return render_template('users/signup.html', form=form)

        login_user(user)

        return redirect('/')

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            login_user(user)

            flash(f'Hey! {user.username}!', 'success')
            return redirect('/')

        flash('Invalid Username/Password', 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():

    logout_user()

    flash('You are logged out! See you next time!', 'success')
    return redirect('/login')


@app.route("/")
def base():

    return render_template("home.html")


@app.route('/random')
def random_beer():
    brewery = random_beer()

    for brew in brewery:
        if brew == None:
            return ''

    return render_template("beer/random_beer.html", brewery=brewery)


# ******************** Functions for brewery data ****************************

def random_beer():
    resp = requests.get(f'{API_URL}/random')

    beers = resp.json()
    brewery = []

    for beer in beers:

        b = beer
        brewery.append(b)

    return brewery


def get_api_response(data):
    brews = data

    breweries = []

    for brew in brews:

        beer = {
            'name': brew['name'],
            'brewery_type': brew['brewery_type'],
            'state': brew['state'],
            'city': brew['city'],
            'country': brew['country'],
            'website_url': brew['website_url'],
        }

        breweries.append(beer)
    return breweries
# ********************* Standard User Routes **********************************


@app.route('/users/saved')
def show_user():
    """Shows users account and favorite saved breweries"""

    user_id = g.user.id
    user = User.query.get_or_404(user_id)

    if user:
        return render_template('users/details.html', user=user)
    else:
        return render_template('users/details.html')

# **************************** Nav and Search links ***************************


@app.route('/index')
def brewery_name_searches():
    name = request.args.get('name')
    breweries = []

    if name:
        resp = requests.get(f'{API_URL}?by_name={name}', params={"n": name})
        data = resp.json()
        breweries = get_api_response(data)
    return render_template('beer/index.html', breweries=breweries)


@app.route('/state')
def brewery_state_searches():

    state = request.args.get('state')
    breweries = []

    if state:
        resp = requests.get(f'{API_URL}?by_state={state}', params={"n": state})
        data = resp.json()
        breweries = get_api_response(data)
    return render_template('beer/state.html', breweries=breweries)


@app.route('/city')
def brewery_city_searches():
    city = request.args.get('city')
    breweries = []

    if city:
        resp = requests.get(f'{API_URL}?by_city={city}', params={"n": city})
        data = resp.json()
        breweries = get_api_response(data)
    return render_template('beer/city.html', breweries=breweries)
