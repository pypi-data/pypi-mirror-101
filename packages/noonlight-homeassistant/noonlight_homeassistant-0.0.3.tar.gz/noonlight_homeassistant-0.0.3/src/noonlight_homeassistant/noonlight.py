import requests
import json

class Noonlight:

    def __init__(self,url,serverToken):
        self.url = url
        self.serverToken = serverToken
        self.alarmID = None
        self.ownerID = None
        self.status = None
        return

    def createAlarm(self,addressline1,city,state,zip,police,fire,medical,other,instructions,name,phone,pin):
        payload = {
            "location": {"address": {
                    "line1": addressline1,
                    "city": city,
                    "state": state,
                    "zip": zip
                }},
            "services": {
                    "police": police,
                    "fire": fire,
                    "medical": medical,
                    "other": other
                    },
            "instructions": {"entry": instructions},
            "name": name,
            "phone": phone,
            "pin": pin
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.serverToken
        }

        response = requests.request("POST", self.url, json=payload, headers=headers)

        if response.ok:
            responseVariables = json.loads(response.text)
            self.alarmID = responseVariables["id"]
            self.ownerID = responseVariables["owner_id"]
            self.status = responseVariables["status"]
            return responseVariables
        else:
            return False

    def updateAlarm(self,alarmID):
        update_url = self.url + "/" + alarmID + "/status"
        print(update_url)

        payload = {"status": "CANCELED"}

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.serverToken
        }

        response = requests.request("POST", update_url, json=payload, headers=headers)

        if response.ok:
            return True
        else:
            return False