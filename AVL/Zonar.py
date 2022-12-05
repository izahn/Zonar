##City Of Coumbia GIS
##Zane Kullman & Jeffrey King
##Work in Progress creating a Zonar Python Library

import requests
import time, datetime
import xml.etree.ElementTree as ET
import getpass

class Zonar:
    def __init__(self, url="https://bos0501.zonarsystems.net/interface.php"):
        """Creates a Zonar Object"""
        self.zonarUrl = url
        self.__authenticate()

    def __init__(self, username, password, url="https://bos0501.zonarsystems.net/interface.php"):
        """Creates a Zonar Object"""
        self.zonarUrl = url
        self.__auth = {'username':username, 'password':password}

    def __authenticate(self):
        """Login - Called when zonar object is created"""
        username = input("Enter Zonar Username: ")
        password = getpass.getpass("Enter your Zonar Password: ")
        self.__auth = {'username':username, 'password':password}

    def getEpochTime(self, date, AMorPM):
        if AMorPM == "AM":
            DateTime = date + " 00:00:00"
        else:
            DateTime = date + " 23:59:59"
        print(DateTime)
        epoch = int(time.mktime(time.strptime(DateTime, '%Y-%m-%d %H:%M:%S')))
        print(epoch)
        return epoch

    def getCurEpochTime(self):
        """Get the current time in epoch time for time difference calculations"""
        DateTime = time.strftime("%Y-%m-%d %H:%M:%S")
        epoch = int(time.mktime(time.strptime(DateTime, '%Y-%m-%d %H:%M:%S')))
        return epoch

    def getPathsManyDays(self, Location, StartDate, EndDate, Type="Standard"):
        """Use this method to get a XML Object for vehicles over a range of days
        Date must be formatted YYYY-MM-DD
        Returns XML, and the UID for each vehicle is it's DIB, not Fleet ID.
        See lookupByID to covert
        Use 'Location = All' to get every vehicle"""

        """Return data is structured as a tree, a list of Assets, each with a list of events, events have xy"""
        payload = self.__auth
        payload['starttime'] = self.getEpochTime(StartDate, "AM")
        payload['endtime'] = self.getEpochTime(EndDate, "PM")

        if Location != "All": #If it is "" then it will return all
            payload['location'] = Location
        else:
            print("Gathering all data will take a while")

        payload['action'] = 'showposition'
        payload['operation'] = 'path'
        payload['format'] = 'xml'
        payload['logvers'] = '3.2'
        payload['version'] = '2'

        req = requests.post(self.zonarUrl, payload)
        data = ET.fromstring(req.text)
        return data

    def getRealTimePaths(self, minuteRange, Type="Standard"):
        """Use this method to get recent paths in real time.
        Input defines the minute range to pull data."""

        """Return data is structured as a tree, a list of Assets, each with a list of events, events have xy"""
        payload = self.__auth
        payload['endtime'] = self.getCurEpochTime()
        payload['starttime'] = payload['endtime'] - 60*minuteRange

        payload['action'] = 'showposition'
        payload['operation'] = 'path'
        payload['format'] = 'xml'
        payload['logvers'] = '3.4'
        payload['version'] = '2'

        req = requests.post(self.zonarUrl, payload)
        data = ET.fromstring(req.text)
        return data

    def getRealTimeCurrent(self, Type="Standard"):
        """Use this method to get current points in real time."""

        """Return data is structured as a tree, a list of Assets, each with a list of events, events have xy"""
        payload = self.__auth
        payload['action'] = 'showposition'
        payload['operation'] = 'current'
        payload['format'] = 'xml'
        payload['logvers'] = '3.4'
        payload['version'] = '2'
        payload['power'] = 'on'

        req = requests.post(self.zonarUrl, payload)
        data = ET.fromstring(req.text)
        return data

    def getAssetsLookup(self):
        """This Method returns a lookup table to match asset ID with fleet ID.
        We need this because the path operation does not currently output fleet
        ID information."""
        payload = self.__auth
        payload['action'] = 'showopen'
        payload['operation'] = 'showassets'
        payload['format'] = 'xml'
        r = requests.post(self.zonarUrl, payload)
        data = ET.fromstring(r.text)

        lookup = {}
        for asset in data:
            ID = asset.attrib['id']
            fleetID = asset.find('fleet').text
            lookup[ID] = fleetID

        return lookup

    def getLocationLookup(self):
        """This Method returns a lookup table to pull vehicle location info.
        We need this because the path operation does not currently output location
        information."""
        payload = self.__auth
        payload['action'] = 'showopen'
        payload['operation'] = 'showassets'
        payload['format'] = 'xml'
        r = requests.post(self.zonarUrl, payload)
        data = ET.fromstring(r.text)

        lookup = {}
        for asset in data:
            ID = asset.attrib['id']
            location = asset.find('location').text
            lookup[ID] = location

        return lookup

