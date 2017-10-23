from urllib.request import urlopen
import json
import pyowm


_id = '4116834'  # id for Eskisehir
key = '71ae36fed5d93780c2ef3969dbbe69f6'   # api key
url = 'http://api.openweathermap.org/data/2.5/weather?id=' + _id + '&APPID=' + key   # full url

owm = pyowm.OWM(key)


# Search for current weather in London (UK)
observation = owm.weather_at_place('Jonesboro, ar')
w = observation.get_weather()

wind = w.get_wind()                  # {'speed': 4.6, 'deg': 330}
humidity = w.get_humidity()              # 87
temperature = w.get_temperature('fahrenheit')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
pressure = w.get_pressure()
status = w.get_status()
details = w.get_detailed_status()

print(details)
print('Temperataure = {} F'.format(temperature["temp"]))
print('Humidity = {} %'.format(humidity))
print('Pressure = {} hPa'.format(pressure["press"]))
print('Wind Speed = {} m/s'.format(wind["speed"]))

fc = owm.three_hours_forecast('Jonesboro, ar')
f = fc.get_forecast()
lst = f.get_weathers()
time = "2017-09-30 12:00:00+00"

rain = fc.will_be_rainy_at(time)
clouds = fc.will_be_cloudy_at(time)

#cloudy = fc.when_clouds()

print(rain, clouds)

#print (cloudy)
