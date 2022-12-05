##City Of Columbia GIS
##Jeff King, Zane Kullman, Rich Buford

from Zonar import Zonar
import arcpy
import datetime
from datetime import timedelta
import time
print datetime.datetime.now()
arcpy.env.overwriteOutput=True

username = "gisadmins"
password = "GIS123"
zonar = Zonar(username, password)

lookup = zonar.getAssetsLookup()
lookuploc = zonar.getLocationLookup()
data = zonar.getRealTimePaths(5)
print("assetcount: " + str(data.attrib['assetcount']))

##Creates feature for points
arcpy.env.overwriteOutput = True

arcpy.env.workspace = "C:\\AVL\\AVL.gdb"

WGS84 = arcpy.SpatialReference(4326)
timediff = ['Date_Time', 'timedif']
fcin="PathPointTemplate"
fcline="C:\\AVL\\AVL.gdb\PathPointTemplate_Lines"
fields = ['Date_Time2']

start = datetime.datetime.now()
timefield=datetime.datetime.now()-datetime.timedelta(seconds=4680)
timefield2=datetime.datetime.now()

try:
    with arcpy.da.UpdateCursor(fcin, fields) as featureclass:
        for row in featureclass:
##            if row[0] <= timefield:
                featureclass.deleteRow()

    print "Rows Deleted"

    with arcpy.da.UpdateCursor(fcline, fields) as featureclass2:
        for row in featureclass2:
##            if row[0] <= timefield:
                featureclass2.deleteRow()

    print "Rows Deleted"

    cursor = arcpy.da.InsertCursor('C:\\AVL\\AVL.gdb\PathPointTemplate',['Fleet_ID', 'SHAPE@XY', 'Date_Time2', 'Speed', 'heading', 'reasons', 'distance_traveled', 'Location', 'timedif'])
    #Formats XML data into variables, saves them into arc feature class created above
    for asset in data:
        #fleetID = zonar.lookupAssetByID(asset.attrib['id'])
        fleetID = asset.attrib['id']
        for event in asset:
            point = arcpy.PointGeometry(arcpy.Point(event.attrib['long'],event.attrib['lat']))
            timestamp = event.attrib['time']
            speed = event.attrib['speed']
            heading = event.attrib['heading']
            reasons = event.attrib['reasons']
            distance_traveled = event.attrib['distance_traveled']

            oldtime = int(time.mktime(time.strptime(timestamp[:-3], '%Y-%m-%d %H:%M:%S')))
            curtime = zonar.getCurEpochTime()
            sec = curtime - oldtime
            #into arc
            cursor.insertRow((lookup[fleetID], point, timestamp[:-3], speed, heading, reasons, distance_traveled, lookuploc[fleetID], sec))
    del cursor
    print "Created Points"

    pointlst = {}
    i = 0
    cursor = arcpy.da.SearchCursor(fcin,['Fleet_ID', 'SHAPE@XY', 'Date_Time2'])
    print "1"
    for cur in cursor:
        x,y = cur[1]
        pointlst[i] = [int(cur[0]), arcpy.Point(x,y), cur[2]]
        i=i+1

    ##Sort by time difference
    for j in range(0, len(pointlst)-1):
        iMin = j
        for i in range(j+1, len(pointlst)):
            if((pointlst[i])[2] < (pointlst[iMin])[2]):
                iMin = i
        if(iMin != j):
            tmp = pointlst[j]
            pointlst[j] = pointlst[iMin]
            pointlst[iMin] = tmp

    cursor = arcpy.da.InsertCursor(fcline,['Fleet_ID', 'SHAPE@', 'Date_Time2'])
    print "6"
    curFleet = None
    print "7"
    nextFleet = "0"
    print "8"

    finFleet = {}
    print "9"

    while(nextFleet != None):
        print "10"
        prevPt = None
        print "11"
        nextFleet = None
        print "12"
        for i in range(0, len(pointlst)):
            if(curFleet == None):
                print "14"
                curFleet = (pointlst[i])[0]
                print "15"
                finFleet[curFleet] = 1
                print "16"
            elif(nextFleet == None and (pointlst[i])[0] not in finFleet):
                print "17"
                nextFleet = (pointlst[i])[0]
                print "18"

            if((pointlst[i])[0] == curFleet):
                if(prevPt != None):
                    print "20"
                    array = arcpy.Array()
                    print "21"
                    array.add((pointlst[i])[1])
                    print "22"
                    array.add(prevPt)
                    print "23"
                    polyline = arcpy.Polyline(array, WGS84)
                    print "24"
                    cursor.insertRow(((pointlst[i])[0], polyline, (pointlst[i])[2]))
                    print "25"

                prevPt = (pointlst[i])[1]
                print "26"

        curFleet = nextFleet
        print "27"
        finFleet[curFleet] = 1
        print "28"
    del cursor
    print "Created Line"

except Exception as e:
    print e.message
    print arcpy.GetMessages()
    print "Think I am done"

endtime = datetime.datetime.now()

print 'It took', endtime-start, 'seconds.'

print ("")
print ("")
exit()
