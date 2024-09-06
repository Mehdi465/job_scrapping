import folium
from geopy.geocoders import Nominatim
import requests
import pandas
import branca

def get_city_coordinates_from_name(city_name:str):
    location=None
    geolocator = Nominatim(user_agent="geoapiExecises")
    location = geolocator.geocode(city_name)

    if location:
        print(f"City: {location.address}")
        print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
        return (location.latitude,location.longitude)
    else:
        print("City not found")
        return None

print(get_city_coordinates_from_name("Toronto"))


### ----------------- MARKERS ---------------- ###
#1 variable popup cannot be in two different markups
m = folium.Map(location=(45.3311, -121.7113),tiles="CartoDB Voyager")

MARKERS = True
if MARKERS :
    folium.Marker(
        location=[45.3288, -121.6625],
        tooltip="Click me!",
        popup="Mt. Hood Meadows",
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)

    html = """
       <h1> This popup is an Iframe</h1><br>
       With a few lines of code...
       <p>
       <code>
           from numpy import *<br>
           exp(-2*pi)
       </code>
       </p>
       """

    iframe = branca.element.IFrame(html=html, width=500, height=300)
    popup1 = folium.Popup(iframe, max_width=500)

    folium.Marker([30, -100], popup=folium.Popup(iframe, max_width=500)).add_to(m)

    folium.Marker(
        location=[45.3311, -121.7113],
        tooltip="Click me!",
        popup=popup1,
        icon=folium.Icon(color="pink"),
    ).add_to(m)

    

### ----------------- Vectors ---------------- ###

VECTORS = True

if VECTORS:

    #m = folium.Map(location=[-71.38, -73.9], zoom_start=11)

    trail_coordinates = [
        (-71.351871840295871, -73.655963711222626),
        (-71.374144382613707, -73.719861619751498),
        (-71.391042575973145, -73.784922248007007),
        (-71.400964450973134, -73.851042243124397),
        (-71.402411391077322, -74.050048183880477),
    ]

    folium.PolyLine(trail_coordinates, tooltip="Coast").add_to(m)

### ------------ Group/LAyerControl ------------- ###
GROUP = True

if GROUP:
    group_1 = folium.FeatureGroup("first group").add_to(m)
    folium.Marker((0, 0), icon=folium.Icon("red")).add_to(group_1)
    folium.Marker((1, 0), icon=folium.Icon("red")).add_to(group_1)

    group_2 = folium.FeatureGroup("second group").add_to(m)
    folium.Marker((0, 1), icon=folium.Icon("green")).add_to(group_2)

    folium.LayerControl().add_to(m)


m.save("results/index.html")