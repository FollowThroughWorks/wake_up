from datetime import datetime # For scheduling the alarm
from threading import Timer # For scheduling the alarm

import modules.alarm # For calling the functions to do things

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

# What actually happens
def run_wake(options_frame):
    modules.alarm.play_song(3)
    function_queue = []
    if options_frame.alarm.check_state.get() == 1:
        alarm_args = (options_frame.alarm.duration.get(),options_frame.alarm.filename.get())
        function_queue.append([modules.alarm.play_song,alarm_args])

        print(function_queue)

    if options_frame.weather.check_state.get() == 1:
        forecast = modules.weather.forecast(options_frame.weather.zip.get())
        if options_frame.weather.temp_check.get() == 1:
            function_queue.append([forecast.temp_message,()])
        
    for function_args_pair in function_queue:
        function_args_pair[0](*function_args_pair[1])
        
    wake_time = options_frame.time.wake_time.get()
    greeting = True
    music = options_frame.alarm.check_state.get()
    weather = options_frame.weather.check_state.get()
    events = options_frame.events.check_state.get()
    emails = options_frame.emails.check_state.get()
    poem_po = options_frame.poetry.poets_org.check_state.get()
    poem_pf = options_frame.poetry.poetry_foundation.check_state.get()
    social_media = options_frame.social_media.check_state.get()
    wake_function = lambda: wake(music=music,greeting=greeting,weather=weather,calendar=events,emails=emails,poem_po=poem_po,poem_pf=poem_pf,fb=social_media)
    schedule(wake_time,wake_function)

