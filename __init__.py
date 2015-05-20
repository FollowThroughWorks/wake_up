import pyttsx# For text to speech

from datetime import datetime
from threading import Timer

from alerts import forecast_info, potd_poets_org, potd_poetry_foundation

NAME = ''
ZIP_CODE = '06519'
SPEECH_SPEED = 130
WAKE_TIME = r'07:00:00'

forecast = forecast_info(ZIP_CODE)
potd_po = potd_poets_org()
potd_pf = potd_poetry_foundation()

# Message to be spoken
def get_message():
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
    alarm_second = int(alarm_time.split(':')[2])

    time_now = datetime.today()
    run_time = time_now.replace(day = (time_now.day)+1, hour=alarm_hour, minute=alarm_minute, second=alarm_second, microsecond=0)
    delta_t = run_time-time_now

    secs = delta_t.seconds+1

    t = Timer(secs,scheduled_function)
    t.start()
    t2 = Timer(secs,lambda: schedule(alarm_time,scheduled_function))
    t2.start()

####################

message = get_message()
schedule(WAKE_TIME,lambda: text_to_speech(message))
#print(message)
#text_to_speech(message)
