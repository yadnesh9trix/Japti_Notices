import os
import time
# import module
import pandas as pd
from datetime import datetime,timedelta
import warnings
warnings.filterwarnings('ignore')
import os
from math import radians, sin, cos, sqrt, atan2
from geopy.geocoders import Nominatim



# Function to calculate distance using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    ## ΔlatDifference = lat1 – lat2(differenceoflatitude)
    ## ΔlonDifference = lon1 – lon2 (difference of longitude)
    d_lat = lat2_rad - lat1_rad
    d_lon = lon2_rad - lon1_rad
    ## a = sin²(ΔlatDifference / 2) + cos(lat1).cos(lt2).sin²(ΔlonDifference / 2)
    ## c = 2.atan2(√a, √(1−a))
    a = sin(d_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    earth_radius_km = 6371.0   # Earth's radius in kilometers
    distance = earth_radius_km * c  ## d is the distance computed between two points.

    return distance


# Function to get current latitude and longitude
def get_current_location():
    geolocator = Nominatim(user_agent="property_sorting")
    location = geolocator.geocode("Pimpri-Chinchwad")
    return location.latitude, location.longitude