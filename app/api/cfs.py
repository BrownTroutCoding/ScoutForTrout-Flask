import requests
from datetime import datetime

def get_and_groom_cfs(river_name):
    print("Now grabbing data from river: %s" % river_name)
    print("---------------------------------------")

    # Define paths
    mainPath = "C:/Users/theco/Documents/CodingTemple/CapstoneProject/fly_fishing_flask_app/app/api/USGS"
    dataDir = "%s/data" %(mainPath)

    # Define river-to-stationID mapping
    river_to_stationID = {
        "gallatin"   : "06043500",
        "madison"    : "06041000",
        "jefferson"  : "06036650",
        "yellowstone": "06192500",
        "shields"    : "06195600",
        "missouri"   : "06054500"
    }

    # Get the station ID for the given river name
    stationID = river_to_stationID.get(river_name.lower())

    # Check if the given river name is valid
    if not stationID:
        print("Invalid river name: %s" % river_name)
        return

    # Build URL for the corresponding river
    url = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites=%s&siteStatus=all&parameterCd=00060" % stationID
    print("Building URL for %s river: %s" % (river_name.capitalize(), url))

    # Make the request
    response = requests.get(url)
    if response.status_code == 200:
        print("Request successful!")
    else:
        print("Request failed with status code %d" % response.status_code)
        return

    # Groom the data to find only the DATETIME and CFS values
    # Used JSON viewer to look through the API and find these two values
    data = response.json()
    print(f"River: " + river_name.capitalize())
    CFSDateTime = data["value"]["timeSeries"][0]["values"][0]["value"][0]["dateTime"]
    CFSDateTime = datetime.strptime(CFSDateTime, "%Y-%m-%dT%H:%M:%S.%f-06:00").strftime("%m/%d/%Y %I:%M %p")
    print(f"Date and Time: " + CFSDateTime)
    CFSValue = data["value"]["timeSeries"][0]["values"][0]["value"][0]["value"]
    print(f"CFS: " + CFSValue)

    return {
        "river": river_name.capitalize(),
        "date_and_time": CFSDateTime,
        "cfs": CFSValue,
    }

# get_and_groom_cfs("gallatin")
