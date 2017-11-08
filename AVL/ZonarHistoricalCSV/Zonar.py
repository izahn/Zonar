##City Of Coumbia GIS
##Zane Kullman & Jeffrey King
##Work in Progress creating a Zonar Python Library

import requests
import time, datetime
import xml.etree.ElementTree as ET
import getpass

class Zonar:
    def __init__(self, url="https://col2225.zonarsystems.net/interface.php"):
        """Creates a Zonar Object"""
        self.zonarUrl = url
        self.__authenticate()

    def __init__(self, username, password, url="https://col2225.zonarsystems.net/interface.php"):
        """Creates a Zonar Object"""
        self.zonarUrl = url
        self.__auth = {'username':username, 'password':password}

    def __authenticate(self):
        """Login - Called when zonar object is created"""
        username = raw_input("Enter Zonar Username: ")
        password = getpass.getpass("Enter your Zonar Password: ")
        self.__auth = {'username':username, 'password':password}

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
