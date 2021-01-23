import datetime

from functions import (
    handle_covid_response,
    handle_weather_response,
    handle_bbc_response,
)


def testing_handle_covid_response():
    """
    Test function for handle_covid_response function.

    :return: None
    """
    today = datetime.date.today()
    today_date = today.strftime("%Y-%m-%d")

    proxy_covid_data = {
        "data": [
            {"date": today_date, "newCases": 123, "newDeathsByDeathDate": 1},
        ]
    }

    assert (
        handle_covid_response(proxy_covid_data)
        == "The new cases of Covid19 from today are: 123 "
        "The number of Covid19 deaths today: 1"
    )


def testing_handle_weather_response():
    """
    Test function for handle_weather_response.

    :return: None
    """

    proxy_weather_data = {
        "cod": 200,
        "main": {
            "temp": 10,
            "pressure": 1,
            "humidity": 50,
        },
        "weather": [{"description": "Nice weather"}],
    }

    assert handle_weather_response(proxy_weather_data, "") == (
        "The weather for today is:  Temperature (in kelvin "
        "unit) = "
        + "10"
        + "\n atmospheric pressure (in hPa unit) = "
        + "1"
        + "\n humidity (in percentage) = "
        + "50"
        + "\n description = "
        + "Nice weather"
    )


def testing_handle_bbc_response():
    """
    Test function for handle_bbc_response.

    :return: None
    """

    proxy_news_data = {
        "articles": [{"title": "News 1"}, {"title": "News 2"}, {"title": "News 3"}]
    }

    assert handle_bbc_response(proxy_news_data, "") == (
        "Here are the top 3 news. "
        + "Article "
        + "1"
        + ": "
        + "News 1"
        + ". "
        + "Article "
        + "2"
        + ": "
        + "News 2"
        + ". "
        + "Article "
        + "3"
        + ": "
        + "News 3"
        + ". "
    )


if __name__ == "__main__":
    testing_handle_covid_response()
    testing_handle_weather_response()
    testing_handle_bbc_response()
