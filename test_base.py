from datetime import datetime

import requests

record_url = "http://127.0.0.1:5000/add_record"
last_time = datetime.now()
vehicle_registration = "KBU234Y"
display_url = "http://192.168.0.103"
vehicle_speed = {
    "speed": 0
}
c = 10
speed_request = requests.get(url=display_url + "/?people=" + str(c - 1))
vehicle_speed["speed"] = speed_request.text
print(speed_request.text)
data = {
    "speed": vehicle_speed["speed"],
    "number_of_people": c - 1,
    "registration": vehicle_registration

}
send_data = requests.post(url=record_url, json=data)
print(send_data.text)
