#Import python libaries
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy import func
from geoalchemy2 import Geometry
from geoalchemy2 import functions
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
import psycopg2
from geojson_rewind import rewind

#Create flask python app
app = Flask(__name__)

#Create database create create_engine
password = "kmr504rmz36"
engine = create_engine('postgresql://postgres:kmr504rmz36@localhost/StormSurge', echo=True)
print(engine)

#Create declarative_base for table
Base = declarative_base()

#Create class for CityL Limits table
class city_limits(Base):
    __tablename__ = 'city_limits'
    gid = Column(Integer, primary_key=True)
    name = Column(String)
    houseunits = Column(Numeric)
    pop2012 = Column(Numeric)
    sqmi = Column(Numeric)
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('POLYGON', 4326))

#Create class for Category table
class category_1(Base):
    __tablename__ = 'category_1'
    gid = Column(Integer, primary_key=True)
    objectid = Column(Numeric)
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('POLYGON', 4326))


#Create DB sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


def build_cityLimits(session):
    #Ceate query of database
    qry = session.query(city_limits,functions.ST_AsGeoJSON(city_limits.geom))
    #qry = session.query(city_limits1,functions.ST_AsGeoJSON(func.ST_SetSRID(city_limits1.geom,4326)))

    #Create geojson file
    f = open(r"static/city_limits.geojson", 'w')

    #Write first line
    f.write(f'{{"type":"FeatureCollection","features":[')

    for row in qry:
        #print(f'{{"type": "Feature","geometry":{row[1]},"properties": {{"name": {row[0].name}}}}}')

        #Enforce right hand rule
        corrected = rewind(row[1])

        #Check to see if the row is the last element if so remove ending comma for geojson file
        if row != qry[-1]:
            #Write out rows to create geojson file with comma
            f.write(f'{{"type": "Feature","geometry":{corrected},"properties": {{"name": "{row[0].name}"}}}},')
        else:
            #Write out list feature without ending comma
            f.write(f'{{"type": "Feature","geometry":{corrected},"properties": {{"name": "{row[0].name}"}}}}')

    #Write last line
    f.write(f']}}')

    #Close file
    f.close()

def buildCategory(session):
    #Ceate query of database
    qry = session.query(category_1,functions.ST_AsGeoJSON(category_1.geom))

    #Create geojson file
    f = open(r"static/category.geojson", 'w')

    #Write first line
    f.write(f'{{"type":"FeatureCollection","features":[')

    for row in qry:

        #Enforce right hand rule
        corrected = rewind(row[1])

        #Check to see if the row is the last element if so remove ending comma for geojson file
        if row != qry[-1]:
            #Write out rows to create geojson file with comma
            f.write(f'{{"type": "Feature","geometry":{corrected}}},')
        else:
            #Write out list feature without ending comma
            f.write(f'{{"type": "Feature","geometry":{corrected}}}')

    #Write last line
    f.write(f']}}')


#Main web page
@app.route('/')
def index():
    build_cityLimits(session)

    return render_template("index.html")

#Page after user has submitted city and Category
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        city_name = request.form['city']
        category = request.form['category']
        buildCategory(session)

    return render_template("submit.html")


if __name__ == '__main__':
    app.run(debug=True)
