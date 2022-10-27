from tkinter import *
import tkinter as tk
import datetime
import turtle
import pytz
from scipy.io import wavfile
import sounddevice as sd
import numpy as np
import os
import glob
  

# Creating the root window
root = Tk()
root.geometry('700x700')
root.configure(background='linen')
root.title("Speaking Swahili clock by Fabienne and Vicky")
  
# Creating a listbox and attaching it to root window
listbox = Listbox(root)
  
# Adding Listbox to the left side of root window
listbox.pack(side = LEFT, fill = BOTH)
  
# Creating a Scrollbar and attaching it to root window
scrollbar = Scrollbar(root)
  
# Adding Scrollbar to the right side of root window
scrollbar.pack(side = RIGHT, fill = BOTH)

#list of common timezones
zons = pytz.common_timezones
  
# Insert elements into the listbox
for values in zons:
    listbox.insert(END, values)
      
# Attaching Listbox to Scrollbar
listbox.config(yscrollcommand = scrollbar.set, background="linen", foreground="black")
scrollbar.config(command = listbox.yview)

# Creating dictionary that matches western hour to what it would be in Swahili/Kenya
westhours = [*range(7, 20, 1)] + [20,21,22,23,0,1,2,3,4,5,6]
kenyahours = [*range(1,13,1)] + [*range(1,13,1)]
dict_kenya_time = dict(zip(westhours,kenyahours))

# Creating dictionary that matches Swahili words for numbers to integers
swahili_numbers = ["moja", "mbili", "tatu", "nne", "tano", "sita", "saba", "nane", "tisa", "kumi"]
numbers = [*range(1,11,1)]
swahili_numbers_dict = dict(zip(numbers, swahili_numbers))

# Creating dictionary that matches Swahili words to English words
swahili_words = ["dakika", "ishirini", "arobaini", "hamsini", "robo", "nusu", "na", "kasoro", "alasiri", "asubuhi", "jioni", "usiku", "mchana", "saa"]
words = ["minute", 20, 40, 50, 15, 30, "and", "without", "afternoon", "morning", "evening", "night", "daytime", "hour"]
swahili_words_dict = dict(zip(words, swahili_words))

# Merging the dicts
swahili_vocab = swahili_numbers_dict | swahili_words_dict

# Creating the labels with the welcome message
welcome =Label(root,text="Welcome to our Swahili Speaking Clock!",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="orange")
swahili_language =Label(root,text="Swahili (or Kiswahili) is a Bantu language,\n spoken primarily in Tanzania, Kenya and Mozambique.",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="peru")
time_system =Label(root,text="It has an interesting time-telling system,\n with 12 day hours (7h-19h) and 12 night hours (20h-6h).",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="peru")
start =Label(root,text="Choose a time zone to start!",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="peru")

# Creating labels for the time in time zone text, time in the Swahili system text and time in Swahili text. The text is added later.
west =Label(root,text="",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="peru")
kenya =Label(root,text="",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="peru")
swahili =Label(root,text="",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="OrangeRed")

# Posiotioning welcome labels
welcome.pack(padx=5, pady=(70, 5),fill=X)
swahili_language.pack(padx=5, pady=10,fill=X)
time_system.pack(padx=5, pady=5,fill=X)
start.pack(padx=5, pady=5,fill=X)

# Function to match Western time to time in Swahili system
def change_time_to_kenya(currentTime):
    currentTime = dict_kenya_time[currentTime]
    return currentTime

# Function that gets the current time, changes it to the chosen time zone and sets the texts in the labels that tell you time in current timezone
# and in the Swahili system
def west_time():
    global minutesInZone, hoursInZone, morning_or_evening, swahili_morning_or_evening
    # Get input from listbox and prettify it
    listbox_value = [listbox.get(i) for i in listbox.curselection()]
    format_time_zone = str(listbox_value).replace("'", "").replace('[', '').replace(']', '')
    # Get time (full, hours and minutes) in the chosen timezone
    time_zone = pytz.timezone(format_time_zone)
    currentTimeInZone = time_zone.localize(datetime.datetime.utcnow())
    currentTimeInZone = currentTimeInZone.replace(tzinfo=pytz.utc)
    currentTimeInZone = currentTimeInZone.astimezone(time_zone)
    currentfullTimeInZone = currentTimeInZone.strftime("%H:%M")
    minutesInZone = currentTimeInZone.strftime("%M")
    hoursInZone = currentTimeInZone.strftime("%H")
    
    # Set whether its in the day time or night time in English and Swahili
    if int(hoursInZone) >= 7 and int(hoursInZone) <= 18:
        morning_or_evening = "in the day time"
        swahili_morning_or_evening = "asubuhi"
    else:
        morning_or_evening = "in the night time"
        swahili_morning_or_evening = "usiku"
    
    # Destroy welcome labels
    swahili.config(text="")
    welcome.destroy()
    swahili_language.destroy()
    time_system.destroy()
    start.destroy()
    
    # Gives the time in the Swahili system
    full_kenya_time = str(change_time_to_kenya(int(hoursInZone))) + ":" + minutesInZone
    
    # Positioning the labels and putting in the text
    west.pack(padx=5, pady=(90,5),fill=X)
    kenya.pack(padx=5, pady=5,fill=X)
    
    west.config(text = f"The time in your chosen timezone {format_time_zone} is {currentfullTimeInZone}.")
    kenya.config(text = f"According to the Swahili system, this would be {full_kenya_time} {morning_or_evening}.")
    
    return minutesInZone, hoursInZone, swahili_morning_or_evening

