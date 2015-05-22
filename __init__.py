import pyttsx# For text to speech

from datetime import datetime
from threading import Timer

from alerts import forecast_info
from alerts import potd_poets_org, potd_poetry_foundation
from alerts import calendar
from alerts import gmail

NAME = 'Mike'
ZIP_CODE = '06519'
SPEECH_SPEED = 130
WAKE_TIME = r'12:21:00'

forecast = forecast_info(ZIP_CODE)
potd_po = potd_poets_org()
potd_pf = potd_poetry_foundation()
calendar = calendar()
email = gmail()


# Message to be spoken
def get_message():
    message = "Good morning {}.\n\n" \
              "Here is your weather forecast for {}: " \
              "\n\tTemperature lows at {} and highs at {}. " \
              "\n\tChance of precipitation in the day is {}% and at night is {}%. " \
              "\n\tThe sun will set at {}." \
              "\nHere are your events for the day:" \
              "\n\t{}" \
              "\nYou have {} unread emails".format(NAME,forecast.location,forecast.temp_low,forecast.temp_high,
                                              forecast.day_precip,forecast.night_precip,forecast.sunset,
                                              [event for event in calendar.events("day")],
                                                   email.unread_emails())
    return message

# Reads argument text aloud
def text_to_speech(text):
    engine = pyttsx.init()
    engine.setProperty('rate',SPEECH_SPEED)
    engine.say(text)
    engine.runAndWait()

# Schedule a function to occur at the same time every day
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
print(message)
schedule(WAKE_TIME,lambda: text_to_speech(message))
