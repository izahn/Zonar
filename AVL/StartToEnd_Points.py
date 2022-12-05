
# Esri start of added imports
import sys, os, arcpy
# Esri end of added imports

# Esri start of added variables
g_ESRI_variable_1 = u'C:\\AVL\\AVL.gdb'
# Esri end of added variables

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

start = datetime.datetime.now()

## PARAMETERS
#tstart_date = arcpy.GetParameterAsText(0)
tstart_date = "2/11/2017 00:00:00 AM"
##

start_date = (tstart_date.split(" "))[0]
year = (start_date.split("/"))[2]
month = (start_date.split("/"))[0]
day = (start_date.split("/"))[1]
start_date = year + "-" + month + "-" + day

#start_time = tstart_date[11:-3]
#start_M = tstart_date[-3:]

fc_name = "StartToEnd_Points.txt"
end_date = start_date

lookup = zonar.getAssetsLookup()
lookuploc = zonar.getLocationLookup()
data = zonar.getPathsManyDays("All", start_date, end_date)
print("assetcount: " + str(data.attrib['assetcount']))

arcpy.env.overwriteOutput = True
arcpy.env.workspace = arcpy.env.packageWorkspace

WGS84 = arcpy.SpatialReference(4326)
fc_path = "C:\\AVL"
fc = fc_path + "\\" + fc_name
if arcpy.Exists(fc):
    arcpy.Delete_management(fc)

fields = ['Fleet_ID', 'Date_Time', 'SHAPE@XY']

arcpy.CreateFeatureclass_management(fc_path, fc_name, "POINT")
arcpy.AddField_management(fc, fields[0], "TEXT")
arcpy.AddField_management(fc, fields[1], "DATE")

try:
    cursor = arcpy.da.InsertCursor(fc, fields)

    ##Formats XML data from Zonar into variables, saves them into pointlst dictionary created above
    for asset in data:
        fleetID = asset.attrib['id']
        for event in asset:
            timestamp = event.attrib['time']
            cursor.insertRow([lookup[fleetID], timestamp[:-3], arcpy.Point(event.attrib['long'],event.attrib['lat'])]) #Fill the feature
    print "Created Feature"

    #arcpy.Compact_management(arcpy.env.workspace) #Compact the GDB
except Exception as e:
    print e.message
    print arcpy.GetMessages()
    print "Think I am done"

endtime = datetime.datetime.now()

print 'It took', endtime-start, 'seconds.'

print ("")
print ("")

exit()





