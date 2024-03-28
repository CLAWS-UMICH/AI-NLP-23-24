# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class Open(Action):

    def name(self) -> Text:
        return "action_open"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'open', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class Close(Action):

    def name(self) -> Text:
        return "action_close"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'close', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class Show(Action):

    def name(self) -> Text:
        return "action_show"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'show', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class Hide(Action):

    def name(self) -> Text:
        return "action_hide"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'hide', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class Enter(Action):

    def name(self) -> Text:
        return "action_enter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'enter', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []

class Mode(Action):

    def name(self) -> Text:
        return "action_mode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'mode', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class Complete(Action):

    def name(self) -> Text:
        return "action_complete"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'complete', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class Take(Action):

    def name(self) -> Text:
        return "action_take"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'take', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class Delete(Action):

    def name(self) -> Text:
        return "action_delete"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'delete', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []

class Sample(Action):

    def name(self) -> Text:
        return "action_sample"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'sample', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []

    
class Pin(Action):

    def name(self) -> Text:
        return "action_pin"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'pin', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class On(Action):

    def name(self) -> Text:
        return "action_on"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'on', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []

class Off(Action):

    def name(self) -> Text:
        return "action_off"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'off', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []

class Temperature(Action):

    def name(self) -> Text:
        return "action_temperature"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'temperature', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class Set(Action):

    def name(self) -> Text:
        return "action_set"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'set', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class End(Action):

    def name(self) -> Text:
        return "action_end"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'end', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class Add(Action):

    def name(self) -> Text:
        return "action_add"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'add', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class Mute(Action):

    def name(self) -> Text:
        return "action_mute"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'mute', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []
    
class Go(Action):

    def name(self) -> Text:
        return "action_go"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'go', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []

class WhatIsMy(Action):

    def name(self) -> Text:
        return "action_what_is_my"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        entity = next(tracker.get_latest_entity_values("item"), None)
        jsonstring = "{'command': 'what_is_my', 'entity':'" + entity + "'}" if entity is not None else "{'command': 'close'}"
        dispatcher.utter_message(text=jsonstring)
        return []

"""
- geosampling
  - take
  - delete
  - sample
  - pin
  - on
  - off
  - temperature
  - open
  - close
  - show
  - hide
  - enter
  - switch_mode
  - complete
  - set
  - end
  - add
  - mute
  - navigate
  - query_status
  - map
"""