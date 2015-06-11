import pyttsx# For text to speech

from datetime import datetime
from threading import Timer

from modules.weather import forecast_info
from modules.poetry import potd_poets_org, potd_poetry_foundation
from modules.events import google_calendar
from modules.email_ import gmail
from modules.facebook import notifications
from modules.anydo_ import any_do

import modules.alarm as alarm

# Constants
NAME = 'Mike'
ZIP_CODE = '11788'
SPEECH_SPEED = 130
WAKE_TIME = r'07:00:00'

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
    forecast = forecast_info(ZIP_CODE)
    message = "Here is your weather forecast for {}: " \
              "\n\tTemperature lows at {} and highs at {}. " \
              "\n\tChance of precipitation in the day is {}% and at night is {}%. " \
              "\n\tThe sun will set at {}.".format(forecast.location,
                                                   forecast.temp_low,forecast.temp_high,
                                                   forecast.day_precip,forecast.night_precip,forecast.sunset)
    print(message)
    text_to_speech(message)

def message_events():
    calendar = google_calendar()
    message = "Here are your events for the day:" \
              "\n\t{}".format('\n'.join(calendar.events("day")))
    print(message)
    text_to_speech(message)

def message_emails():
    email = gmail()
    message = "You have {} unread emails".format(email.unread_emails())
    print(message)
    text_to_speech(message)

def message_poem_po():
    potd_po = potd_poets_org()
    message = "The poets.org poem of the day is {}, by {}:" \
              "\n\n{}".format(potd_po.title,potd_po.author,'\n'.join(potd_po.lines))
    print(message)
    text_to_speech(message)

def message_poem_pf():
    potd_pf = potd_poetry_foundation()
    message = "The Poetry Foundation poem of the day is {}, by {}:\n".format(potd_pf.title,potd_pf.author)
    print(message)
    text_to_speech(message)
    print('\n'.join(potd_pf.lines))
    potd_pf.read_poem()

def message_facebook():
    fb_notifications = notifications()
    message = 'You have {} unseen facebook notifications and {} unread facebook notifications.'.format(fb_notifications.unseen_count,fb_notifications.unread_count)
    print(message)
    text_to_speech(message)

def message_anydo():
    ad = any_do()
    message = 'You have {} unchecked tasks on Any Do'.format(ad.unchecked_task_count)
    print(message)
    text_to_speech(message)

# Method that runs in morning
def wake(music=True,greeting=True,weather=True,calendar=False,emails=False,poem_po=False,poem_pf=False,fb=False,ad=False):

    if music: alarm.play_song()    
    if greeting: message_greeting()
    if weather: message_weather()
    if calendar: message_events()
    if emails: message_emails()
    if poem_po: message_poem_po()
    if poem_pf: message_poem_pf()
    if fb: message_facebook()
    if ad: message_anydo()

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

if __name__ == '__main__':
    wake_function = lambda: wake(music=True,greeting=True,weather=True,calendar=True,emails=True,poem_po=True,poem_pf=True,fb=True)
    # wake_function() # For testing
    schedule(WAKE_TIME,wake_function)
