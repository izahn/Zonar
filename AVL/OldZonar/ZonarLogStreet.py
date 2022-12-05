##City Of Coumbia GIS
##Zane Kullman
##DO NOT SHARE##

from Zonar import Zonar
import requests
import time, sched
import xml.etree.ElementTree as ET
import csv
import sys

from datetime import datetime
from os import system

def periodicLog(scheduler, interval, zonar, fleet, firstRun=False):
    try:
        data = zonar.getFull(fleet)
        f = open("L:\\Projects\\Zonar\\CollectStreetLog\\ID{}.csv".format(fleet), 'ab')
        dictWriter = csv.DictWriter(f, fieldnames = ['time', 'long', 'lat', 'speed', 'heading', 'odometer', 'power'])
        if firstRun:
            dictWriter.writeheader()
            dictWriter.writerow(data)
        else:
            dictWriter.writerow(data)
        f.close()
    except:
        print "Error! " + data
    scheduler.enter(1,interval,periodicLog, (scheduler, interval, zonar, fleet))


if len(sys.argv) <= 1:
    fleet = input('Enter the fleet ID: ')
else:
    fleet = sys.argv[1]
    
system("title "+str(fleet))
system("mode con:cols=70 lines=5")

zonar = Zonar(disableEncryption=True)
s = sched.scheduler(time.time, time.sleep)
periodicLog(s, 1, zonar, fleet, firstRun=True)

try:
    while True:
        s.run()
except:
    print("Restarting at {}".format(str(datetime.now())))
