import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GOOGLE_MAPS_API_KEY")

gmaps = googlemaps.Client(key=api_key)


print(dir(gmaps))

def get_lat_lng(address):
    """
    Returns the latitude and longitude coordinates for a given address.
    """
    