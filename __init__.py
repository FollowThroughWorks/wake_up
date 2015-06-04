import pyttsx# For text to speech

from datetime import datetime
from threading import Timer

from weather import forecast_info
from poetry import potd_poets_org, potd_poetry_foundation
from events import google_calendar
from email_ import gmail

import alarm

# Constants
NAME = 'Mike'
ZIP_CODE = '11788'
SPEECH_SPEED = 130
WAKE_TIME = r'06:30:00'

# Retrieving information from alerts for messages
forecast = forecast_info(ZIP_CODE)
potd_po = potd_poets_org()
potd_pf = potd_poetry_foundation()
calendar = google_calendar()
email = gmail()

# Reads argument text aloud
def text_to_speech(text):
    engine = pyttsx.init()
    engine.setProperty('rate',SPEECH_SPEED)
    engine.say(text)
    engine.runAndWait()

# Methods for reading messages
def message_greeting():
    message = "Good morning {}.".format(NAME)
    print(message)
    text_to_speech(message)

def message_weather():    
    message = "Here is your weather forecast for {}: " \
              "\n\tTemperature lows at {} and highs at {}. " \
              "\n\tChance of precipitation in the day is {}% and at night is {}%. " \
              "\n\tThe sun will set at {}.".format(forecast.location,
                                                   forecast.temp_low,forecast.temp_high,
                                                   forecast.day_precip,forecast.night_precip,forecast.sunset)
    print(message)
    text_to_speech(message)

def message_events():
    message = "Here are your events for the day:" \
              "\n\t{}".format('\n'.join(calendar.events("day")))
    print(message)
    text_to_speech(message)

def message_emails():
    message = "You have {} unread emails".format(email.unread_emails())
    print(message)
    text_to_speech(message)

def message_poem_po():
    message = "The poets.org poem of the day is {}, by {}:" \
              "\n\n{}".format(potd_po.title,potd_po.author,'\n'.join(potd_po.lines))
    print(message)
    text_to_speech(message)

def message_poem_pf():    
    message = "The Poetry Foundation poem of the day is {}, by {}:\n".format(potd_pf.title,potd_pf.author)
    print(message)
    text_to_speech(message)
    print('\n'.join(potd_pf.lines))
    potd_pf.read_poem()

# Method that runs in morning
def wake(music=True,greeting=True,weather=True,calendar=False,emails=False,poem_po=False,poem_pf=False):

    if music: alarm.play_song()    
    if greeting: message_greeting()
    if weather: message_weather()
    if calendar: message_events()
    if emails: message_emails()
    if poem_po: message_poem_po()
    if poem_pf: message_poem_pf()

# Schedule a function to occur at the same time every day
def schedule(alarm_time,scheduled_function):
    alarm_hour = int(alarm_time.split(':')[0])
    alarm_minute = int(alarm_time.split(':')[1])
    alarm_second = int(alarm_time.split(':')[2])

    time_now = datetime.today()
    run_time = time_now.replace(day = (time_now.day)+1, hour=alarm_hour, minute=alarm_minute, second=alarm_second, microsecond=0)
    delta_t = run_time-time_now

    secs = delta_t.seconds+1

    print("Scheduling wakeup for {}".format(alarm_time))
    t = Timer(secs,scheduled_function)
    t.start()
    t2 = Timer(secs,lambda: schedule(alarm_time,scheduled_function))
    t2.start()


####################

wake_function = lambda: wake(music=True,greeting=True,weather=True,calendar=True,emails=True,poem_pf=True)
#wake(poem_pf = True, poem_po = True)
schedule(WAKE_TIME,wake_function)
