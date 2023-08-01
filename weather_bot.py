# essential library
import spacy
import requests

nlp = spacy.load("en_core_web_md")

# API keys
api_key = "d1d8732a7afdea0fc946428e4330cb8e"

# get_weather function


def get_weather(city_name):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(
        city_name, api_key)

    response = requests.get(api_url)
    response_dict = response.json()

    weather = response_dict["weather"][0]["description"]

    if response.status_code == 200:
        return weather
    else:
        print('[!] HTTP {0} calling [{1}]'.format(
            response.status_code, api_url))
        return None


# chat-bot function
weather = nlp("Current weather in a city today")


def chat_bot(statement):
    statement = nlp(statement)
    min_similarity = 0.65

    if weather.similarity(statement) >= min_similarity:
        for ent in statement.ents:
            if ent.label_ == "GPE":  # GeoPolitical Entity
                city = ent.text
                city_weather = get_weather(city)
                if city_weather is not None:
                    return "In " + city + ", the current weather is: " + city_weather
                else:
                    return "Something went wrong"
            else:
                return "You need to tell me a city to check"
    else:
        "Sorry I don't understand that. Please rephrase your statement."


# Main Program
print("Hi! I am Windy a weather bot.........")
statement = input("How can I help you ?\n")
response = chat_bot(statement)
print(response)
