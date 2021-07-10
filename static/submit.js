//Title: Coastal Alabama Storm Surge Impact
//Author: Kyle Roebling
//Date: 6/17/2021

//Global variables
var category = new L.LayerGroup();
var city = new L.FeatureGroup();

//Style variables
var city_style ={
  color: '#FCB900',
  fill: false
}

var category_style ={
  color: '#0079F2',
  stroke: false
}

//Create leaflet map variable
var mymap = L.map('mapid').setView([30.695366, -88.039894], 9);
mymap.invalidateSize();

//Add Basemap
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/light-v10',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1Ijoia3JvZWJsaW5nIiwiYSI6ImNqeXczaGplMjB3YjgzYmxyZGU1OG90bXUifQ.ItIrq8YGHvZIilkcx-U8Ag'
}).addTo(mymap);

//Make ajax call to get geojson file for category
function category_data(mymap){
  category.clearLayers()
  //To get around geojson cache I used a timestamp to make each request unique
  $.getJSON("static/category.geojson",{_: new Date().getTime()} ,function(data){
    category_layer = L.geoJson(data,{
            onEachFeature: function (feature, layer) {
                //layer.bindPopup('<p>' + feature.properties.name '</p>'));
                layer.setStyle(category_style);

            },
        })
        category.addLayer(category_layer);
        category.addTo(mymap);
      });
};

//Make ajax call to get geojson file for city
function city_data(mymap){
  //To get around geojson cache I used a timestamp to make each request unique
  $.getJSON("static/city.geojson",{_: new Date().getTime()} ,function(data){
    city_layer = L.geoJson(data,{
            onEachFeature: function (feature, layer) {
                //layer.bindPopup('<p>' + feature.properties.name '</p>'));
                layer.setStyle(city_style);
            },
        })
        city.addLayer(city_layer);
        city.addTo(mymap);
        mymap.fitBounds(city.getBounds())
      });
};

//Add category geojson to map
category_data(mymap)
//Add city geojson to mapid
city_data(mymap)
