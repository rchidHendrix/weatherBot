# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

import requests
import json

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher



class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def JsonExtraction(self, location) -> Text:
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid=ac5b2b9b89fa2cdc85eb4a13aadc8106".format(location))
        print("Staus code", response.status_code)
        text = json.dumps(response.json(), sort_keys=True, indent=4)
        c = json.loads(text)
        print("temp ", c['main']['temp'])
        return c['main']['temp']

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot('location')
        print("location name", location)
        l = self.JsonExtraction(location)

        # Convert K to C
        l = l - 273.15
        
        print("Location", l)
        dispatcher.utter_message(text="Today's weather at {} {} 'C!".format(location, round(l, 2)))

        return []

  
