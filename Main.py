import json
import csv
import time
from openWeather import weather
import datetime
from csv import DictWriter
from os.path import exists
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



def sendmail(file,filename):

    fromaddr = "weathermonitortce@gmail.com"
    password ="weathermonitortce2021"
    toaddr = "svquants@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "solar_power_prediction_datasheet"
    body = "Report"
    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(file,"rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password=password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

    return True



field_names = ['fdate', 'ftime', 'ftemp', 'fdew_point', 'fpressure', 'fhumidity', 'fuv_index', 'fclouds_percentage', 'fvisibility', 'fwind_speed', 'fwind_deg', 'fweather', 'fdescription', 'time', 'temp', 'dew_point', 'pressure', 'humidity', 'uv_index', 'clouds_percentage', 'visibility', 'wind_speed', 'wind_deg', 'weather', 'description', 'mtime', 'mtemp', 'mhumidity', 'mwindspeed', 'solar_irradiation']

obj = weather("madurai")


while(1):
	print("True")

	current_time = str(datetime.datetime.now())

	if(int(current_time[11:13])>=6 and int(current_time[11:13])<=19):
		if(current_time[14:16]=="00" or current_time[14:16]=="15" or current_time[14:16]=="30" or current_time[14:16]=="45"):

			current_data = obj.get_current_weather()
			forecast_data = obj.get_forecast_weather(1)

			with open("config.json",'r') as js:
				actual_data = json.load(js)

				data = {'mtime': 0, 'mtemp': 0, 'mhumidity': 0, 'mwindspeed': 0, 'solar_irradiation': 0}

			with open("config.json", "w") as jsonFile:
				json.dump(data, jsonFile)

			json_data = { **forecast_data, **current_data, **actual_data }
			print(json_data)

			
			if(exists('datasheet.csv')):
				with open('datasheet.csv', 'a') as f_object:
					dictwriter_object = DictWriter(f_object, fieldnames=field_names)
					dictwriter_object.writerow(json_data)
					f_object.close()
			else:
				with open('datasheet.csv', 'w') as f_object:
					dictwriter_object = DictWriter(f_object, fieldnames=field_names)
					dictwriter_object.writeheader()
					dictwriter_object.writerow(json_data)
					f_object.close()
			

			time.sleep(60)


	if(int(current_time[11:13])==20 and int(current_time[14:16])==0):
		var = sendmail("datasheet.csv","datasheet.csv")
		if(var):
			print(var)
			print("mail sent")
			os.remove('datasheet.csv')

		time.sleep(200)

