from pymongo import MongoClient


client = MongoClient('mongodb://arballoonsat:WHwQTbUiI^z2qsX@ds135234.mlab.com:35234/abstrack')
db = client['abstrack']


class GetIridium():

    def getApiData(self, imei):
        
        try:
            telemetry = db.telemetry.find_one()
            balloon = hashlib.sha1(telemetry['imei']) #hash imei for balloon identifier
            time = telemetry['time']
            lon = telemetry['longitude']
            lat = telemetry['latitude']
            alt = telemetry['altitude']
        except:
            return {}

        self.iridiumInterrupt = False

    def interrupt(self):
        self.iridiumInterrupt = True


