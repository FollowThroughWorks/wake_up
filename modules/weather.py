import pywapi # For retrieving weather info
from utilities # For text to speech

# Weather information
class forecast:
    def __init__(self,zip_in):
        zip_code = zip_in

        print("Retrieving weather info...")
        weather = pywapi.get_weather_from_weather_com(zip_code,units='imperial')
        weather_today = weather['forecasts'][0]
        
        self.location = weather['location']['name'].split('(')[0]

        self.temp_high = weather_today['high']
        self.temp_low = weather_today['low']
        self.day_humidity = weather_today['day']['humidity']
        self.day_precip = weather_today['day']['chance_precip']
        self.night_humidity = weather_today['night']['humidity']
        self.night_precip = weather_today['night']['chance_precip']
        self.sunrise = weather_today['sunrise']
        self.sunset = weather_today['sunset']

    def temp_message(self):
        message = "Today's temperature will range from {} to {} degrees".format(self.temp_low,self.temp_high)
        tts(message)

    def precipitation_message(self):
        message = "Chance of precipitation in the day is {}% and at night is {}%".format(self.day_precip,self.night_precip)
        tts(message)

    def sunset_message(self):
        message = "Sunset is at {}".format(self.sunset)
        tts(message)
