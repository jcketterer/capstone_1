from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    fav_brewery = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=False)

    # navigation is users -> likes and back
    user_likes = db.relationship("Like", backref="users")

    def __repr__(self):
        return f"<User {self.id}: {self.username}, {self.first_name}, {self.last_name}, {self.fav_brewery}>"

    @classmethod
    def sign_up(cls, username, first_name, last_name, date_of_birth, email, fav_brewery, password):
        """Sign up user
        Takes hashed password and adds to DB
        """

        hashed_pw = bcrypt.generate_password_hash(password).decode("UTF-8")

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            email=email,
            fav_brewery=fav_brewery,
            password=hashed_pw,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Locates username and password for authentication

        if user is found it returns the user object otherwise returns false.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_authenticated = bcrypt.check_password_hash(
                user.password, password)
            if is_authenticated:
                return user
        return False


class Like(db.Model):
    """Like model"""

    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True,
    )
    brewery_id = db.Column(
        db.Integer,
        db.ForeignKey("breweries.id"),
        primary_key=True,
    )


class Brewery(db.Model):
    """Brewery Model"""

    __tablename__ = "breweries"

    id = db.Column(db.Integer, primary_key=True,
                   nullable=True, unique=True, autoincrement=True)
    obdb_id = db.Column(db.Text)
    name = db.Column(db.Text, nullable=False)
    brewery_type = db.Column(db.Text, nullable=False)
    street = db.Column(db.Text, nullable=True)
    address_2 = db.Column(db.Text, nullable=True)
    address_3 = db.Column(db.Text, nullable=True)
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=True)
    country_province = db.Column(db.Text, nullable=True)
    postal_code = db.Column(db.String, nullable=False)
    website_url = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    country = db.Column(db.Text, nullable=False)
    longitude = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Text, nullable=True)

    # navigation is brewery -> likes and back

    brewery_likes = db.relationship("Like", backref="breweries")
