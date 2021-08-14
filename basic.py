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
from sqlalchemy import text

#Create flask python app
app = Flask(__name__)

#Create variable for development mode
dev = False

#If deveopement mode is true use local host database, else use production database
if dev:
    #Create database create create_engine
    password = "kmr504rmz36"
    engine = create_engine('postgresql://postgres:kmr504rmz36@localhost/StormSurge', echo=True)
    print(engine)
else:
    #Create database create create_engine
    engine = create_engine('postgresql://gismapgi:23IHij9p2x@gismap22.gis-cdn.net/gismapgi_stormsurge', echo=True)
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

#Create class for Category table
class category_2(Base):
    __tablename__ = 'category_2'
    gid = Column(Integer, primary_key=True)
    objectid = Column(Numeric)
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('POLYGON', 4326))

#Create class for Category table
class category_3(Base):
    __tablename__ = 'category_3'
    gid = Column(Integer, primary_key=True)
    objectid = Column(Numeric)
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('POLYGON', 4326))

#Create class for Category table
class category_4(Base):
    __tablename__ = 'category_4'
    gid = Column(Integer, primary_key=True)
    objectid = Column(Numeric)
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('POLYGON', 4326))

#Create class for Category table
class category_5(Base):
    __tablename__ = 'category_5'
    gid = Column(Integer, primary_key=True)
    objectid = Column(Numeric)
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    geom = Column(Geometry('POLYGON', 4326))

#Create class for buildings table
class buildings(Base):
    __tablename__ = 'buildings'
    gid = Column(Integer, primary_key=True)
    shape_leng = Column(Numeric)
    shape_area = Column(Numeric)
    city = Column(String)
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

def build_Category(session,category):
    #Ceate query of database
    conn = engine.connect()

    print(category)
    if category == "category_1":
        #qry = session.query(category_1,functions.ST_AsGeoJSON(category_1.geom))
        qry = text("""SELECT ST_AsGeoJSON(category_1.geom) AS "ST_GeoJSON_1" FROM category_1""")
    elif category == "category_2":
        #qry = session.query(category_2,functions.ST_AsGeoJSON(category_2.geom))
        qry = text("""SELECT ST_AsGeoJSON(category_2.geom) AS "ST_GeoJSON_1" FROM category_2""")
    elif category == "category_3":
        #qry = session.query(category_3,functions.ST_AsGeoJSON(category_3.geom))
        qry = text("""SELECT ST_AsGeoJSON(category_3.geom) AS "ST_GeoJSON_1" FROM category_3""")
    elif category == "category_4":
        #qry = session.query(category_4,functions.ST_AsGeoJSON(category_4.geom))
        qry = text("""SELECT ST_AsGeoJSON(category_4.geom) AS "ST_GeoJSON_1" FROM category_4""")
    elif category == "category_5":
        #qry = session.query(category_5,functions.ST_AsGeoJSON(category_5.geom))
        qry = text("""SELECT ST_AsGeoJSON(category_5.geom) AS "ST_GeoJSON_1" FROM category_5""")

    result = conn.execute(qry)

    #Create geojson file
    f = open(r"static/category.geojson", 'w')
    #Write first line
    f.write(f'{{"type":"FeatureCollection","features":[')
    for row in result:
        #Enforce right hand rule
        corrected = rewind(row[0])
        #Check to see if the row is the last element if so remove ending comma for geojson file

        #Write out rows to create geojson file with comma
        f.write(f'{{"type": "Feature","geometry":{corrected}}},')
    if 'corrected' in locals():
        #Write out last list feature without ending comma
        f.write(f'{{"type": "Feature","geometry":{corrected}}}')

    #Write last line
    f.write(f']}}')
    #Close file
    f.close()

