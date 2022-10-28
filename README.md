# Speaking Swahili Clock⏰🦁
A program with interactive interface that lets you choose a time zone, shows you the current time in the chosen time zone in Swahili and reads it out for you!

### Swahili time-telling system🌄🌠
Swahilian time begins when the sun rises. The days are divided in two cycles of 12 hours, one during the day and one during the night. This means that when the clock hits 7 a.m., it is 1 in the morning in Swahili, _saa moja_ (hour one). At 7 o’clock in the evening the sun will be down, meaning that it is 1 in the night in Swahilitime. 

In the first 30 minutes of an hour, you say the time simply by combining the current hour and minutes. So 8:26 in the morning would be "_saa mbili na dakika ishirini na sita_" (hour two and minute twenty and six). There is a special word for "quarter", so 9:15 would be "_saa tatu na robo_" (hour three and a quarter). Similarly, the special word for "half an hour" is "nusu" and therefore 9:30 would be "_saa tatu na nusu_" (hour three and half). 

If it has been over 30 minutes in the hour, the time will be read as a statement of subtraction from the coming hour. For example, 7:40 will be "_saa mbili kasoro dakika ishirini_" (hour two without minute twenty). The same goes if there are 15 minutes to an hour: 9:45 will be "_saa nne kasoro robo_"(hour four without a quarter). To indicate if the time is during the day or during the night, the sentence will end with specifying it. "_Asubuhi_" means "during the daytime" and "_usiku_" - "during the night time. This is normally specified only when it is a round hour, but it can be added for explicitness if needed. 

To put it all together, 10:27 a.m. would look like this: "_saa nne na dakika ishirini na saba mchana_" (hour four and minute twenty and seven morning).

### Repository contents
The repository contains folder "audios" that includes the .wav files the programme uses. They were scraped from https://www.spokenswahili.com/blog/telling-the-time-in-swahili/.

The .png files in the repository are used as background for the clock window.

### How to run
Within the terminal, move to the root directory, where the requirements file is located. With the command ``pip install -r requirements.txt`` you can install all necessary packages to run the code. In case you get a tkinter ImportError, please refer to: https://tkdocs.com/tutorial/install.html. Next, run the file code.py from the root directory with the command ``python code.py``.

Two windows open when the command is executed. The main window contains the welcome text and the control buttons. The other is where you can have a clock showing the current time in your timezone. 

To start, choose a timezone from the scrollable listbox and confirm it with button "Show time in zone". The current time in the timezone will be displayed. To see translation to Swahili, press "Translate to Swahili". Please make sure to press the buttons in this order! To draw the clock - press "Draw clock". Its background will depend on whether it is daytime or nightime. Once close, this window does not open again, unless you execute the code again. Finally, to have the program pronounce the time, press "Tell me the time"!

To start again with a new timezone, just choose a new timezone and press "Show time in zone" and any other feature buttons again!
