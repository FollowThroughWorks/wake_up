import json # For loading preferences
import pyttsx # For reading text
import modules.alarm # For loading alarm scale size

SPEECH_SPEED = 130

def text_to_speech(text):
    engine = pyttsx.init()
    engine.setProperty('rate',SPEECH_SPEED)
    engine.say(text)
    engine.runAndWait()
    
def load_settings(options_frame):
    try:
        with open('settings.json','r') as in_json:
            settings = json.loads(in_json.read())

        options_frame.time.wake_time.set(settings['time']['wake time'])
        options_frame.time.am_pm.set(settings['time']['am_pm'])
        options_frame.time.name.set(settings['time']['name'])
        
        options_frame.alarm.check_state.set(settings['alarm']['check_state'])
        options_frame.alarm.filename.set(settings['alarm']['file'])
        options_frame.alarm.duration.set(settings['alarm']['duration'])
        alarm_length = modules.alarm.sound(settings['alarm']['file']).length
        options_frame.alarm.alarm_length_scale.configure(to=alarm_length)

        options_frame.weather.check_state.set(settings['weather']['check_state'])    
        options_frame.weather.zip.set(settings['weather']['zip'])
        options_frame.weather.temp.set(settings['weather']['temp'])
        options_frame.weather.precipitation.set(settings['weather']['precipitation'])
        options_frame.weather.sunset.set(settings['weather']['sunset'])

        options_frame.events.check_state.set(settings['events']['check_state'])    
        options_frame.events.google_cal.set(settings['events']['google']),
        #options_frame.events.facebook.set(settings['events']['facebook'])

        options_frame.emails.check_state.set(settings['emails']['check_state'])
        options_frame.emails.gmail.set(settings['emails']['gmail'])

        options_frame.poetry.check_state.set(settings['poetry']['check_state'])
        options_frame.poetry.pf_text.set(settings['poetry']['poetry_pf']['text'])
        options_frame.poetry.pf_audio_type.set(settings['poetry']['poetry_pf']['audio'])
        options_frame.poetry.poetry_foundation.check_state.set(settings['poetry']['poetry_pf']['check_state'])
        options_frame.poetry.po_text.set(settings['poetry']['poetry_po']['text'])
        options_frame.poetry.po_audio_type.set(settings['poetry']['poetry_po']['audio'])
        options_frame.poetry.poets_org.check_state.set(settings['poetry']['poetry_po']['check_state'])

        options_frame.social_media.check_state.set(settings['social media']['check_state'])    
        options_frame.social_media.facebook.set(settings['social media']['facebook'])

        options_frame.todo.check_state.set(settings['to do']['check_state'])    
        options_frame.todo.any_do.set(settings['to do']['anydo'])
    except:
        print("No settings file found")

    
def save_settings(options_frame):
    settings = {
	"time": {
                "wake time":options_frame.time.wake_time.get(),
                "am_pm":options_frame.time.am_pm.get(),
                "name":options_frame.time.name.get()
        },
	"alarm": {
                "check_state": options_frame.alarm.check_state.get(),
		"file": options_frame.alarm.filename.get(),
		"duration": options_frame.alarm.duration.get()
	},
	"weather": {
                "check_state": options_frame.weather.check_state.get(),
		"zip": options_frame.weather.zip.get(),
		"temp": options_frame.weather.temp.get(),
		"precipitation": options_frame.weather.precipitation.get(),
		"sunset": options_frame.weather.sunset.get()
	},
	"events": {
                "check_state": options_frame.events.check_state.get(),
		"google": options_frame.events.google_cal.get(),
		"facebook": ""#options_frame.events.facebook.get()
	},
	"emails": {
                "check_state": options_frame.emails.check_state.get(),
		"gmail": options_frame.emails.gmail.get()
	},
	"poetry": {
                "check_state": options_frame.poetry.check_state.get(),
		"poetry_pf": {
                        "check_state": options_frame.poetry.poetry_foundation.check_state.get(),
			"text": options_frame.poetry.pf_text.get(),
			"audio": options_frame.poetry.pf_audio_type.get()
		},
		"poetry_po": {
                        "check_state": options_frame.poetry.poets_org.check_state.get(),
			"text": options_frame.poetry.po_text.get(),
			"audio": options_frame.poetry.po_audio_type.get()
		}
	},
	"social media": {
                "check_state": options_frame.social_media.check_state.get(),
		"facebook": options_frame.social_media.facebook.get()
	},
	"to do": {
                "check_state": options_frame.todo.check_state.get(),
		"anydo": options_frame.todo.any_do.get()
	}
    }
    print("Saving settings")
    with open('settings.json', 'w') as out_json:
        json.dump(settings, out_json)
