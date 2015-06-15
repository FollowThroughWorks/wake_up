import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from utilities import load_settings, save_settings # For saving and loading preferences
import wake # For scheduling waking when Wake Up! is pressed
import modules.alarm
import datetime

###### METHODS #########
def toggle_subchoices(parent_frame):
    check_state = parent_frame.check_state.get()
    print("{}: {}".format(type(parent_frame),check_state))
    for choice_object in parent_frame.winfo_children()[1:]:
        # For all child objects except the first (the check button), toggle if it's disabled or not
        if check_state:
            enable_widget(choice_object)
        else:
            disable_widget(choice_object)

def disable_widget(widget):
    if widget.winfo_class() != 'Frame':
        widget.state(['disabled'])
    else:
        disable_children(widget)
        
def disable_children(parent_frame):
    for child in parent_frame.winfo_children():
        child.state(['disabled'])

def enable_widget(widget):
    if widget.winfo_class() != 'Frame':
        widget.state(['!disabled'])
    else:
        enable_children(widget)

def enable_children(parent_frame):
    check_state = parent_frame.check_state.get()
    parent_frame.winfo_children()[0].state(['!disabled'])
    for child in parent_frame.winfo_children()[1:]:
        if check_state:
            child.state(['!disabled'])
        
def update_label(to_display,label):
    label.configure(text = "{}".format(to_display))
    
def file_choice(parent_frame):
    parent_frame.filename.set(askopenfilename())

def alert_window(message):
    alert = tk.Toplevel()

    text = ttk.Label(alert,text=message)
    text.grid(column=1,row=1)

    button = ttk.Button(alert, text="Okay", command=alert.destroy)
    button.grid(column=1,row=2)

    alert.columnconfigure(1,weight=1)

def choose_alarm(alarm_frame):
    file_choice(alarm_frame)
    if not '.mp3' in alarm_frame.filename.get():
        alert_window("Please choose an mp3 file")
        alarm_frame.filename.set("Invalid File")
    else:
        file_length = modules.alarm.sound(alarm_frame.filename.get()).length
        alarm_frame.alarm_length_scale.configure(to=file_length)
        if alarm_frame.duration.get() > file_length: alarm_frame.duration.set(file_length)
        update_label("Duration: {}".format(alarm_frame.duration.get()),alarm_frame.length_label)
    
###### CLASSES TO INHERIT FROM ########
    
class ChoiceAndSubchoicesFrame(tk.Frame):
    def __init__(self,parent,option_name):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        self.config(borderwidth=1,relief='ridge',padx=5,pady=5)

        # Checkbox to turn on or off
        self.check_state = tk.IntVar(value=0)     
        self.on_off_check = ttk.Checkbutton(self,text=option_name,variable=self.check_state,
                                command=lambda: toggle_subchoices(self),style='ChoiceAndSubchoices.TCheckbutton')
        self.on_off_check.grid(column=1,row=0,columnspan=4)

        # Image
        try:
            img = tk.PhotoImage(file='images/{}.gif'.format(option_name.lower()))
            img_label = ttk.Label(self,image=img)
            img_label.image = img
            img_label.grid(column=0,row=0)
        except tk.TclError:
            print("No image found")    

        # Disable everything but the main choice
        toggle_subchoices(self)
        
        # Padding between elements
        for child in self.winfo_children(): child.grid_configure(padx=2,pady=2)

        

class SubSubchoicesFrame(ChoiceAndSubchoicesFrame):
    def __init__(self,parent,option_name):
        ChoiceAndSubchoicesFrame.__init__(self,parent,option_name)
        self.parent = parent
        self.on_off_check.configure(style='SubSubchoices.TCheckbutton')
        self.config(relief='sunken')
        
####### ACTUAL CONTENT, NOT ABSTRACTIONS ########

# --------- Options frames --------- #

