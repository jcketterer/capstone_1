from csv import DictReader
from app import db
from models import Brewery

db.drop_all()
db.create_all()

with open("generator/usa_breweries.csv") as breweries:
    db.session.bulk_insert_mappings(Brewery, DictReader(breweries))

db.session.commit()
