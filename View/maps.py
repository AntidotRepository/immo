# import gmplot package
import gmplot
import os

# https://pypi.org/project/geopy/
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="lol")
location = geolocator.geocode(12059)

gmap4 = gmplot.GoogleMapPlotter(location.latitude, location.longitude, 13)

# heatmap plot heating Type
# points on the Google map
gmap4.heatmap([location.latitude], [location.longitude])

# Pass the absolute path
gmap4.draw(os.getcwd() + "/maps.html")