class TimeFrame(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)
        self.parent = parent

        # Name
        name_label= ttk.Label(self,text="Name:")
        name_label.grid(column=1,row=2,sticky='E')
        self.name = tk.StringVar()
        name_entry = ttk.Entry(self,textvariable=self.name)
        name_entry.grid(column=2,row=2,pady=5)

        # Time
        vcmd = self.register(self.validate_time)  

        time_label = ttk.Label(self,text="Wake Time:",style="TimeFrame.TLabel")
        time_label.grid(column=1,row=1)

        self.wake_time = tk.StringVar(value="07:00")
        time_entry = ttk.Entry(self,textvariable=self.wake_time,validate='focusout',
                               validatecommand=(vcmd,'%P'),style="TimeLabel.TEntry")
        time_entry.grid(column=2,row=1,padx=5)

        self.am_pm = tk.StringVar()
        am = ttk.Radiobutton(self,text="AM",variable=self.am_pm,value="am",command=lambda: print(self.am_pm.get()))
        pm = ttk.Radiobutton(self,text="PM",variable=self.am_pm,value="pm",command=lambda: print(self.am_pm.get()))
        am.grid(column=3,row=1)
        pm.grid(column=4,row=1)

    def validate_time(self,new_text):
        # If there is text
        if new_text:
            try:
                hour = new_text.split(':')[0]
                minute = new_text.split(':')[1]
                assert len(minute) == 2
                assert int(minute) < 61
                assert len(hour) > 0 and len(hour) < 3
                assert int(hour) < 13
                if len(hour) == 1:
                    hour = "0{}".format(hour)
                self.wake_time.set('{}:{}'.format(hour,minute))
                self.parent.parent.buttons.schedule_button.state(['!disabled'])
            except (IndexError,AssertionError):
                alert_window("Invalid time")
                self.parent.parent.buttons.schedule_button.state(['disabled'])
        # If there is no text
        else:
            alert_window("Invalid time")
            self.parent.parent.buttons.schedule_button.state(['disabled'])

        return True

class AlarmFrame(ChoiceAndSubchoicesFrame):
    def __init__(self,parent):
        ChoiceAndSubchoicesFrame.__init__(self,parent,"Alarm")
        
        # Filename field
        self.filename = tk.StringVar(value="modules/bugle.mp3")
        entry_one = ttk.Entry(self,textvariable=self.filename)
        entry_one.grid(column=1,row=1)

        # File select button
        file_select_button = ttk.Button(self,text="Select File",command=lambda: choose_alarm(self))
        file_select_button.grid(column=2,row=1)

        # Song length scale
        self.length_label = ttk.Label(self,text="Duration: 0")
        self.length_label.grid(column=1,row=3,columnspan=2)
       
        self.duration = tk.IntVar()
        self.alarm_length_scale = ttk.Scale(self,orient=tk.HORIZONTAL,from_=1,to=200,variable=self.duration,value=1)
        self.alarm_length_scale.config(command=lambda x: update_label("Duration: {}".format(self.duration.get()),self.length_label))
        self.alarm_length_scale.grid(column=1,row=2,columnspan=2)

        # Disable everything but the main choice
        toggle_subchoices(self)

        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)

class WeatherFrame(ChoiceAndSubchoicesFrame):
    def __init__(self,parent):
        ChoiceAndSubchoicesFrame.__init__(self,parent,"Weather")

        vcmd = self.register(self.validate_zip)
        
        # Zip Code
        self.zip = tk.IntVar()

        zip_label = ttk.Label(self,text="Zip Code")
        zip_label.grid(column=1,row=1)
        zip_entry = ttk.Entry(self,textvariable=self.zip,validate='focusout',
                              validatecommand = (vcmd,'%P'))
        zip_entry.grid(column=2,row=1)


        # Options
        self.temp = tk.BooleanVar()
        temp_check = ttk.Checkbutton(self,text="Temperature",variable=self.temp)
        temp_check.grid(column=1,row=2)

        self.precipitation = tk.BooleanVar()
        precipitation_check = ttk.Checkbutton(self,text="Precipitation",variable=self.precipitation)
        precipitation_check.grid(column=2,row=2)

        self.sunset = tk.BooleanVar()
        sunset_check = ttk.Checkbutton(self,text="Sunset",variable=self.sunset)
        sunset_check.grid(column=1,row=3)
        
        toggle_subchoices(self)

        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)

    def validate_zip(self,new_text):
        # If there is text
        if new_text:
            try:
                assert len(new_text) == 5
                return True
            except (AssertionError):
                alert_window("Please insert a 5-digit zip")
                self.zip.set("00000")
                return True
        # If there is no text
        else:
            alert_window("Please insert a 5-digit zip")
            self.zip.set("00000")
            return False

class EventsFrame(ChoiceAndSubchoicesFrame):
    def __init__(self,parent):
        ChoiceAndSubchoicesFrame.__init__(self,parent,"Events")

        self.google_cal = tk.BooleanVar()
        google_cal_check = ttk.Checkbutton(self,text="Google",variable=self.google_cal)
        google_cal_check.grid(column=1,row=1)
        
        '''
        self.facebook = tk.BooleanVar()
        facebook_check = ttk.Checkbutton(self,text="Facebook",variable=self.facebook)
        facebook_check.grid(column=2,row=1)
        '''
        
        toggle_subchoices(self)

        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)

