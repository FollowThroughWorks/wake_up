from datetime import datetime # For scheduling the alarm
from threading import Timer # For scheduling the alarm

import modules.alarm # For calling the functions to do things
import modules.weather
import modules.events
import modules.email_
import modules.poetry
import modules.facebook
import modules.anydo_

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

def run_functions(function_queue):             
    for function_args_pair in function_queue:
        function_args_pair[0](*function_args_pair[1])
        
# What actually happens
def run_wake(options_frame):
    
    # List of [function,(args)] to call at scheduled time
    function_queue = []

    # Alarm
    if options_frame.alarm.check_state.get() == 1:
        sound = modules.alarm.sound(options_frame.alarm.filename.get())
        alarm_args = (options_frame.alarm.duration.get(),)
        function_queue.append([sound.play,alarm_args])

    # Weather
    if options_frame.weather.check_state.get() == 1:
        forecast = modules.weather.forecast(options_frame.weather.zip.get())
        # Temperature
        if options_frame.weather.temp.get() == 1:
            function_queue.append([forecast.temp_message,()])
        # Precipitation
        if options_frame.weather.precipitation.get() == 1:
            function_queue.append([forecast.precipitation_message,()])
        # Sunset
        if options_frame.weather.sunset.get() == 1:
            function_queue.append([forecast.sunset_message,()])

    # Events
    if options_frame.events.check_state.get() == 1:
        # Google Calendar
        if options_frame.events.google_cal.get() == 1:
            google_events = modules.events.google_calendar()
            function_queue.append([google_events.events_message,()])

    # Emails
    if options_frame.emails.check_state.get() == 1:
        # Gmail
        if options_frame.emails.gmail.get() == 1:
            gmail = modules.email_.gmail()
            function_queue.append([gmail.unread_emails_message,()])

    # Poetry
    if options_frame.poetry.check_state.get() == 1:
        # Poetry foundation
        if options_frame.poetry.poetry_foundation.check_state.get() == 1:
            pf = modules.poetry.potd_poetry_foundation()
            # Text
            if options_frame.poetry.pf_text.get() == 1:
                function_queue.append([pf.display_poem,()])
            # Audio                
            if options_frame.poetry.pf_audio_type.get() == 'site':
                function_queue.append([pf.read_poem_site,()])
            elif options_frame.poetry.pf_audio_type.get() == 'tts':
                function_queue.append([pf.read_poem_tts,()])
            elif options_frame.poetry.pf_audio_type.get() == 'none':
                print("No audio")
        # Poetry foundation
        if options_frame.poetry.poets_org.check_state.get() == 1:
            po = modules.poetry.potd_poets_org()
            # Text
            if options_frame.poetry.po_text.get() == 1:
                function_queue.append([po.display_poem,()])
            # Audio                
            if options_frame.poetry.po_audio_type.get() == 'tts':
                function_queue.append([po.read_poem_tts,()])
            elif options_frame.poetry.po_audio_type.get() == 'none':
                pass

    # Social Media
    if options_frame.social_media.check_state.get() == 1:
        # Facebook
        if options_frame.social_media.facebook.get() == 1:
            fb = modules.facebook.notifications()
            function_queue.append([fb.notifications_message,()])

    # To Do
    if options_frame.todo.check_state.get() == 1:
        # Any.Do
        if options_frame.todo.any_do.get() == 1:
            ad = modules.anydo_.any_do()
            function_queue.append([ad.tasks_message,()])
 
    wake_time = options_frame.time.wake_time.get()
    '''
    greeting = True
    music = options_frame.alarm.check_state.get()
    weather = options_frame.weather.check_state.get()
    events = options_frame.events.check_state.get()
    emails = options_frame.emails.check_state.get()
    poem_po = options_frame.poetry.poets_org.check_state.get()
    poem_pf = options_frame.poetry.poetry_foundation.check_state.get()
    social_media = options_frame.social_media.check_state.get()
    '''
    wake_function = lambda: run_functions(function_queue)
    schedule(wake_time,wake_function)

