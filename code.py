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
  
# Creating a Listbox and
# attaching it to root window
listbox = Listbox(root)
  
# Adding Listbox to the left
# side of root window
listbox.pack(side = LEFT, fill = BOTH)
  
# Creating a Scrollbar and 
# attaching it to root window
scrollbar = Scrollbar(root)
  
# Adding Scrollbar to the right
# side of root window
scrollbar.pack(side = RIGHT, fill = BOTH)

zons = pytz.common_timezones
  
# Insert elements into the listbox
for values in zons:
    listbox.insert(END, values)
      
# Attaching Listbox to Scrollbar
# Since we need to have a vertical 
# scroll we use yscrollcommand
listbox.config(yscrollcommand = scrollbar.set, background="linen", foreground="black")

# setting scrollbar command parameter 
# to listbox.yview method its yview because
# we need to have a vertical view
scrollbar.config(command = listbox.yview)

westhours = [*range(7, 20, 1)] + [20,21,22,23,0,1,2,3,4,5,6]
kenyahours = [*range(1,13,1)] + [*range(1,13,1)]
dict_kenya_time = dict(zip(westhours,kenyahours))

swahili_numbers = ["moja", "mbili", "tatu", "nne", "tano", "sita", "saba", "nane", "tisa", "kumi"]
numbers = [*range(1,11,1)]
swahili_numbers_dict = dict(zip(numbers, swahili_numbers))

swahili_words = ["dakika", "ishirini", "arobaini", "hamsini", "robo", "nusu", "na", "kasoro", "alasiri", "asubuhi", "jioni", "usiku", "mchana", "saa"]
words = ["minute", 20, 40, 50, 15, 30, "and", "without", "afternoon", "morning", "evening", "night", "daytime", "hour"]
swahili_words_dict = dict(zip(words, swahili_words))

swahili_vocab = swahili_numbers_dict | swahili_words_dict

welcome =Label(root,text="Welcome to our Swahili Speaking Clock!",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="orange")
swahili_language =Label(root,text="Swahili (or Kiswahili) is a Bantu language,\n spoken primarily in Tanzania, Kenya and Mozambique.",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="peru")
time_system =Label(root,text="It has an interesting time-telling system,\n with 12 day hours (7h-19h) and 12 night hours (20h-6h).",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="peru")
start =Label(root,text="Choose a time zone to start!",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="peru")

west =Label(root,text="",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="peru")
kenya =Label(root,text="",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="peru")
swahili =Label(root,text="",bd=9, relief="flat",
    font=("Ariel",12,"bold"),bg="linen",fg="OrangeRed")

welcome.pack(padx=5, pady=(70, 5),fill=X)
swahili_language.pack(padx=5, pady=10,fill=X)
time_system.pack(padx=5, pady=5,fill=X)
start.pack(padx=5, pady=5,fill=X)

def change_time_to_kenya(currentTime):
    currentTime = dict_kenya_time[currentTime]
    return currentTime

# Function for printing the
# selected listbox value(s)
def west_time():
    global minutesInZone, hoursInZone, morning_or_evening, swahili_morning_or_evening
    listbox_value = [listbox.get(i) for i in listbox.curselection()]
    format_time_zone = str(listbox_value).replace("'", "").replace('[', '').replace(']', '')
    time_zone = pytz.timezone(format_time_zone)
    currentTimeInZone = time_zone.localize(datetime.datetime.utcnow())
    currentTimeInZone = currentTimeInZone.replace(tzinfo=pytz.utc)
    currentTimeInZone = currentTimeInZone.astimezone(time_zone)
    currentfullTimeInZone = currentTimeInZone.strftime("%H:%M")
    minutesInZone = currentTimeInZone.strftime("%M")
    hoursInZone = currentTimeInZone.strftime("%H")
    
    if int(hoursInZone) >= 7 and int(hoursInZone) <= 18:
        morning_or_evening = "in the day time"
        swahili_morning_or_evening = "asubuhi"
    else:
        morning_or_evening = "in the night time"
        swahili_morning_or_evening = "usiku"
    
    swahili.config(text="")
    welcome.destroy()
    swahili_language.destroy()
    time_system.destroy()
    start.destroy()

    full_kenya_time = str(change_time_to_kenya(int(hoursInZone))) + ":" + minutesInZone
    
    west.pack(padx=5, pady=(90,5),fill=X)
    kenya.pack(padx=5, pady=5,fill=X)
    
    west.config(text = f"The time in your chosen timezone {format_time_zone} is {currentfullTimeInZone}.")
    kenya.config(text = f"In Swahili, this would be {full_kenya_time} {morning_or_evening}.")
    
    return minutesInZone, hoursInZone, swahili_morning_or_evening


