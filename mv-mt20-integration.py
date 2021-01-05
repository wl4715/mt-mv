import json
import requests
import webbrowser
from time import sleep

from env_user import api_key, dashboard_url, network_id, mv_serial, mt_serial

headers = {
	'X-Cisco-Meraki-API-Key' : api_key
}

def get_door_latest_reading():
	payload = {
		'metric' : "door"
	}

	response = requests.get(
			dashboard_url + '/networks/' + network_id + '/sensors/stats/latestBySensor',
			headers = headers,
			params = payload
		).json()

	ts = response[0]["ts"]
	door_opened = response[0]["value"] 

	return ts, door_opened



def post_mv_snapshot(ts):
	body = {
		'timestamp' : ts,
		'fullframe' : False
	}

	response = requests.post(
			dashboard_url + '/devices/' + mv_serial + '/camera/generateSnapshot',
			headers = headers,
			data = body
		)
	
	snapshot = json.loads(response.text)["url"]

	return snapshot

while(True):
	door_opened = get_door_latest_reading()[1]
	print(door_opened)

	if door_opened == 1.0:
		snapshot_url = post_mv_snapshot(get_door_latest_reading()[0])
		print(snapshot_url)
		webbrowser.open(snapshot_url, new = 2)

	sleep(20)


