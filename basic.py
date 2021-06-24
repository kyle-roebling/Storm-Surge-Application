#Import python libaries
from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
import psycopg2

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
    geom = Column(Geometry('POLYGON'))

#Create DB sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

#Create connection
conn = engine.connect()

#Ceate select object
s = select([city_limits])
print(s)

result = conn.execute(s)
for row in result:
    print(row['name'])

#Create Query for database
#query = session.query(city_limits).all()
#print(query)
#for city in query:
    #print(city.name)

#Main web page
@app.route('/')
def index():


    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
