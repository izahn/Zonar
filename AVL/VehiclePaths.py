##City Of Columbia GIS
##Jeff King, Zane Kullman, Rich Buford

from operator import itemgetter
from Zonar import Zonar
import arcpy
import datetime
from datetime import timedelta
import time

print datetime.datetime.now()
arcpy.env.overwriteOutput=True

username = "gisadmins"
password = "admin1234"
zonar = Zonar(username, password)

lookup = zonar.getAssetsLookup()
lookuploc = zonar.getLocationLookup()
data = zonar.getRealTimePaths(1)
print("assetcount: " + str(data.attrib['assetcount']))

arcpy.env.overwriteOutput = True
arcpy.env.workspace = "C:\\atlas_shared\\AVL\\Zonar.gdb" #arcpy.env.workspace = "W:\\AVL.gdb" #FOR TESTING

WGS84 = arcpy.SpatialReference(4326)
timediff = ['Date_Time', 'timedif']
SDEworkspace = "C:\\Users\\gisbatch\\AppData\\Roaming\\ESRI\\Desktop10.5\\ArcCatalog\\ScriptAdmin.sde"
SDEfc = "\\City.DBO.AVL\\City.DBO.PathPointTemplate_Lines"
fcline = SDEworkspace+SDEfc #fcline = "W:\\AVL.gdb\PathPointTemplate_Lines" #FOR TESTING
fields = ['Date_Time2', 'timedif']

start = datetime.datetime.now()
timefield=datetime.datetime.now()-datetime.timedelta(days=20)
timefield2=datetime.datetime.now()

curtime = zonar.getCurEpochTime() #Get current epoch time to use for timedif field population

try:

    ##Delete features older than 7 days from the line
    with arcpy.da.UpdateCursor(fcline, fields) as featureclass2:
        for row in featureclass2:
            if row[0] <= timefield:
                featureclass2.deleteRow()
            else:
                old = datetime.datetime.strftime(row[0], '%Y-%m-%d %H:%M:%S')
                oldtime = int(time.mktime(time.strptime(old, '%Y-%m-%d %H:%M:%S'))) #Old epoch time
                sec = curtime - oldtime #timedif
                row[1] = sec #set timedif
                featureclass2.updateRow(row) #update feature
    print "Lines Deleted"

    pointlst = {}
    i = 0

    ##Open up file that has the most recent point information for each fleet ID, to parse for connecting the lines
    try:
        f = open("C:\\atlas_shared\\AVL\\recentFleet.txt", "r") #f = open("W:\\PythonScript\\Zonar\\recentFleet.txt", "r") #FOR TESTING
        for line in f: #Parse out the field information from the text file
            if( len(line) < 2 ):
                print("Ignoring blank space in recentFleet.txt")
            else:
                fleetID = line.split("'")[1]
                X = (line.split("(")[1]).split(",")[0] #Parse point X info
                Y = ((line.split("(")[1]).split(",")[1])[1:] #Parse point Y info
                timestamp = line.split("'")[3] #Parse timestamp info
                timedif = line.split("'")[5] #Parse timedif info
                location = line.split("'")[7] #Parse location info
                pointlst[i] = [fleetID, arcpy.Point(X,Y), timestamp, timedif, location] #Fill the poinstlst dictionary with these points
                i = i+1
        f.close() #close file
    except IOError as e:
        print("Creating file for the first time!")

    ##Formats XML data from Zonar into variables, saves them into pointlst dictionary created above
    for asset in data:
        fleetID = asset.attrib['id']
        for event in asset:
            timestamp = event.attrib['time']
            speed = event.attrib['speed']
            heading = event.attrib['heading']
            reasons = event.attrib['reasons']
            distance_traveled = event.attrib['distance_traveled']

            oldtime = int(time.mktime(time.strptime(timestamp[:-3], '%Y-%m-%d %H:%M:%S'))) #Old epoch time
            sec = curtime - oldtime #timedif

            pointlst[i] = [lookup[fleetID], arcpy.Point(event.attrib['long'],event.attrib['lat']), timestamp[:-3], str(sec), lookuploc[fleetID]] #Fill the pointlst dictionary
            i = i+1
    print "Created Table"

    ##Sort by time difference (Selection Sort -- 0(N^2))
    for j in range(0, len(pointlst)-1):
        iMin = j
        for i in range(j+1, len(pointlst)):
            if((pointlst[i])[2] < (pointlst[iMin])[2]):
                iMin = i
        if(iMin != j):
            tmp = pointlst[j]
            pointlst[j] = pointlst[iMin]
            pointlst[iMin] = tmp

    ##Insert lines in the correct order for each fleet ID, sorted by time differences
    cursor = arcpy.da.InsertCursor(fcline,['Fleet_ID', 'SHAPE@', 'Date_Time2', 'timedif', 'location'])
    curFleet = None
    nextFleet = "0"
    finFleet = {}
    mostRecentFleet = ""
    #Open up file for writing to write out most recent points to a text file, to be opened on next program run
    f = open("C:\\atlas_shared\\AVL\\recentFleet.txt", "w") #f = open("W:\\PythonScript\\Zonar\\recentFleet.txt", "w") #FOR TESTING
    while(nextFleet != None): #Keep going until there are no more points to connect
        prevPt = None #Used as previous point to connect to current point
        nextFleet = None #Next fleet ID to look at
        for i in range(0, len(pointlst)):
            if(curFleet == None): #First point condition
                curFleet = (pointlst[i])[0]
                finFleet[curFleet] = 1
            elif(nextFleet == None and (pointlst[i])[0] not in finFleet): #Next fleet ID condition
                nextFleet = (pointlst[i])[0]

            if((pointlst[i])[0] == curFleet): #If this item is part of the current fleet ID
                if(prevPt != None): #Make line
                    array = arcpy.Array()
                    array.add((pointlst[i])[1])
                    array.add(prevPt)
                    polyline = arcpy.Polyline(array, WGS84)
                    cursor.insertRow(((pointlst[i])[0], polyline, (pointlst[i])[2], int((pointlst[i])[3]), (pointlst[i])[4]))
                prevPt = (pointlst[i])[1] #Fill previous point
                mostRecentFleet = str(pointlst[i]) #Hold most recent point for this fleet ID
        f.write(mostRecentFleet + "\n") #Write most recent point for this fleet ID
        curFleet = nextFleet #Move to next fleet ID
        finFleet[curFleet] = 1 #Marked current fleet ID as done
    del cursor
    f.close() #Close file
    print "Created Line"

    arcpy.Compact_management(arcpy.env.workspace) #Compact the GDB
    print "Compact Complete"

except Exception as e:
    print e.message
    print arcpy.GetMessages()
    print "Think I am done"

endtime = datetime.datetime.now()

print 'It took', endtime-start, 'seconds.'

print ("")
print ("")

exit()
