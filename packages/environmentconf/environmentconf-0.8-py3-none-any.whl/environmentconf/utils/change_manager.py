#! /usr/bin/env python
from typing import Dict

class ChangeManager(object):
    """This class ChangeManager.

    It contains properties and methods that listens for action change and notifies subscribers.
    """

    changeProducers = None
    UNCHANGED = "UNCHANGED"
    CHANGED = "CHANGED"
    def __init__(self) -> None:
        self.changeProducers = {}
        self.changeSubscribers = []
    
    def register_producer(self, producer_name, state):
        """This method registers the change producers.
        
        @param producer_name: str - Name of the change producer
        @param state: str - Initial state from where it might change to some different state
        """
        self.changeProducers[producer_name] = {
            "state": state,
            "changeSubscribers": []
        }
    
    def register_subscriber(self, name, subscriber, action_args):
        """This method registers the change subscribers.
        
        @param name: str - Name of the change producer
        @param subscriber: object - An instance of change subscriber
        @param action_args: Dict - Action arguments to pass when notifying change
        """
        if name in self.changeProducers:
            self.changeProducers[name]["changeSubscribers"].append({
                "subscriber": subscriber,
                "action_args": action_args
            })
    
    def change_state(self, producer_name, state):
        """This method registers the state change.
        
        @param producer_name: str - Name of the change producer
        @param state: str - New state
        """
        if producer_name in self.changeProducers:
            self.changeProducers[producer_name]["state"] = state

    def trigger_changes(self):
        """Notifies all the subscribers if any producer registered change."""
        for producer_name in self.changeProducers.keys():
            producer = self.changeProducers[producer_name]
            if producer["state"] == self.CHANGED and len(producer["changeSubscribers"]) > 0:
                for subscriber in producer["changeSubscribers"]:
                    try:
                        func = getattr(subscriber["subscriber"], "change_handler")
                        func(subscriber["action_args"])
                    except Exception as ex:
                        print(ex)