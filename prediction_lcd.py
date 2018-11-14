import requests
import json
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd

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
    lcd.clear()

    lcd_rs = digitalio.DigitalInOut(board.D26)
    lcd_en = digitalio.DigitalInOut(board.D19)
    lcd_d7 = digitalio.DigitalInOut(board.D27)
    lcd_d6 = digitalio.DigitalInOut(board.D22)
    lcd_d5 = digitalio.DigitalInOut(board.D24)
    lcd_d4 = digitalio.DigitalInOut(board.D25)

    lcd_columns = 16
    lcd_rows = 2

    lcd = adafruit_character_lcd.Character_LCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

    # Stop ID for Packard & Arch = 1720
    # Route = 5 (Packard) towards Blake Transit Center
    next_time = get_next_predicted_time(1720, 5)
    seconds_until = calculate_seconds_until(next_time)

    print(seconds_until / 60)
    lcd.message(str(seconds_until / 60))

if __name__ == "__main__":
    main()