def swahili_hours():
    global swahilihour
    kenya_time = str(change_time_to_kenya(int(hoursInZone)))
    if int(minutesInZone) < 30:
        if int(kenya_time) <= 10:
            swahilihour = swahili_vocab[int(kenya_time)]
        elif int(kenya_time) > 10:
            swahili_number_1 = swahili_vocab[int(kenya_time[0]) * 10]
            swahili_number_2 = swahili_vocab[int(kenya_time[1])]
            swahilihour = swahili_number_1 + " na " + swahili_number_2
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
                one_hour_ahead = abs(number_hours - (int(kenya_time)+1))
                swahilihour = swahili_vocab[one_hour_ahead]

    return swahilihour


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
            swahilitime = f"{swahilihour} na dakika {swahiliminutes}."

    elif int(minutes) == 15:
        swahiliminutes = swahili_vocab[int(minutes)]
        swahilitime = f"{swahilihour} na {swahiliminutes}."
        
    elif int(minutes) > 10 and int(minutes) < 30:
        swahili_number_1 = swahili_vocab[int(minutes[0]) * 10]
        if int(minutes[1]) == 0:
            swahiliminutes = swahili_number_1
        else:
            swahili_number_2 = swahili_vocab[int(minutes[1])]
            swahiliminutes = swahili_number_1 + " na " + swahili_number_2
        swahilitime = f"{swahilihour} na dakika {swahiliminutes}."

    elif int(minutes) == 30:
        swahiliminutes = swahili_vocab[int(minutes)]
        swahilitime = f"{swahilihour} na dakika {swahiliminutes}."

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

    swahili.pack(padx=5, pady=5,fill=X)
    swahili.config(font=("Ariel",12,"bold"), text = f"The translation is:\n Saa {swahilitime}")

    return swahilitime


wn = turtle.Screen()
pen = turtle.Turtle()
wn.bgcolor("linen")
wn.setup(width=600, height=600)

def draw_clock():
    if int(hoursInZone) >= 7 and int(hoursInZone) <= 18:
        wn.bgpic("day.png")
    else:
        wn.bgpic("night.png")
    wn.setup(width=600, height=600)
    wn.title("Clock")

    pen.hideturtle()
    pen.speed(0)
    pen.pensize(3)

    pen.up()  
    pen.goto(0,210)
    pen.setheading(180)
    pen.fillcolor("linen")
    pen.down()
    pen.begin_fill()
    pen.circle(210)
    pen.end_fill()

    pen.up()
    pen.goto(0,210)
    pen.setheading(180)
    pen.color("PeachPuff3")
    pen.pendown()
    pen.circle(210)

    pen.penup()
    pen.goto(0,0)
    pen.setheading(90)

    for _ in range(13):
        pen.fd(190)
        pen.pendown()
        pen.fd(20)
        pen.penup()
        pen.color("peru")
        pen.goto(0,0)
        pen.rt(30)

    pen.penup()
    pen.goto(0,0)
    pen.color("orange3")
    pen.setheading(90)
    angle = (int(hoursInZone) / 12) * 360
    pen.rt(angle)
    pen.pendown()
    pen.fd(100)

    pen.penup()
    pen.goto(0,0)
    pen.color("orange4")
    pen.setheading(90)
    angle = (int(minutesInZone) / 60) * 360
    pen.rt(angle)
    pen.pendown()
    pen.fd(150)

    wn.mainloop()

def play_audio():
    kiswahilitime = "Saa " + swahilitime
    path = os.path.abspath("audios")
    list_of_file_names = []
    list_of_files = []

    for filename in glob.glob(os.path.join(path, '*.wav')):
        abspath = os.path.abspath(filename)
        sr, data = wavfile.read(abspath)
        filename = os.path.split(abspath)[-1]
        filename = filename.replace(".wav", "")
        list_of_file_names.append(filename)
        filename = data[:, 0]
        list_of_files.append(filename)

    audio_dictionary = dict(zip(list_of_file_names, list_of_files))

    kiswahilitime = kiswahilitime.lower()
    kiswahilitime = kiswahilitime.replace(".", "")
    list_of_words = kiswahilitime.split()

    tell_time = [audio_dictionary["saa"][0]]
    for word in list_of_words:
        tell_time = np.concatenate((tell_time, audio_dictionary[word]))


    sd.play(tell_time, sr)


 
play_button = tk.Button(root, text="Tell me the time", bg="PeachPuff", width=20, command=play_audio).pack(pady=(20, 50), side = BOTTOM)

clock = tk.Button(root, text="Draw clock", bg="PeachPuff", width=20, command=draw_clock).pack(pady=20, side = BOTTOM)

translate = tk.Button(root, text="Translate to Swahili", bg="PeachPuff", width=20, command=swahili_time_complete).pack(pady=20, side = BOTTOM)

chosen_time_zone = tk.Button(root, text="Show time in zone", bg="PeachPuff", width=20, command=west_time).pack(pady=(5, 20), side = BOTTOM)

root.mainloop()