# Function that translates the time in the Swahili system to Swahili
def swahili_hours():
    global swahilihour
    kenya_time = str(change_time_to_kenya(int(hoursInZone)))
    if int(minutesInZone) < 30:
        if int(kenya_time) <= 10:
            swahilihour = swahili_vocab[int(kenya_time)]
        elif int(kenya_time) > 10:
            # The word for the tens plus "and" and the word for the ones
            swahili_number_1 = swahili_vocab[int(kenya_time[0]) * 10]
            swahili_number_2 = swahili_vocab[int(kenya_time[1])]
            swahilihour = swahili_number_1 + " na " + swahili_number_2
    # If later than 31 minutes past the hour, take the next hour, according to the system, as it is "next hour without some minutes"
    elif int(minutesInZone) >= 31:
        if int(kenya_time) < 10:
            swahilihour = swahili_vocab[int(kenya_time)+1]
        elif int(kenya_time) >= 10:
            kenya_time =  str(int(kenya_time) + 1)
            swahili_number_1 = swahili_vocab[int(kenya_time[0]) * 10]
            swahili_number_2 = swahili_vocab[int(kenya_time[1])]
            number_hours = (int(kenya_time[0]) * 10) + int(kenya_time[1])
            if number_hours < 13:
                swahilihour = swahili_number_1 + " na " + swahili_number_2
            else: 
                # If the hour is 12, the next hour will be 13, which is incorrect. Start counting from 1 again.
                one_hour_ahead = abs(number_hours - (int(kenya_time)+1))
                swahilihour = swahili_vocab[one_hour_ahead]

    return swahilihour


# Function to translate the minutes to Shahili
def swahili_time_complete():
    global swahilitime
    swahili_morning_evening = swahili_morning_or_evening
    minutes = minutesInZone
    swahilihour = swahili_hours()
    if int(minutes) <= 10:
        if int(minutes) == 0:
            swahilitime = f"{swahilihour} {swahili_morning_evening}."
        else:
            swahiliminutes = swahili_vocab[int(minutes)]
            # "na dakika" means "and minute"!
            swahilitime = f"{swahilihour} na dakika {swahiliminutes}."
    # "Quarter" has a special word.
    elif int(minutes) == 15:
        swahiliminutes = swahili_vocab[int(minutes)]
        swahilitime = f"{swahilihour} na {swahiliminutes}."
        
    elif int(minutes) > 10 and int(minutes) < 30:
        # The word for the tens (swahili_number_1), and the word for the ones (swahili_number_2)!
        swahili_number_1 = swahili_vocab[int(minutes[0]) * 10]
        # If it is exactly 10 or 20, we need only the word for the tens.
        if int(minutes[1]) == 0:
            swahiliminutes = swahili_number_1
        else:
            swahili_number_2 = swahili_vocab[int(minutes[1])]
            swahiliminutes = swahili_number_1 + " na " + swahili_number_2
        swahilitime = f"{swahilihour} na dakika {swahiliminutes}."

    # "Half" has a special word.
    elif int(minutes) == 30:
        swahiliminutes = swahili_vocab[int(minutes)]
        swahilitime = f"{swahilihour} na dakika {swahiliminutes}."

    # If we are past 31 minutes past the hour, we use "kasoro" meaning without.
    elif int(minutes) >= 31:
        minutes = str(60 - int(minutes))
        if int(minutes) <= 10:
            swahiliminutes = swahili_vocab[int(minutes)]
            swahilitime = f"{swahilihour} kasoro dakika {swahiliminutes}."

        elif int(minutes) == 15:
            swahiliminutes = swahili_vocab[int(minutes)]
            swahilitime = f"{swahilihour} kasoro {swahiliminutes}."

        elif int(minutes) > 10 and int(minutes) < 30:
            swahili_number_1 = swahili_vocab[int(minutes[0]) * 10]
            if int(minutes[1]) == 0:
                swahiliminutes = swahili_number_1
            else:
                swahili_number_2 = swahili_vocab[int(minutes[1])]
                swahiliminutes = swahili_number_1 + " na " + swahili_number_2
            swahilitime = f"{swahilihour} kasoro dakika {swahiliminutes}."

    # Position the Swahili translation label and add the text.
    swahili.pack(padx=5, pady=5,fill=X)
    swahili.config(font=("Ariel",12,"bold"), text = f"The translation is:\n Saa {swahilitime}")

    return swahilitime


