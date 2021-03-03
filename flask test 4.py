
from flask import Flask, render_template
from flask import request
import time
import datetime
import sched
import json
from datetime import datetime
import requests
from subprocess import call
import logging



app = Flask(__name__)


# Scheduler creation
# Alarm up to 20s of delay due to page refresh
s = sched.scheduler(time.time, time.sleep)


def print_alarm():
    """
    :return: the alarm rings + print info in cmd
    """
    # create logging file + function
    logging.basicConfig(filename='test.log', level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    s.run(blocking=False)
    logging.debug("Your alarm is ringing")
    notifications = []
    alarm_time = request.args.get("alarm")
    alarm_name = request.args.get("name")
    alarm_entry = alarm_time , alarm_name
    notifications.append(alarm_entry)

    # NEWS FUNCTION FOR READING NEWS DURING ALARM
    # Explained in /calendar
    with open('config.json') as json_file:
        data = json.load(json_file)
        for p in data['API']:
            api1 = p['news']
            api1 = str(api1)
            main_url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=" + api1
    open_bbc_page = requests.get(main_url).json()
    article = open_bbc_page["articles"]
    results = []
    for ar in article:
        results.append(ar["title"])
    for i in range(4):
        news_results = results[0] + "\n" + results[1] + "\n" + results[2] + "\n" + results[3]

    # WEATHER FUNCTION FOR READING WEATHER DURING ALARM
    # Explained in /calendar
    with open('config.json') as json_file:
        data = json.load(json_file)
        for p in data['API']:
            api2 = p['weather']
            api2 = str(api2)
            url = 'http://api.openweathermap.org/data/2.5/weather?q=Exeter&appid=' + api2 + '&units=metric'
    res = requests.get(url)
    data = res.json()
    temp = data['main']['temp']
    description = data['weather'][0]['description']
    # Workaround for pyttsx3 not working with flask
    phrase = "Your alarm is ringing! The news for today are:" + format(results[0]) +"also we have" + format(results[1]) + "and finally" + format(results[2]) \
             + "The weather for today in Exeter is:" + format(description) + "And the temperature is" + format(temp) + "degrees celcius"
    # call function to speak the info in phrase
    call(["python3", "speak.py", phrase])




@app.route('/', methods=['POST', 'GET'])
def schedule_event():
    """
    Fonction to schedule the alarms
    :return: Info about the alarm and delay + renders template
    """
    # create variable to know if want alarm to repeat
    repeat = request.args.get("checkbox")
    # create logging file + function
    logging.basicConfig(filename='test.log', level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    s.run(blocking=False)
    # Gets input from user, adds it to variable
    alarm_time = request.args.get("alarm")
    alarm_name = request.args.get("name")

    logging.debug( "The alarm time is:" + str(alarm_time))
    # Add alarm list to JSON file
    data = {}
    data['Alarms'] = [alarm_time , alarm_name]

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

   # Setting alarm
    if alarm_time:
        # Convert alarm_time to a delay + print info in cmd
        time_in_string = alarm_time
        time_in_datetime = datetime.strptime(time_in_string, "%Y-%m-%dT%H:%M")
        epoch_time = (time_in_datetime - datetime(1970, 1, 1)).total_seconds()
        current_time = time.time()
        delay = epoch_time - current_time
        logging.debug("The ecpoch time is:" + str(epoch_time))
        logging.debug("The courrent time is" + str(current_time))
        logging.debug("The created delay is" + str(delay))
        # After delay, run print_alarm function
        s.enter(int(delay), 1, print_alarm)
        if repeat != "None":
            s.enter(int(86400), 1, print_alarm)
            logging.debug("The alarms is set for next day")
    return render_template("clock.html")




@app.route('/calendar')
def news_api():
    """
    News fonction with hidden API
    :return: info about the news + renders template
    """
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
        news_results = results[0] + "\n" + results[1] + "\n" + results[2] + "\n" + results[3]
    # render the template for the webpage + adds news data
    return render_template("calendar.html", news_data = news_results)


def weather_api():
    """
    Weather fonction with hidden API
    :return: the weather information + render the template
    """
    # Getting info with hidden API in config file
    with open('config.json') as json_file:
        data = json.load(json_file)
        for p in data['API']:
            api2 = p['weather']
            api2 = str(api2)
            url = 'http://api.openweathermap.org/data/2.5/weather?q=Exeter&appid=' + api2 + '&units=metric'
    res = requests.get(url)
    data = res.json()
    # getting data from json into variables
    temp = data['main']['temp']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['description']
    weather_results = str(temp) + "\n" + str(description)
    # render the template for the webpage + adds weather data
    return render_template("calendar.html", weather_data = weather_results)




@app.route('/alarms')
def next_alarm():
    """
    :return: info about next alarms
    """
    # open json file with next alarms data
    with open('data.json') as json_file:
        alarm_data = json.load(json_file)
    # Render template and paste it in html file
    return render_template("alarms.html", next_alarms = alarm_data )




if __name__ == "__main__":
    app.run(debug=True)