class EmailsFrame(ChoiceAndSubchoicesFrame):
    def __init__(self,parent):
        ChoiceAndSubchoicesFrame.__init__(self,parent,"Emails")

        self.gmail = tk.BooleanVar()
        gmail_check = ttk.Checkbutton(self,text="Gmail",variable=self.gmail)
        gmail_check.grid(column=1,row=1)
        
        toggle_subchoices(self)
            
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
               
class PoetryFrame(ChoiceAndSubchoicesFrame):
    def __init__(self,parent):
        ChoiceAndSubchoicesFrame.__init__(self,parent,"Poetry")

    # Poetry foundation
        self.poetry_foundation = SubSubchoicesFrame(self,"Poetry Foundation")
        self.poetry_foundation.grid(column=1,row=1,sticky='NSEW')

        # Text
        self.pf_text = tk.BooleanVar()
        pf_text_check = ttk.Checkbutton(self.poetry_foundation,text="Display text",variable=self.pf_text)
        pf_text_check.grid(column=1,row=1,columnspan=3)

        # Audio
        self.pf_audio_type = tk.StringVar()
        pf_audio_tts = ttk.Radiobutton(self.poetry_foundation,text="Text-To-Speech",variable=self.pf_audio_type,
                                       value="tts",command=lambda: print(self.pf_audio_type.get()))
        pf_audio_tts.grid(column=1,row=2)
        pf_audio_site = ttk.Radiobutton(self.poetry_foundation,text="From Site",variable=self.pf_audio_type,
                                        value="site",command=lambda: print(self.pf_audio_type.get()))
        pf_audio_site.grid(column=2,row=2)
        pf_audio_none = ttk.Radiobutton(self.poetry_foundation,text="None",variable=self.pf_audio_type,
                                        value="none",command=lambda: print(self.pf_audio_type.get()))
        pf_audio_none.grid(column=3,row=2)

        toggle_subchoices(self.poetry_foundation)

    # Poets.org
        self.poets_org = SubSubchoicesFrame(self,"Poets.org")
        self.poets_org.grid(column=1,row=2)

        # Text
        self.po_text = tk.BooleanVar()
        po_text_check = ttk.Checkbutton(self.poets_org,text="Display text",variable=self.po_text)
        po_text_check.grid(column=1,row=1,columnspan=2)

        # Audio
        self.po_audio_type = tk.StringVar()
        po_audio_tts = ttk.Radiobutton(self.poets_org,text="Text-To-Speech",variable=self.po_audio_type,
                                      value='tts',command=lambda: print(self.po_audio_type.get()))
        po_audio_tts.grid(column=1,row=2)
        po_audio_none = ttk.Radiobutton(self.poets_org,text="None",variable=self.po_audio_type,
                                      value='none',command=lambda: print(self.po_audio_type.get()))
        po_audio_none.grid(column=2,row=2)  

        toggle_subchoices(self)

        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        
class SocialMediaFrame(ChoiceAndSubchoicesFrame):
    def __init__(self,parent):
        ChoiceAndSubchoicesFrame.__init__(self,parent,"Social Media")

        # Load in images
        fb_img = tk.PhotoImage(file='images/facebook.gif')
        
        # Authenticate Buttons
        '''
        authenticate_label = ttk.Label(self,text="Authenticate:")
        authenticate_label.grid(column=1,row=1)

        authenticate_fb = ttk.Button(self,image=fb_img)
        authenticate_fb.image = fb_img
        authenticate_fb.grid(column=2,row=1)
        toggle_subchoices(self)
        '''

        # Notifications
        self.facebook = tk.BooleanVar()
        fb_notifications_check = ttk.Checkbutton(self,image=fb_img,variable=self.facebook)
        fb_notifications_check.image = fb_img
        fb_notifications_check.grid(column=1,row=1)

        toggle_subchoices(self)
        
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)

class ToDoFrame(ChoiceAndSubchoicesFrame):
    def __init__(self,parent):
        ChoiceAndSubchoicesFrame.__init__(self,parent,"To Do")

        self.any_do = tk.BooleanVar()
        any_do_check = ttk.Checkbutton(self,text="Any.do",variable=self.any_do)
        any_do_check.grid(column=1,row=1)
        
        toggle_subchoices(self)

        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
           
# ----------- Container Frames ------------- #

