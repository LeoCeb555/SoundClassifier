import serial
import sqlite3
import threading # non-blocking input
import time # CPU optimization for multi-threading
import queue # IPC
import os # terminal commands

# Helper functions
def get_input(queue): # thread 2 function
    while True:
        user_input = input()
        queue.put(user_input)

def get_notification(): # thread 3 function
    while True:
        if(ser2.in_waiting > 0):
            line = ser2.readline()
            line = line.decode('utf-8')
            print(line) # notify user about event

        time.sleep(0.01) # give cpu a break

def clear_terminal():
    # 'nt' is for Windows, 'posix' is for Mac and Linux
    os.system('cls' if os.name == 'nt' else 'clear')

# Setup USART ports
ser2 = serial.Serial('/dev/cu.usbmodem14203', 115200, timeout=1)
ser3 = serial.Serial('/dev/cu.usbserial-0001', 115200, timeout=1)

# Determine what table and label will be used
sound = input("What sound are you recording? ")

while(sound.lower() != "snap" and
      sound.lower() != "clap" and
      sound.lower() != "door" and
      sound.lower() != "sink" and
      sound.lower() != "whistle" and
      sound.lower() != "bell"):
    sound = input("Invalid sound - please try again: ")

clear_terminal()

# Setup and start helper threads
input_queue = queue.Queue()
input_thread = threading.Thread(target=get_input, args=(input_queue,), daemon=True)
input_thread.start()

notification_thread = threading.Thread(target=get_notification, daemon=True)
notification_thread.start()

if ser2.is_open and ser3.is_open:
    print(f"Connected to: {ser2.port} and {ser3.port}")
    connection = sqlite3.connect("/Users/vivianacebrero/Documents/UCI/Research/SoundClassifier/SQL/sound_data.db") # open local database to organize recieved data
    cursor = connection.cursor()

    while True:

        if not input_queue.empty(): # break loop without blocking it
            data = input_queue.get()
            if data.lower() == "q":
                break

        if(ser3.in_waiting > 0): # process raw data into database

            line = ser3.readline()
            line = line.decode('utf-8')
            features = line.replace("\r\n", "").split(",", 5) # clean up data
            print(f"Features: {features}")
            
            cursor.execute(f"""INSERT INTO {sound}_feature_table(
                           energy,
                           zcr,
                           peak,
                           dominant_frequency,
                           spectral_centroid,
                           spectral_bandwidth,
                           label)
                        VALUES(
                        {features[0]},
                        {features[1]},
                        {features[2]},
                        {features[3]},
                        {features[4]},
                        {features[5]},
                        '{sound}')""")
            connection.commit() # save changes to database
            print(f"\nSucessfully inserted into {sound}_feature_table. Row ID: {cursor.lastrowid}\n")
        
        time.sleep(0.01)

connection.close()