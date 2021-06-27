#Import python libaries
from flask import Flask, render_template
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

#Create DB sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

#Ceate query of database
qry = session.query(city_limits,functions.ST_AsGeoJSON(city_limits.geom))
#qry = session.query(city_limits1,functions.ST_AsGeoJSON(func.ST_SetSRID(city_limits1.geom,4326)))

print(qry[0][0].name)
print(qry[1][1])
#Create geojson file
f = open(r"city_limits.geojson", 'w')

#Enforce right hand rule
corrected = rewind(qry[0][1])

f.write(f'{{"type": "Feature","geometry":{corrected},"properties": {{"name": "{qry[0][0].name}"}}}},')

#for row in qry:
    #print(f'{{"type": "Feature","geometry":{row[1]},"properties": {{"name": {row[0].name}}}}}')
    #f.write(f'{{"type": "Feature","geometry":{row[1]},"properties": {{"name": {row[0].name}}}}},')


#Close file
f.close()

#Main web page
@app.route('/')
def index():


    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