# Frame containing all of the options        
class OptionsFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.parent = parent

        self.time = TimeFrame(self)
        self.time.grid(column=1,row=1,columnspan=2,pady=5)
        
        self.alarm = AlarmFrame(self)
        self.alarm.grid(column=1,row=2,sticky='NSEW')

        self.weather = WeatherFrame(self)
        self.weather.grid(column=2,row=2,sticky='NSEW')

        self.emails = EmailsFrame(self)
        self.emails.grid(column=1,row=3,sticky='NSEW')

        self.todo = ToDoFrame(self)
        self.todo.grid(column=2,row=3,sticky='NSEW')

        self.events = EventsFrame(self)
        self.events.grid(column=1,row=4,sticky='NSEW')
        
        self.social_media = SocialMediaFrame(self)
        self.social_media.grid(column=2,row=4,sticky='NSEW')

        self.poetry = PoetryFrame(self)
        self.poetry.grid(column=1,row=5,sticky='NSEW')

        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        # Make rows and columns expand
        for x in range(2,6):
            self.rowconfigure(x,weight=1)

# --------- Other frames ---------- #

# Frame containing the display information
class DisplayFrame(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)
        self.parent = parent

        self.config(borderwidth=5,relief='sunken')

        text_label = ttk.Label(self,text="Alarm will go off in:")
        text_label.grid(column=1,row=1,sticky='E')

        self.timer = ttk.Label(self,text="00:00:00")
        self.timer.grid(column=2,row=1,sticky='W')

        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)

    def update_timer(self,alarm_time):
        now = datetime.datetime.now()
        countdown = alarm_time - now
        countdown_hours = int(countdown.seconds / 3600)
        countdown_minutes = int(countdown.seconds / 60 % 60)
        countdown_seconds = int(countdown.seconds % 60)
        timer = "{}:{}:{}".format(countdown_hours,countdown_minutes,countdown_seconds)
        
        self.timer.configure(text=timer)
        self.after(1000,lambda: self.update_timer(alarm_time))

class ButtonsFrame(ttk.Frame):
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)
        self.parent = parent

        save_settings_button = ttk.Button(self,text="Save Settings",command=lambda: save_settings(self.parent.options))
        save_settings_button.grid(column=1,row=1,sticky='NSEW',padx=30)

        self.run_button = ttk.Button(self,text="Run Now", command = lambda: wake.run_wake_from_gui(self.parent.options))
        self.run_button.grid(column=2,row=1)
        
        self.schedule_button = ttk.Button(self,text="Schedule",command= self.on_schedule)
        self.schedule_button.grid(column=3,row=1,sticky='NSEW',padx=30)

        close_button = ttk.Button(self,text="Close",command=lambda: parent.parent.destroy())
        close_button.grid(column=4,row=1,sticky='NSEW',padx=30)

        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)
        self.columnconfigure(4,weight=1)

    def on_schedule(self):
        self.parent.scheduler.schedule(self.parent.options.time.wake_time.get(),self.parent.options.time.am_pm.get(),lambda: wake.run_wake_from_gui(self.parent.options))
        # Update display
        alarm_time = self.parent.scheduler.run_time
        self.parent.display.update_timer(alarm_time)
        
# The main window   
class MainApplication(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        tk.Frame.__init__(self,parent)
        self.parent = parent
        
        # Fonts & Styles
        choiceandsubchoice_font = tk.font.Font(size=10,weight='bold')
        subsubchoice_font = tk.font.Font(size=8,weight='bold')
        timelabel_font = tk.font.Font(size=12,weight='bold')
       
        s = ttk.Style()
        s.configure('SubSubchoices.TCheckbutton',font=subsubchoice_font)
        s.configure('ChoiceAndSubchoices.TCheckbutton',font=choiceandsubchoice_font)
        s.configure('TimeFrame.TLabel',font=timelabel_font)
        s.configure('TimeFrame.TEntry',font=timelabel_font)

        # Frames
        self.options = OptionsFrame(self)
        self.options.grid(column=1,row=1,padx=5,pady=5,sticky='NSEW')
   
        self.buttons = ButtonsFrame(self)
        self.buttons.grid(column=1,row=2,sticky='NSEW',columnspan=2,pady=5)

        self.display = DisplayFrame(self)
        self.display.grid(column=1,row=3,padx=5,pady=5,sticky='NSEW')

        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.rowconfigure(1,weight=1)

        # Load options
        load_settings(self.options)

        for frame in self.options.winfo_children():
            try:
                toggle_subchoices(frame)
            except:
                print("No checkbox for {}".format(type(frame)))
                pass

        # Updates the alarm duration label on first load
        update_label("Duration: {}".format(self.options.alarm.duration.get()),self.options.alarm.length_label)

        # Creates scheduler object
        self.scheduler = wake.scheduler()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wake Up!")
    root.iconbitmap('images/clock.ico')
    MainApplication(root).pack(side="top",fill="both",expand=True)
    root.mainloop()
