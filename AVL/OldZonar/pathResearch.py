from Zonar import Zonar #Import Zonar Library
import datetime
import time
import requests

zonarurl = 'https://col2225.zonarsystems.net/interface.php'

def getEpochRange(date):
    """Given a date, returns a tuple from 12AM to 11:59PM of that day
    Date must be in YYYY-MM-DD format, including the hyphen"""
    
    startDateTime = date + " 00:00:00" #Start at 12AM
    endDateTime = date + " 23:59:59" #End at 11:59:59PM
    print startDateTime, endDateTime
    startEpoch = int(time.mktime(time.strptime(startDateTime, '%Y-%m-%d %H:%M:%S'))) - time.timezone
    endEpoch = int(time.mktime(time.strptime(endDateTime, '%Y-%m-%d %H:%M:%S'))) - time.timezone
    print startEpoch, endEpoch
    return (startEpoch, endEpoch)


day = getEpochRange('2016-03-14')
payload = {'username' : 'zakullma', 'password':'lookimnsa'} #Delete From Final Project
payload['action'] = 'showposition'
payload['operation'] = 'path'
payload['format'] = 'xml'
payload['logvers'] = '3.2'
payload['version'] = '2'
payload['starttime'] = day[0]
payload['endtime'] = day[1]

#payload['reqtype'] = 'fleet'
#payload['target']= str(1812)
payload['location'] = 'Solid Waste - Grissum'

req = requests.post(zonarurl, payload)
print req
f = open("C:\\Users\\zakullma\\Desktop\\trash.xml", 'wb')
f.write(req.text)
f.close()
