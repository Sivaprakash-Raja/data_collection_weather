import paho.mqtt.client as mqttClient
import json
import time

class Mqtt:

	def __init__(self):
		self.json_data = {}
		mqttclient = mqttClient.Client("5664")
		mqttclient.on_connect = self.on_connect
		mqttclient.on_message = self.on_message
		mqttstatus = mqttclient.connect("broker.emqx.io", 1883,60)
		mqttclient.loop_forever()

	def on_connect(self,mqttclient, userdata, flags,rc):
		if rc == 0:
			mqttclient.subscribe("/test/weather")
		else:
			print("Connection failed")
        
	def on_message(self,mqttclient, userdata, msg):
	
		mqtt_msg = str(msg.payload).replace("\n", "").replace("b'", "").replace("'", "")
		json_data = json.loads(mqtt_msg)

		wdata = {"mtime": json_data["Timestamp"][11:],"mtemp":json_data["data"]["Temperature"],"mhumidity":json_data["data"]["Humidity"],"mwindspeed":json_data["data"]["Wind_speed"],"solar_irradiation":json_data["data"]["Solar_Irradiation"]}

		print(wdata)

		with open("config.json", "r") as jsonFile:
			data = json.load(jsonFile)

		data = wdata
	
		with open("config.json", "w") as jsonFile:
			json.dump(data, jsonFile)



Mqtt()

