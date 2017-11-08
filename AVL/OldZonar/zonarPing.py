##City Of Coumbia GIS
##Zane Kullman
##DO NOT SHARE##
##Probably Broken as I work on Zonar API Wraper and actually think critically
from Zonar import Zonar
import requests
import time, sched
import xml.etree.ElementTree as ET

def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, periodic,
                    (scheduler, interval, action, actionargs))

    print len(scheduler.queue)
    action(*actionargs)

def printPoint(zonar, fleet):
    r = zonar.getLocation(fleet)
    data = ET.fromstring(r.text)
    #print "long: {}, lat: {}".format(data[0][0].text, data[0][1].text)
    print r.text
    return data


def timeCheck(scheduler, zonar, fleet):
    r =zonar.getLocation(fleet)
    data = ET.fromstring(r.text)[0]
    timestamp = int(data[3].text)

    global lastTime
    if timestamp > lastTime:
        f = open("C:\\Users\\zakullma\\Desktop\\Time_{}.csv".format(fleet), 'ab')
        f.write(str(timestamp)+"\n")
        print 'Hey!'
        lastTime = timestamp
        f.close()
    scheduler.enter(1, 1, timeCheck,
                    (scheduler, zonar, fleet))
        
    
s = sched.scheduler(time.time, time.sleep)
zonar = Zonar() ##This will ask for a password
lastTime = None
fleet = input('Enter the fleet ID: ')
timeCheck(s, zonar, fleet)
