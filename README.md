# Speaking Swahili Clock⏰🦁
A program with interactive interface that lets you choose a time zone, shows you the current time in the chosen time zone in Swahili and reads it out for you!

The repository contains folder "audios" that includes the .wav files the programme uses. They were scraped from https://www.spokenswahili.com/blog/telling-the-time-in-swahili/.

The .png files in the repository are used as background for the clock window.

Within the terminal, move to the root directory, where the requirements file is located. With the command ``pip install -r requirements.txt`` you can install all necessary packages to run the code. In case you get a tkinter ImportError, please refer to: https://tkdocs.com/tutorial/install.html. Next, run the file code.py from the root directory with the command ``python code.py``.

Two windows open when the command is executed. The main window contains the welcome text and the control buttons. The other is where you can have a clock showing the current time in your timezone. 

To start, choose a timezone from the scrollable listbox and confirm it with button "Show time in zone". The current time in the timezone will be displayed. To see translation to Swahili, press "Translate to Swahili". Please make sure to press the buttons in this order! To draw the clock - press "Draw clock". Its background will depend on whether it is daytime or nightime. Once close, this window does not open again, unless you execute the code again. Finally, to have the program pronounce the time, press "Tell me the time"!

To start again with a new timezone, just choose a new timezone and press "Show time in zone" and any other feature buttons again!
