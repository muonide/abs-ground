from flask import Flask, flash, redirect, render_template, request
from random import randint
from pymongo import MongoClient

 
client = MongoClient('mongodb://arballoonsat:WHwQTbUiI^z2qsX@ds135234.mlab.com:35234/abstrack')
db = client['abstrack']

locallon = 'Longitude = 35.12345'
locallat = 'Latitude = -90.213'
localalt = 'Altitude = 123 m'
targetbear = 'Target Bearing = 90'
targetelev = 'Target Elevation = 30'
currentbear = 'Current Bearing = 83.1'
currentelev = 'Current Elevation = 27.2'
los = ' Line of sight = 25 km'

temperature = 'Temperature = 23 C'
pressure = 'Pressure = 1 atm'
humidity = 'Humidity = Arkansas'
accel = 'Accel: 0'
mag = 'Mag = 0'
gyro = 'Gyro = 0'

app = Flask(__name__)



 
@app.route("/")
def index():
 
	telemetry = db.telemetry.find_one()
	longitude = telemetry['longitude']
	latitude = telemetry['latitude']
	altitude = telemetry['altitude']
	longString = 'Longitude = {}'.format(longitude) 
	latString = 'Latitude = {}'.format(latitude) 
	altString = 'Altitude = {} m'.format(altitude) 

	balloondata = [longString, latString, altString]
	localdata = [locallon, locallat, localalt]
	servodata = [currentbear, currentelev, targetbear, targetelev, los]
	weatherdata = [temperature, pressure, humidity]
	calibrationdata = [accel, mag, gyro]

	return render_template(
        'index.html', **locals())
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
