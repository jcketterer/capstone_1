from csv import DictReader
from app import db
from models import User, Like, Brewery, db

db.drop_all()
db.create_all()

with open("generator/breweries.csv") as breweries:
    db.session.bulk_insert_mappings(Brewery, DictReader(breweries))

# user1 = User(
#     username="jimbo123",
#     first_name="Jim",
#     last_name="Stand",
#     email="ilikebeer@gmail.com",
#     fav_brewery="Founders",
#     password="secret,
# )

# user2 = User(
#     username="Tding34",
#     first_name="Tim",
#     last_name="Dingleberry",
#     email="beerisgood@yahoo.com",
#     fav_brewery="Four Peaks",
#     password="secret32",
# )

# user3 = User(
#     username="HillyHank767",
#     first_name="Hank",
#     last_name="Hill",
#     email="beerpongchamp@aol.com",
#     fav_brewery="Stone Brewery",
#     password="secret135",
# )

# db.session.add_all([user1, user2, user3])
db.session.commit()
