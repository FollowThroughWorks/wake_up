import pywapi

# Weather information
class forecast_info:
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
