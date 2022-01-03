import re
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
from sqlalchemy import or_
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import User, Like, Brewery, db, connect_db
from forms import AddUserFrom, LoginForm, EditUserForm
from werkzeug.exceptions import Unauthorized
import os
import requests


CURR_USER_KEY = "curr_user"
API_URL = "https://api.openbrewerydb.org/breweries"

app = Flask(__name__)
app.jinja_env.filters["zip"] = zip

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql://brewery"
)  # .replace("://", "ql://", 1)

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

# ********************* Beer routes ****************************


@app.route('/random')
def random_beer():
    brewery = random_beer()

    for brew in brewery:
        if brew == None:
            return ''

    return render_template("beer/random_beer.html", brewery=brewery)


@app.route('/beer/<int:brew_id>/info', methods=['POST', 'GET'])
def beer_info(brew_id):

    brewery = Brewery.query.filter(Brewery.id == brew_id)

    return render_template("beer/info.html", brewery=brewery)


@ app.route('/allbrew')
def allbrew():
    brews = Brewery.query.all()
    return render_template("beer/allbrew.html", brews=brews)


@ app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        form = request.form
        search_val = form['query']
        search = "%{0}%".format(search_val)
        results = Brewery.query.filter(Brewery.name.like(search)).all()

        return render_template('beer/allbrew.html', brews=results)
    else:
        return redirect('beer/allbrew.html')


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


@ app.route('/users/profile')
def show_user():
    """Shows users account and favorite saved breweries"""

    user_id = g.user.id
    user = User.query.get_or_404(user_id)

    if user:
        return render_template('users/details.html', user=user)
    else:
        return redirect('/')


@ app.route('/users/edit', methods=['POST', 'GET'])
def edit_user():

    if not g.user:
        flash("Access Unauthorized", 'danger')
        return redirect('/')

    user = g.user
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.fav_brewery = form.fav_brewery.data

            db.session.commit()
            return redirect('/users/profile')
        flash("Wrong Password, try again", 'danger')
    return render_template('/users/edit.html', form=form, user_id=user.id)

# **************************** Nav and Search links ***************************


@ app.route('/index')
def brewery_name_searches():
    name = request.args.get('name')
    breweries = []

    if name:
        resp = requests.get(
            f'{API_URL}?by_name={name}&per_page=50', params={"n": name})
        data = resp.json()
        breweries = get_api_response(data)
    return render_template('beer/index.html', breweries=breweries)


@ app.route('/state')
def brewery_state_searches():

    state = request.args.get('state')
    breweries = []

    if state:
        resp = requests.get(
            f'{API_URL}?by_state={state}&per_page=50', params={"s": state})
        data = resp.json()
        breweries = get_api_response(data)
    return render_template('beer/state.html', breweries=breweries)


@ app.route('/city')
def brewery_city_searches():
    city = request.args.get('city')
    breweries = []

    if city:
        resp = requests.get(
            f'{API_URL}?by_city={city}&per_page=50', params={"c": city})
        data = resp.json()
        breweries = get_api_response(data)
    return render_template('beer/city.html', breweries=breweries)

# *************** LIKE ROUTES *************************
