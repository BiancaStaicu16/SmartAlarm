import time
from datetime import datetime, timezone, date
import json
import requests


def notifications_covid() -> str:
    """
    This function provides the needed information for the covid briefing.

    :return: str - string to say
    """

    # The url is a public one.
    url = (
        "https://api.coronavirus.data.gov.uk/v1/data?"
        "filters=areaType=nation;areaName=england&"
        'structure={"date":"date","newCases":"newCasesByPublishDate", '
        '"newDeathsByDeathDate":"newDeathsByDeathDate"}'
    )
    response = requests.get(url)
    covid_data = response.json()

    return handle_covid_response(covid_data)


def handle_covid_response(covid_data: dict) -> str:
    """

    :param covid_data: dict - covid_data
    :return: str - add_to_covid
    """

    today = date.today()
    today_date = today.strftime("%Y-%m-%d")
    add_to_covid = ""

    for item in covid_data["data"]:
        if item["date"] == today_date:
            add_to_covid = (
                add_to_covid
                + "The new cases of Covid19 from today are: "
                + str(item["newCases"])
                + " "
            )

    # Loop through data to find covid information.
    for item in covid_data["data"]:
        if item["date"] == today_date:
            if item["newDeathsByDeathDate"] is None:
                add_to_covid = add_to_covid + "The number of Covid19 deaths today: 0"
            else:
                add_to_covid = (
                    add_to_covid
                    + "The number of Covid19 deaths today: "
                    + str(item["newDeathsByDeathDate"])
                )

    return add_to_covid


with open("config.json", "r") as f:

    # Open config.json file.
    data = json.load(f)


def announcements_alarm(to_say: str) -> str:
    """
    This function provides the needed information for the weather briefing.

    :param to_say: str - to_say
    :return: str - string to say
    """
    api_key = data["api_key1"]
    base_url = "api.openweathermap.org/data/2.5/weather?q="
    city_name = "chicago"
    complete_url = "http://" + base_url + city_name + "&appid=" + api_key

    # We have the complete url.
    # We are going to extract the information.
    response = requests.get(complete_url)
    weather_response = response.json()

    return handle_weather_response(weather_response, to_say)


def handle_weather_response(weather_response: dict, to_say: str) ->str:
    """

    :param weather_response: dict - weather_response
    :param to_say: str - to_say
    :return: str - to_say
    """

    # The if statement checks the website status.
    if weather_response["cod"] != "404":
        all_weather_responses = weather_response["main"]
        current_temperature = all_weather_responses["temp"]
        current_pressure = all_weather_responses["pressure"]
        current_humidiy = all_weather_responses["humidity"]
        weather_response2 = weather_response["weather"]
        weather_description = weather_response2[0]["description"]
        to_say = to_say + "The weather for today is: "

        # We were interested in having the temperature, pressure and humidity news.
        to_say = to_say + (
            " Temperature (in kelvin unit) = "
            + str(current_temperature)
            + "\n atmospheric pressure (in hPa unit) = "
            + str(current_pressure)
            + "\n humidity (in percentage) = "
            + str(current_humidiy)
            + "\n description = "
            + str(weather_description)
        )
    else:
        pass

    return to_say


def bbc_news(to_say: str) -> str:
    """
    This function provides the needed information for the news briefing.

    :param to_say: str - to_say
    :return: str - to say
    """
    api_key2 = data["api_key2"]
    url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey="
    final_url = url + api_key2

    # Now that we have the final url, we can extract the pieces of information that we need.
    open_bbc_page = requests.get(final_url).json()

    return handle_bbc_response(open_bbc_page, to_say)


def handle_bbc_response(bbc_page: dict, to_say: str) -> str:
    """

    :param bbc_page: dict - bbc_page
    :param to_say: str - to_say
    :return: str - to_say
    """
    articles = bbc_page["articles"]
    results = []

    # Loop going through each article.
    for each_article in articles:
        results.append(each_article["title"])
    to_say = to_say + "Here are the top 3 news. "

    # Loop that creates the news section.
    for i in range(3):
        to_say = to_say + "Article " + str(i + 1) + ": " + results[i] + ". "

    return to_say


def create_alarm(year: int, month: int, day: int, hour: int, minute: int) -> float:
    """
    This function finds the waiting time until the alarm is going to be triggered.

    :param year: int - year
    :param month: int - month
    :param day: int - day
    :param hour: int - hour
    :param minute: int - minute
    :return: float - Unix Timestamp
    """
    this_date_time = datetime(year, month, day, hour, minute)
    timestamp = this_date_time.replace(tzinfo=timezone.utc).timestamp()
    total_time = timestamp - time.time()

    return total_time
