import sched, time, datetime
import pyttsx3
import requests
import sys
import threading
import queue
import os
import json
from flask import Flask
from flask import request, render_template

app = Flask(__name__)

@app.route("/")

def restart_program():
    """
    Restarts the current program.
    """
    python = sys.executable
    os.execl(python, python, * sys.argv)

def print_alarm():
    """
    :return: Rings the alarl at the given time
    """
    print("Alarm is ringing!!!: {}".format(datetime.datetime.now()))
    engine = pyttsx3.init()
    engine.say("RING! RING! Time to WakeUp")
    engine.runAndWait()


def weather_api():
    """
    :return: Weather info
    """
    import requests
    from pprint import pprint
    # Getting info with hidden API in config file
    with open('config.json') as json_file:
        data = json.load(json_file)
        for p in data['API']:
            api2 = p['weather']
            api2 = str(api2)

            url = 'http://api.openweathermap.org/data/2.5/weather?q=Exeter&appid=' + api2 + '&units=metric'


    res = requests.get(url)

    data = res.json()

    temp = data['main']['temp']
    wind_speed = data['wind']['speed']

    description = data['weather'][0]['description']
    # Data
    print('Temperature in Exeter : {} degree celcius'.format(temp))
    # Voice
    engine = pyttsx3.init()
    engine.say("Temperature in Exeter")
    engine.say(format(temp))
    engine.say("degres")
    # Data
    print('Wind Speed in Exeter : {} m/s'.format(wind_speed))
    # Voice
    engine.say("Wind speeds in exeter")
    engine.say(format(wind_speed))
    engine.say("meters per hour")
    # Data
    print('Description : {}'.format(description))
    # Voice
    engine.say("It is")
    engine.say(format(description))
    # End Voice
    engine.runAndWait()


def news_api():
    # BBC news api hidden in config file
    with open('config.json') as json_file:
        data = json.load(json_file)
        for p in data['API']:
            api1 = p['news']
            api1 = str(api1)
            main_url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=" + api1

      # fetching data
    open_bbc_page = requests.get(main_url).json()

      # getting all articles in a string article
    article = open_bbc_page["articles"]

    # empty list which  contain all trending news

    results = []

    for ar in article:
          results.append(ar["title"])

    for i in range(4):
         # printing all trending news
         print(i + 1, results[i])

    # Voice for the first 4 results
    engine = pyttsx3.init()
    engine.say("Here are the most relevant news for today")
    engine.say(format(results[0]))
    engine.say(format(results[1]))
    engine.say(format(results[2]))
    engine.say(format(results[3]))
    engine.runAndWait()




# ask time for alarm--------------------------------

t1 = int(input("YEAR:"))
t2 = int(input("Month:"))
t3 = int(input("Day:"))
t4 = int(input("Hour:"))
t5 = int(input("Min:"))




# Creating variable-----------------------------------

alarma = datetime.datetime(t1,t2,t3,t4,t5).timestamp()


# making scheduler------------------------------------

s = sched.scheduler(time.time)
x1 = s.enterabs(alarma, 1, print_alarm)
x2 = s.enterabs(alarma, 2, weather_api)
x3 = s.enterabs(alarma, 3, news_api)

print("Waiting alarm...")

# User choices----------------------------------------

def console(q):
    while 1:
        cmd = input('> ')
        q.put(cmd)
        if cmd == '2':
            break

def cancel_alarm():
    print('--> Cancelling alarms')
    s.cancel(x1)
    s.cancel(x2)
    s.cancel(x3)
    print('--> No alarms pending')
    print("Press 2 to end the program")



def add_alarm():
   print("")

def invalid_input():
    print('---> Unknown command')

def main():
    cmd_actions = {'1': cancel_alarm, '3': add_alarm}
    cmd_queue = queue.Queue()
    print("Select 1 to cancel alarm")
    print("Select 2 to quit an continue with the program")


    dj = threading.Thread(target=console, args=(cmd_queue,))
    dj.start()

    while 1:
        cmd = cmd_queue.get()
        if cmd == '2':
            break
        action = cmd_actions.get(cmd, invalid_input)
        action()

main()
s.run()


# Prompt user new alarm-------------------------------

print("looks like you don't have any alarm")
def add_alarm():
   print("Okay")
   answer = input("Do you really want to add an alarm? ")
   if answer.lower().strip() in "y yes".split():
       restart_program()

def invalid_input():
    print('---> Unknown command')

def main():
    cmd_actions = {'1': add_alarm}
    cmd_queue = queue.Queue()
    print("Select 1 add an alarm")

    dj = threading.Thread(target=console, args=(cmd_queue,))
    dj.start()

    while 1:
        cmd = cmd_queue.get()
        if cmd == '2':
            break
        action = cmd_actions.get(cmd, invalid_input)
        action()

main()



