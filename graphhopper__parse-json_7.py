import requests
import urllib.parse

def geocoding(location, key):
    while location == "":
        location = input("Enter the location again: ")

    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        new_loc = f"{name}, {state}, {country}" if state else f"{name}, {country}"
        print(f"Geocoding API URL for {new_loc} (Location Type: {value})\n{url}")
    else:
        lat, lng, new_loc = "null", "null", location
        if json_status != 200:
            print(f"Geocode API status: {json_status}\nError message: {json_data.get('message', 'No message')}")
    return json_status, lat, lng, new_loc

def routing(orig, dest, vehicle, key):
    route_url = "https://graphhopper.com/api/1/route?"
    op = f"&point={orig[1]}%2C{orig[2]}"
    dp = f"&point={dest[1]}%2C{dest[2]}"
    paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
    paths_status = requests.get(paths_url).status_code
    paths_data = requests.get(paths_url).json()

    if paths_status == 200:
        print(f"Routing API Status: {paths_status}\nRouting API URL:\n{paths_url}")
        print(f"Directions from {orig[3]} to {dest[3]} by {vehicle}")
        distance = paths_data["paths"][0]["distance"]
        time = paths_data["paths"][0]["time"]
        miles, km = distance / 1000 / 1.61, distance / 1000
        sec, min, hr = int(time / 1000 % 60), int(time / 1000 / 60 % 60), int(time / 1000 / 60 / 60)
        print(f"Distance Traveled: {miles:.1f} miles / {km:.1f} km")
        print(f"Trip Duration: {hr:02d}:{min:02d}:{sec:02d}")
        print("Instructions:")
        for instruction in paths_data["paths"][0]["instructions"]:
            path = instruction["text"]
            distance = instruction["distance"]
            print(f"{path} ({distance / 1000:.1f} km / {distance / 1000 / 1.61:.1f} miles)")
    else:
        print(f"Routing API Status: {paths_status}\nError message: {paths_data.get('message', 'No message')}")

def main():
    key = "8e924744-c1e0-4109-ab99-2819ee98a55c"  # Replace with your actual API key
    while True:
        print("\n+++++++++++++++++++++++++++++++++++++++++++++")
        print("Vehicle profiles available on Graphhopper:")
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        print("car, bike, foot")
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        profile = ["car", "bike", "foot"]
        vehicle = input("Enter a vehicle profile from the list above: ")
        if vehicle in ["quit", "q"]:
            break
        if vehicle not in profile:
            vehicle = "car"
            print("No valid vehicle profile was entered. Using the car profile.")

        loc1 = input("Starting Location: ")
        if loc1 in ["quit", "q"]:
            break
        orig = geocoding(loc1, key)

        loc2 = input("Destination: ")
        if loc2 in ["quit", "q"]:
            break
        dest = geocoding(loc2, key)

        if orig[0] == 200 and dest[0] == 200:
            routing(orig, dest, vehicle, key)
        else:
            print("Unable to process routing due to geocoding errors.")

if __name__ == "__main__":
    main()
