#-------------------------------------------------------------------------------
# Name:        Current Location Zonar
# Purpose:      Show the current location of Zonar vehicles
#
# Author:      (Jeff King, Rich Buford)
#
# Created:     30/12/2016
# Copyright:   (c) City of Columbia GIS
#-------------------------------------------------------------------------------

from Zonar import Zonar
import arcpy, datetime, time
arcpy.env.overwriteOutput=True
starttime = datetime.datetime.now()
print starttime
username = "gisadmins"
password = "admin1234"
zonar = Zonar(username, password)
saveFile = "plow_spread2" #Needs to be in Zonar.gdb before run
streetBuf = "street_buffer2" #Needs to be in Zonar.gdb before run

lookup = zonar.getAssetsLookup()
lookuploc = zonar.getLocationLookup()
data = zonar.getRealTimePaths(1)

##Creates feature for points
arcpy.env.overwriteOutput = True
print "env set"
arcpy.env.workspace = "C:\\atlas_shared\\AVL\\Zonar.gdb"
print "workspace set"
WGS84 = arcpy.SpatialReference(4326)
print "Spatial Ref Set"

try:
    ##Create Insert Cursor
    delCur = arcpy.da.UpdateCursor(saveFile,['Fleet_ID', 'SHAPE@XY', 'Date_Time', 'Speed', 'location'])
    for cur in delCur:
        delCur.deleteRow()
    del delCur

    cursor = arcpy.da.InsertCursor(saveFile,['Fleet_ID', 'SHAPE@XY', 'Date_Time', 'Speed', 'location'])
    ##Formats XML data into variables, saves them into arc feature class created above
    for asset in data:
        ID = asset.attrib['id']
        timeTrav = 0
        point = None
        speed = None
        fleetID = None
        for event in asset:
            timestamp = (event.attrib['time'])[:-3]
            oldtime = int(time.mktime(time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')))
            curtime = zonar.getCurEpochTime()
            sec = curtime - oldtime
            point = arcpy.PointGeometry(arcpy.Point(event.attrib['long'],event.attrib['lat']))
            speed = event.attrib['speed']
            fleetID = lookup[ID]
            location = lookuploc[ID]
            timeTrav = sec

            #into arc
            cursor.insertRow((fleetID, point, timestamp, speed, location))
    del cursor
    print "Created Points"

    ##Join information between zonar points and street buffer
    newBuf = "new_buffer2"
    arcpy.SpatialJoin_analysis(streetBuf, saveFile, newBuf, "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", "INTERSECT", "#")
    print "Created Spatial Join"

    ##Dictionaries to match information
    timestamp = {}
    loc = {}
    holdTime = {}
    locSearch = "Street - Grissum"

    ##fill timestamp dictionary with most recent timestamp for each buffer segment, for each fleet ID
    cursor = arcpy.da.SearchCursor(newBuf,['timestamp', 'timedif', 'Date_Time', 'UNIQUE_ID', 'location_1'])
    for cur in cursor:
        i = str(cur[3])
        loc[i] = cur[4]
        if(cur[4] == locSearch):
            thisTime = None
            hold = None
            if(cur[2] != None): #assign a datetime if there was none
                thisTime = int(time.mktime(time.strptime(cur[2], '%Y-%m-%d %H:%M:%S')))

            try:
                hold = timestamp[i]
            except:
                hold = None

            timestamp[i] = cur[2]
            try:
                if(thisTime != None and thisTime > holdTime[i]):
                    holdTime[i] = thisTime
                else:
                    timestamp[i] = hold
            except:
                holdTime[i] = thisTime
    del cursor
    print "Searched through and filled timestamp dictionary"

    ##Matches dictionaries from the spatial join to the original street buffer segments
    cursor = arcpy.da.UpdateCursor(streetBuf,['timestamp', 'timedif', 'UNIQUE_ID', 'location'])
    for cur in cursor:
        i = str(cur[2])
        cur[3] = loc[i]
        if(cur[3] == locSearch):
            if(timestamp[i] != None):
                cur[0] = timestamp[i]

            if(cur[0] != None):
                oldtime = int(time.mktime(time.strptime(cur[0], '%Y-%m-%d %H:%M:%S')))
                curtime = zonar.getCurEpochTime()
                sec = curtime - oldtime

                cur[1] = sec

            cursor.updateRow(cur)
    del cursor

except Exception as e:
    print e.message
    print arcpy.GetMessages()
    print "Processes Completed"

endtime = datetime.datetime.now()
print 'It took', endtime-starttime, 'to run'
print ("")
print ("")
