import pyttsx# For text to speech

from datetime import datetime
from threading import Timer

from alerts import forecast_info
from alerts import potd_poets_org, potd_poetry_foundation
from alerts import calendar
from alerts import gmail

import alarm

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
def get_message(greeting=True,weather=True,events=True,emails=False,poem_po=False,poem_pf=False):
    message_greeting = "Good morning {}.".format(NAME)
    
    message_weather = "Here is your weather forecast for {}: " \
              "\n\tTemperature lows at {} and highs at {}. " \
              "\n\tChance of precipitation in the day is {}% and at night is {}%. " \
              "\n\tThe sun will set at {}.".format(forecast.location,
                                                   forecast.temp_low,forecast.temp_high,
                                                   forecast.day_precip,forecast.night_precip,forecast.sunset)

    message_events = "Here are your events for the day:" \
              "\n\t{}".format('\n'.join(calendar.events("day")))

    message_emails = "You have {} unread emails".format(email.unread_emails())

    message_poem_po = "The poets.org poem of the day is {}, by {}:" \
              "\n\n{}".format(potd_po.title,potd_po.author,'\n'.join(potd_po.lines))

    message_poem_pf = "The Poetry Foundation poem of the day is {}, by {}:" \
              "\n\n{}".format(potd_pf.title,potd_pf.author,'\n'.join(potd_pf.lines))

    message = ""
    if greeting: message += message_greeting + '\n\n'
    if weather: message += message_weather + '\n\n'
    if events: message += message_events + '\n\n'
    if emails: message += message_emails + '\n\n'
    if poem_po: message += message_poem_po + '\n\n'
    if poem_pf: message += message_poem_pf + '\n\n'
    
    return message

# Reads argument text aloud
def text_to_speech(text):
    engine = pyttsx.init()
    engine.setProperty('rate',SPEECH_SPEED)
    engine.say(text)
    engine.runAndWait()

def wake(music=False,speech=True):

    message = get_message(emails=True)
    
    if music:
        alarm.play_song()
    
    if speech:
        print(message)
        #text_to_speech(message)

    
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

wake(music=True)
schedule(WAKE_TIME,lambda: wake())