def build_City(session,city_name):

    conn = engine.connect()
    #Ceate query of database to only get the city that was selected
    #qry = session.query(city_limits,functions.ST_AsGeoJSON(city_limits.geom)).filter_by(name=f'{city_name}')
    qry = text("""SELECT name, ST_AsGeoJSON(city_limits.geom) AS "ST_AsGeoJSON_1" FROM city_limits WHERE name= :c """)
    result = conn.execute(qry, c=city_name)
    #qry = session.query(city_limits,functions.ST_AsGeoJSON(city_limits.geom)).filter_by(name='Bayou La Batre')
    print(result)
    #Create geojson file
    f = open(r"static/city.geojson", 'w')
    #Write first line
    f.write(f'{{"type":"FeatureCollection","features":[')

    for row in result:
        print(row[0])
        #print(f'{{"type": "Feature","geometry":{row[1]},"properties": {{"name": {row[0].name}}}}}')
        #Enforce right hand rule
        corrected = rewind(row[1])

        #Write out rows to create geojson file with comma
        f.write(f'{{"type": "Feature","geometry":{corrected},"properties": {{"name": "{row[0]}"}}}},')
    if 'corrected' in locals():
        #Write out last list feature without ending comma
        f.write(f'{{"type": "Feature","geometry":{corrected},"properties": {{"name": "{row[0]}"}}}}')


    #Write last line
    f.write(f']}}')
    #Close file
    f.close()

def build_buildings(session,city_name):
    #Create query to get all of the building footprints in the selected city
    #Create spatial query
    conn = engine.connect()
    #qry = text("""SELECT city, ST_AsGeoJSON(buildings.geom) AS "ST_AsGeoJSON_1" FROM buildings WHERE city='Bucks'""")
    qry = text("""SELECT city, ST_AsGeoJSON(buildings.geom) AS "ST_AsGeoJSON_1" FROM buildings WHERE city= :c """)
    result = conn.execute(qry, c=city_name)

    #Create geojson file
    f = open(r"static/buildings.geojson", 'w')
    #Write first line
    f.write(f'{{"type":"FeatureCollection","features":[')

    for row in result:
        #Enforce right hand rule
        corrected = rewind(row[1])

        #Write out rows to create geojson file with comma
        f.write(f'{{"type": "Feature","geometry":{corrected},"properties": {{"name": "{row[0]}"}}}},')
    if 'corrected' in locals():
        #Write out last list feature without ending comma
        f.write(f'{{"type": "Feature","geometry":{corrected},"properties": {{"name": "{row[0]}"}}}}')

    #Write last line
    f.write(f']}}')
    #Close file
    f.close()

def build_damage(session,category,city_name):
    #Connect to database
    conn = engine.connect()

    #Get data text data for city
    #city_qry = text("""SELECT ST_AsEWKT(city_limits.geom) AS "ST_Text_1" FROM city_limits WHERE name= :c """)
    #city_result = conn.execute(city_qry, c=city_name)

    #Put geom data into variable
    #for row in city_result:
        #city_coords = row

    #Use if statement to get the correct category query
    if category == "category_1":
        qry = text("""SELECT ST_AsGeoJSON(buildings.geom) AS "ST_GeoJSON_1" FROM buildings,category_1 WHERE buildings.city =:c AND ST_Within(buildings.geom,category_1.geom)""")
    elif category == "category_2":
        qry = text("""SELECT ST_AsGeoJSON(buildings.geom) AS "ST_GeoJSON_1" FROM buildings,category_2 WHERE buildings.city =:c AND ST_Within(buildings.geom,category_2.geom)""")
    elif category == "category_3":
        qry = text("""SELECT ST_AsGeoJSON(buildings.geom) AS "ST_GeoJSON_1" FROM buildings,category_3 WHERE buildings.city =:c AND ST_Within(buildings.geom,category_3.geom)""")
    elif category == "category_4":
        qry = text("""SELECT ST_AsGeoJSON(buildings.geom) AS "ST_GeoJSON_1" FROM buildings,category_4 WHERE buildings.city =:c AND ST_Within(buildings.geom,category_4.geom)""")
    elif category == "category_5":
        qry = text("""SELECT ST_AsGeoJSON(buildings.geom) AS "ST_GeoJSON_1" FROM buildings,category_5 WHERE buildings.city =:c AND ST_Within(buildings.geom,category_5.geom)""")


    #Execute querey
    result = conn.execute(qry,c=city_name)

    #Create spatial query; get buildings that are intersect both city and category
    #qry = text("""SELECT ST_AsGeoJSON(buildings.geom) AS "ST_GeoJSON_1" FROM buildings,category_1 WHERE buildings.city =:c AND ST_Within(buildings.geom,category_1.geom)""")
    #result = conn.execute(qry,c=city_name)

    #Put geom data into variable
    for row in result:
        #Create geojson file
        f = open(r"static/damage.geojson", 'w')
        #Write first line
        f.write(f'{{"type":"FeatureCollection","features":[')

        for row in result:
            #Enforce right hand rule
            corrected = rewind(row[0])

            #Write out rows to create geojson file with comma
            f.write(f'{{"type": "Feature","geometry":{corrected}}},')
        if 'corrected' in locals():
            #Write out last list feature without ending comma
            f.write(f'{{"type": "Feature","geometry":{corrected}}}')

        #Write last line
        f.write(f']}}')
        #Close file
        f.close()

