import requests
import json
from datetime import datetime

def get_next_predicted_time(stop_id, route):
    base_url = "http://rt.theride.org/bustime/api/v3/getpredictions?key=PAvcL9aJb9U8WMrzmCesKyw9C&format=json&rtpidatafeed=bustime"
    query = f"{base_url}&stpid={stop_id}&rt={route}"
    r = requests.get(query)
    res = r.json()

    # JSON returned shows a list of objects of the next few arriving busses
    # We'll look at just the first result
    next_time = res['bustime-response']['prd'][0]['prdtm']

    return next_time

# this function takes in the time string that is outputted from the API,
# converts it to a datetime object and uses that to calculate the seconds
# from now until that time
def calculate_seconds_until(time_string):
    next_time_dt = datetime.strptime(time_string, '%Y%m%d %H:%M')
    td = next_time_dt - datetime.now()
    return td.seconds

def main():
    # Stop ID for Packard & Arch = 1720
    # Route = 5 (Packard) towards Blake Transit Center
    next_time = get_next_predicted_time(1720, 5)
    seconds_until = calculate_seconds_until(next_time)

    print(seconds_until / 60)

if __name__ == "__main__":
    main()
