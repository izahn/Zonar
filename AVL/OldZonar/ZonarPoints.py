##Zonar Track Single Vehicle
##Zane Kullman
##City Of Columbia GIS
##DO NOT SHARE##

import xml.etree.ElementTree as ET
import requests
import time

import arcpy
import getpass

def zaneAuth():
    secretKey = getpass.getpass("Enter the secret key: ")
    username = "zakullma"
    ##OTP encrypted PW, requires the secret key to be user entered (see above). This password is only for zonar
    encryptedPW = '\x1c\x0e\x1c\x18\x1e\x02\x1c\x17P'
    xorWord = lambda ss,cc: ''.join(chr(ord(s)^ord(c)) for s,c in zip(ss,cc*100))
    return {'username':username, "password":xorWord(encryptedPW, secretKey)}

def getData(payload): ##Returns Long, Lat
    r = requests.post("https://col2225.zonarsystems.net/interface.php", payload)
    doc = ET.fromstring(r.text)
    return doc

def printData(data, fleetID = 0):
    for vehicle in data:
        if fleetID == 0 or fleetID == int(vehicle.attrib['fleet']):
            for key in vehicle.attrib:
                print "{} : {}".format(key, vehicle.attrib[key])
            for i,value in enumerate(vehicle):
                print "{} : {}".format(vehicle[i].tag, vehicle[i].text)
            print "\n==========================="

def toGIS(fleetID = 0): #0 Means all

    ##HTTPS Payload for Post
    payload = zaneAuth()
    payload['action'] = 'showposition'
    payload['operation'] = 'current'
    payload['format'] = 'xml'
    payload['version'] = '2'
    payload['logvers'] = '3'
    payload['power'] = 'on'
    
    ##ArcSetup
    arcpy.env.workspace = "J:\\Projects\\Zonar\\Zonar.gdb" ##Move To J Drive
    fc = "truckTrack"
    fields = ["Fleet_ID", "SHAPE@XY", "Date_Time", "Heading", "Speed", "Power"]
    count = 0
    while True:
        print "tick {}".format(count)
        data = getData(payload)
        printData(data)
        print "tick {}".format(count)
        count = count + 1
        
        rows = []
        for vehicle in data:
            if fleetID == 0 or fleetID == int(vehicle.attrib['fleet']):
                xy = (float(vehicle[0].text), float(vehicle[1].text))
                row = [vehicle.attrib['fleet'], xy, vehicle[3].text, vehicle[2].text, vehicle[4].text, vehicle[5].text]
                rows.append(row)
                
        cursor = arcpy.da.InsertCursor(fc, fields)
        for row in rows:
            cursor.insertRow(row)
        del cursor
        time.sleep(5)

def getKML():
    payload = zaneAuth()
    payload['password'] = 'lookimnsa'
    payload['action'] = 'showposition'
    payload['operation'] = 'path'
    payload['format'] = 'kml'

    payload['starttime'] = '1454133600'
    payload['endtime'] = '1454392800'
    payload['version'] = '2'
    payload['logvers'] = '3'
    r = requests.get("https://col2225.zonarsystems.net/interface.php", payload)
    return r
