import json # For loading preferences

def toggle_subchoices(parent_frame):
    check_state = parent_frame.check_state.get()
    print("{}: {}".format(type(parent_frame),check_state))
    for choice_object in parent_frame.winfo_children()[1:]:
        # For all child objects except the first (the check button), toggle if it's disabled or not
        if check_state:
            enable_widget(choice_object)
        else:
            disable_widget(choice_object)
            
def text_to_speech(text):
    engine = pyttsx.init()
    engine.setProperty('rate',SPEECH_SPEED)
    engine.say(text)
    engine.runAndWait()
    
def load_settings(options_frame):
    with open('settings.json','r') as in_json:
        settings = json.loads(in_json.read())

    options_frame.time.wake_time.set(settings['time'])
    options_frame.alarm.check_state.set(settings['alarm']['check_state'])
    options_frame.alarm.filename.set(settings['alarm']['file'])
    options_frame.alarm.duration.set(settings['alarm']['duration'])

    options_frame.weather.check_state.set(settings['weather']['check_state'])    
    options_frame.weather.zip.set(settings['weather']['zip'])
    options_frame.weather.temp.set(settings['weather']['temp'])
    options_frame.weather.precipitation.set(settings['weather']['precipitation'])
    options_frame.weather.sunset.set(settings['weather']['sunset'])

    options_frame.events.check_state.set(settings['events']['check_state'])    
    options_frame.events.google_cal.set(settings['events']['google']),
    options_frame.events.facebook.set(settings['events']['facebook'])

    options_frame.emails.check_state.set(settings['emails']['check_state'])
    options_frame.emails.gmail.set(settings['emails']['gmail'])

    options_frame.poetry.check_state.set(settings['poetry']['check_state'])
    options_frame.poetry.pf_text.set(settings['poetry']['poetry_pf']['text'])
    options_frame.poetry.pf_audio_type.set(settings['poetry']['poetry_pf']['audio'])
    options_frame.poetry.check_state.set(settings['poetry']['poetry_pf']['check_state'])
    options_frame.poetry.po_text.set(settings['poetry']['poetry_po']['text'])
    options_frame.poetry.po_audio_type.set(settings['poetry']['poetry_po']['audio'])
    options_frame.poetry.check_state.set(settings['poetry']['poetry_po']['check_state'])

    options_frame.social_media.check_state.set(settings['social media']['check_state'])    
    options_frame.social_media.facebook.set(settings['social media']['facebook'])

    options_frame.todo.check_state.set(settings['to do']['check_state'])    
    options_frame.todo.any_do.set(settings['to do']['anydo'])

    for frame in options_frame.winfo_children():
        try:
            toggle_subchoices(frame)
        except:
            print("No checkbox for {}".format(type(frame)))
            pass
    
def save_settings(options_frame):
    settings = {
	"time": options_frame.time.wake_time.get(),
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
		"facebook": options_frame.events.facebook.get()
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