#Create a trutle window to draw the clock.
wn = turtle.Screen()
pen = turtle.Turtle()
wn.bgcolor("linen")
wn.setup(width=600, height=600)

# Function to draw the clock.
def draw_clock():
    # Set background according to time of day.
    if int(hoursInZone) >= 7 and int(hoursInZone) <= 18:
        wn.bgpic("day.png")
    else:
        wn.bgpic("night.png")
    wn.setup(width=600, height=600)
    wn.title("Clock")

    # Set pensise.
    pen.hideturtle()
    pen.speed(0)
    pen.pensize(3)

    #Draw circle.
    pen.up()  
    pen.goto(0,210)
    pen.setheading(180)
    pen.fillcolor("linen")
    pen.down()
    pen.begin_fill()
    pen.circle(210)
    pen.end_fill()

    #Draw another circle
    pen.up()
    pen.goto(0,210)
    pen.setheading(180)
    pen.color("PeachPuff3")
    pen.pendown()
    pen.circle(210)

    pen.penup()
    pen.goto(0,0)
    pen.setheading(90)

    #Draw the notches for the hours.
    for _ in range(13):
        pen.fd(190)
        pen.pendown()
        pen.fd(20)
        pen.penup()
        pen.color("peru")
        pen.goto(0,0)
        pen.rt(30)

    #Draw the hours arm based on the hour in current time zone!
    pen.penup()
    pen.goto(0,0)
    pen.color("orange3")
    pen.setheading(90)
    angle = (int(hoursInZone) / 12) * 360
    pen.rt(angle)
    pen.pendown()
    pen.fd(100)

    #Draw the minutes arm. 
    pen.penup()
    pen.goto(0,0)
    pen.color("orange4")
    pen.setheading(90)
    angle = (int(minutesInZone) / 60) * 360
    pen.rt(angle)
    pen.pendown()
    pen.fd(150)

    #End the possibility for events in the turtle window.
    wn.mainloop()

# Function to play the audio!
def play_audio():
    kiswahilitime = "Saa " + swahilitime
    # Using abspath to avoid issues with path names in diff systems
    path = os.path.abspath("audios")
    list_of_file_names = []
    list_of_files = []

    for filename in glob.glob(os.path.join(path, '*.wav')):
        # Append the names of the audio files to the list. All used Swahili words have a corresponding audio, named the word itself.
        abspath = os.path.abspath(filename)
        sr, data = wavfile.read(abspath)
        filename = os.path.split(abspath)[-1]
        filename = filename.replace(".wav", "")
        list_of_file_names.append(filename)
        # Append the first channel of the audio files to a list.
        filename = data[:, 0]
        list_of_files.append(filename)

    # Zip the lists tp create an audio dictionary, where the keys are the words (from the file names) and the values the files.
    audio_dictionary = dict(zip(list_of_file_names, list_of_files))

    # From the translation of the time to Swahili, get all the words (in lowercase).
    kiswahilitime = kiswahilitime.lower()
    kiswahilitime = kiswahilitime.replace(".", "")
    list_of_words = kiswahilitime.split()

    # Read the audio file for each wors and concatenate
    tell_time = [audio_dictionary["saa"][0]] # Set the datatype of the array with one element of the audio arrays which is int16.
    for word in list_of_words:
        tell_time = np.concatenate((tell_time, audio_dictionary[word]))

    #Play the concatenated audio!
    sd.play(tell_time, sr)


 # Position all the buttons and set which functions to execute when clicking on them.
play_button = tk.Button(root, text="Tell me the time", bg="PeachPuff", width=20, command=play_audio).pack(pady=(20, 50), side = BOTTOM)

clock = tk.Button(root, text="Draw clock", bg="PeachPuff", width=20, command=draw_clock).pack(pady=20, side = BOTTOM)

translate = tk.Button(root, text="Translate to Swahili", bg="PeachPuff", width=20, command=swahili_time_complete).pack(pady=20, side = BOTTOM)

chosen_time_zone = tk.Button(root, text="Show time in zone", bg="PeachPuff", width=20, command=west_time).pack(pady=(5, 20), side = BOTTOM)

# Close of possibilities for events in main window.
root.mainloop()
