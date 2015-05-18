import pyttsx# For text to speech
import pywapi # For weather

from datetime import datetime
from threading import Timer

NAME = ''
ZIP_CODE = ''
SPEECH_SPEED = 130
WAKE_TIME = r'7:00'

# Weather information
class forecast:
    zip_code = ZIP_CODE
    weather = pywapi.get_weather_from_weather_com(zip_code,units='imperial')

    weather_today = weather['forecasts'][0]
    location = weather['location']['name'].split('(')[0]

    temp_high = weather_today['high']
    temp_low = weather_today['low']
    day_humidity = weather_today['day']['humidity']
    day_precip = weather_today['day']['chance_precip']
    night_humidity = weather_today['night']['humidity']
    night_precip = weather_today['night']['chance_precip']
    sunrise = weather_today['sunrise']
    sunset = weather_today['sunset']

# Message to be spoken
def message():
    message = "Good morning {}. Here is your weather forecast for {}. " \
              "Temperature lows at {} and highs at {}. " \
              "Chance of precipitation in the day is {}% and at night is {}%. " \
              "The sun will set at {}".format(NAME,forecast.location,forecast.temp_low,forecast.temp_high,
                                              forecast.day_precip,forecast.night_precip,forecast.sunset)
    return message

def text_to_speech(text):
    engine = pyttsx.init()
    engine.setProperty('rate',SPEECH_SPEED)
    engine.say(text)
    engine.runAndWait()

def schedule(alarm_time,scheduled_function):
    alarm_hour = int(alarm_time.split(':')[0])
    alarm_minute = int(alarm_time.split(':')[1])

    time_now = datetime.today()
    run_time = (time_now.replace(day = time_now.day, hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0))
    delta_t = run_time-time_now

    print(time_now)
    print(run_time)
    print(delta_t)

    secs = delta_t.seconds+1

    t = Timer(secs,scheduled_function)
    t.start()

####################

print(message())
schedule(WAKE_TIME,lambda: text_to_speech(message()))
#print(message)
#text_to_speech(message)
