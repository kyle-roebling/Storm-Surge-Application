//Title: Coastal Alabama Storm Surge Impact
//Author: Kyle Roebling
//Date: 6/17/2021

//Global variables
var city_limits = new L.LayerGroup();

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

//Make ajax call to get geojson file
function city_limits_data(mymap){

  $.getJSON("static/city_limits.geojson", function(data){
    city_limits_layer = L.geoJson(data,{
            onEachFeature: function (feature, layer) {
                //layer.bindPopup('<p>' + feature.properties.name '</p>'));
            },
        })
        city_limits.addLayer(city_limits_layer);
        city_limits.addTo(mymap);
      });
};

city_limits_data(mymap)