def build_counts(session,category,city_name):
    #Create connection to database
    conn = engine.connect()

    #Create query to get total building count from selected city
    #building_qry = text("""SELECT count(gid) FROM buildings WHERE city =:c""")

    #Create query to get storm surge impacted buildings from selected city
    #Use if statement to get the correct category query
    if category == "category_1":
        damage_building_qry = text("""SELECT COUNT(buildings.gid) FROM buildings,category_1 WHERE buildings.city =:c AND ST_Within(buildings.geom,category_1.geom)""")
    elif category == "category_2":
        damage_building_qry  = text("""SELECT COUNT(buildings.gid) FROM buildings,category_2 WHERE buildings.city =:c AND ST_Within(buildings.geom,category_2.geom)""")
    elif category == "category_3":
        damage_building_qry  = text("""SELECT COUNT(buildings.gid)FROM buildings,category_3 WHERE buildings.city =:c AND ST_Within(buildings.geom,category_3.geom)""")
    elif category == "category_4":
        damage_building_qry  = text("""SELECT COUNT(buildings.gid) FROM buildings,category_4 WHERE buildings.city =:c AND ST_Within(buildings.geom,category_4.geom)""")
    elif category == "category_5":
        damage_building_qry  = text("""SELECT COUNT(buildings.gid) FROM buildings,category_5 WHERE buildings.city =:c AND ST_Within(buildings.geom,category_5.geom)""")

    #Create query to get total population of selected city
    count_qry = text("""SELECT city_limits.pop2012,city_limits.buildings,city_limits.roads FROM city_limits WHERE name =:c """)

    #Create query to get total population impacted by storm surge
    #Use if statement to get the correct category query
    if category == "category_1":
        damage_population_qry = text("""SELECT SUM(population.pop2010) FROM population,category_1 WHERE population.city =:c AND ST_Within(population.geom,category_1.geom)""")
    elif category == "category_2":
        damage_population_qry  = text("""SELECT SUM(population.pop2010) FROM population,category_2 WHERE population.city =:c AND ST_Within(population.geom,category_2.geom)""")
    elif category == "category_3":
        damage_population_qry  = text("""SELECT SUM(population.pop2010) FROM population,category_3 WHERE population.city =:c AND ST_Within(population.geom,category_3.geom)""")
    elif category == "category_4":
        damage_population_qry  = text("""SELECT SUM(population.pop2010) FROM population,category_4 WHERE population.city =:c AND ST_Within(population.geom,category_4.geom)""")
    elif category == "category_5":
        damage_population_qry  = text("""SELECT SUM(population.pop2010) FROM population,category_5 WHERE population.city =:c AND ST_Within(population.geom,category_5.geom)""")

    #Create query to get total mileage of roads impacted by storm surge
    #Use if statement to get the correct category query
    if category == "category_1":
        damage_roads_qry = text("""SELECT COUNT(roads2.gid) FROM roads2,category_1 WHERE roads2.city =:c AND ST_Within(roads2.geom,category_1.geom)""")
    elif category == "category_2":
        damage_roads_qry  = text("""SELECT COUNT(roads2.gid) FROM roads2,category_2 WHERE roads2.city =:c AND ST_Within(roads2.geom,category_2.geom)""")
    elif category == "category_3":
        damage_roads_qry  = text("""SELECT COUNT(roads2.gid) FROM roads2,category_3 WHERE roads2.city =:c AND ST_Within(roads2.geom,category_3.geom)""")
    elif category == "category_4":
        damage_roads_qry  = text("""SELECT COUNT(roads2.gid) FROM roads2,category_4 WHERE roads2.city =:c AND ST_Within(roads2.geom,category_4.geom)""")
    elif category == "category_5":
        damage_roads_qry  = text("""SELECT COUNT(roads2.gid) FROM roads2,category_5 WHERE roads2.city =:c AND ST_Within(roads2.geom,category_5.geom)""")

    #Create query to get total miles of roads in selected city
    #roads_qry = text("""SELECT COUNT(roads2.gid) FROM roads2 WHERE city =:c """)

    #Execute query
    counts = conn.execute(count_qry,c=city_name)
    damage_building_count = conn.execute(damage_building_qry,c=city_name)
    #population_count = conn.execute(population_qry,c=city_name)
    damage_population_count = conn.execute(damage_population_qry,c=city_name)
    #roads_count = conn.execute(roads_qry,c=city_name)
    damage_roads_count = conn.execute(damage_roads_qry,c=city_name)

    #Save counts to variables
    #for row in building_count:
        #building_total = row[0]

    for row in damage_building_count:
        damage_building_total = row[0]
        if damage_building_total == None:
            damage_building_total = 0
        else:
            damage_building_total = int(damage_building_total)

    #for row in population_count:
        #population_total = int(row[0])

    for row in damage_population_count:
        damage_population_total = row[0]
        if damage_population_total == None:
            damage_population_total = 0
        else:
            damage_population_total = int(damage_population_total)

    #for row in roads_count:
        #roads_total = row[0]
        #if roads_total == None:
            #roads_total = 0
        #else:
             #roads_total = int(roads_total)

    for row in counts:
        population_total = row[0]
        building_total = row[1]
        roads_total = row[2]
        if roads_total == None:
            roads_total = 0
        else:
            roads_total = int(roads_total)
        if population_total == None:
            population_total = 0
        else:
            population_total = int(population_total)
        if roads_total == None:
            roads_total = 0
        else:
            roads_total = int(roads_total)

    for row in damage_roads_count:
        damage_roads_total = row[0]
        if damage_roads_total == None:
            damage_roads_total = 0
        else:
             damage_roads_total = int(damage_roads_total)

    return building_total,damage_building_total,population_total,damage_population_total,roads_total,damage_roads_total

#Main web page
@app.route('/')
def index():
    #build_cityLimits(session)

    return render_template("index.html")

#Page after user has submitted city and Category
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        #Save form data into variables
        city_name = request.form['city']
        category = request.form['category']
        #Call function to query data for category, city and buildings
        build_Category(session,category)
        build_City(session,city_name)
        #build_buildings(session,city_name)
        build_damage(session,category,city_name)
        #building_total,damage_building_total,population_total,damage_population_total,roads_total,damage_roads_total
        building_total,damage_building_total,population_total,damage_population_total,roads_total,damage_roads_total = build_counts(session,category,city_name)

        #Return category name to send to submit html page
        if category == "category_1":
            cat = 'Category 1'
        elif category == "category_2":
            cat = 'Category 2'
        elif category == "category_3":
            cat = 'Category 3'
        elif category == "category_4":
            cat = 'Category 4'
        elif category == "category_5":
            cat = 'Category 5'

    return render_template("submit.html", damage_pop = damage_population_total, damage_buildings = damage_building_total, damage_roads = damage_roads_total, pop = population_total , building = building_total, road = roads_total, city = city_name, cat = cat)

#Page with information about the application
@app.route('/about', methods=['POST'])
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)
