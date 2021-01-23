import os
import threading
import logging
import sched
import time
import flask
from flask import Flask, render_template, request, redirect, url_for
import pyttsx3
import license

mit = license.find("MIT")

from functions import create_alarm, bbc_news, announcements_alarm, notifications_covid

app = Flask(__name__)
logging.basicConfig(
    filename="alarm.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)

# The global variables that we need, returning lists of values.
covid_list = []
list_of_alarms = []


@app.route("/create", methods=["GET", "POST"])
def handle_data():
    """
    Upon submitting a alarm form request, this function applies and
    validates the necessary data in order to create an adequate
    alarm with conditions specified by user.

    :return: Redirect - main_route.
    """

    if flask.request.method == "POST":

        clock_name = request.form["clockname"]
        date_time = request.form["date_time"]

        # We make sure that a date is given so that an alarm could be created.
        if not date_time:
            new_engine = pyttsx3.init()
            new_engine.say("Alarm can not be created")
            new_engine.runAndWait()
            logging.warning("No date time input - Alarm could not be created.")
        else:
            try:
                weather_briefing = request.form["weather"]
            except:
                weather_briefing = "off"
            try:
                news_briefing = request.form["brefingsname"]
            except:
                news_briefing = "off"

            year = int(date_time[0:4])
            month = int(date_time[5:7])
            day = int(date_time[8:10])
            hour = int(date_time[11:13])
            minute = int(date_time[14:16])
            total_time = create_alarm(year, month, day, hour, minute)
            initialise_alarm(total_time, clock_name, news_briefing, weather_briefing)

            # We make sure the alarm is not set in the past.
            if total_time > 0:
                if not clock_name:
                    if minute < 10:
                        list_of_alarms.append(
                            "Date:"
                            + str(day)
                            + "/"
                            + str(month)
                            + "/"
                            + str(year)
                            + " "
                            + "Time:"
                            + str(hour)
                            + ":"
                            + "0"
                            + str(minute)
                        )
                    else:
                        list_of_alarms.append(
                            "Date:"
                            + str(day)
                            + "/"
                            + str(month)
                            + "/"
                            + str(year)
                            + " "
                            + "Time:"
                            + str(hour)
                            + ":"
                            + str(minute)
                        )

                else:
                    if minute < 10:
                        list_of_alarms.append(
                            "Alarm name:"
                            + clock_name
                            + " "
                            + "Date:"
                            + str(day)
                            + "/"
                            + str(month)
                            + "/"
                            + str(year)
                            + " "
                            + "Time:"
                            + str(hour)
                            + ":"
                            + "0"
                            + str(minute)
                        )
                    else:
                        list_of_alarms.append(
                            "Alarm name:"
                            + clock_name
                            + " "
                            + "Date:"
                            + str(day)
                            + "/"
                            + str(month)
                            + "/"
                            + str(year)
                            + " "
                            + "Time:"
                            + str(hour)
                            + ":"
                            + str(minute)
                        )

    return redirect(url_for("main_route"))


@app.route("/")
def main_route():
    """
        Main route.

    :return: None
    """
    return render_template(
        "alarm.html", covid_list=covid_list, list_of_alarms=list_of_alarms
    )


def initialise_alarm(total_time: float, alarm_name: str, is_news: str, is_weather: str):
    """

    :param total_time: float - total_time
    :param alarm_name: str - alarm_name
    :param is_news: str - is_news
    :param is_weather: str - is_weather
    :return: None
    """

    scheduler = sched.scheduler(time.time, time.sleep)

    def print_event(name: str, display_news: str, display_weather: str):
        """
        This function is going to trigger the alarm.

        :param name: str - name
        :param display_news:  str - display_news
        :param display_weather: str -display_weather
        :return: None
        """

        print("EVENT:", time.time(), name)
        to_say = "Alarm: " + name + ", has triggered. "
        new_engine = pyttsx3.init()

        covid_list.append(notifications_covid())

        # We make sure that the checkbox for news and weather.
        if display_news == "on":
            to_say = bbc_news(to_say)

        if display_weather == "on":
            to_say = announcements_alarm(to_say)
        new_engine.say(to_say)
        new_engine.runAndWait()

    print("START:", time.time())

    if total_time > 0:
        event = scheduler.enter(
            total_time,
            1,
            print_event,
            (
                alarm_name,
                is_news,
                is_weather,
            ),
        )
    else:
        new_engine = pyttsx3.init()
        new_engine.say("Alarm can not be created")
        new_engine.runAndWait()
        logging.warning(
            "Alarm can not be created in the past - Alarm could not be created."
        )

    threading.Thread(target=scheduler.run).start()


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
