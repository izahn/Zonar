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
import arcpy, datetime, time, os, sys

arcpy.env.overwriteOutput = True
print "env set"
arcpy.env.workspace = "C:\atlas_shared\AVL\Zonar.gdb"
print "workspace set"
WGS84 = arcpy.SpatialReference(4326)
print "Spatial Ref Set"

start = datetime.datetime.now()
print start

username = "gisadmins"
password = "admin1234"
zonar = Zonar(username, password)
saveFile = "CurrentLocations"

lookup = zonar.getAssetsLookup()
lookuploc = zonar.getLocationLookup()
data = zonar.getRealTimeCurrent()

try:
	##Create Insert Cursor
	delCur = arcpy.da.UpdateCursor(saveFile,['Fleet_ID', 'SHAPE@XY', 'Date_Time', 'Speed'])
	for cur in delCur:
		delCur.deleteRow()
	del delCur

	cursor = arcpy.da.InsertCursor(saveFile,['Fleet_ID', 'SHAPE@XY', 'Date_Time', 'Speed'])
	##Formats XML data into variables, saves them into arc feature class created above
	for asset in data:
		fleetID = asset.attrib['fleet']
		timestamp = asset.find('time').text
		point = arcpy.PointGeometry(arcpy.Point(asset.find('long').text,asset.find('lat').text))
		speed = asset.find('speed').text
		cursor.insertRow((fleetID, point, timestamp, speed))
	del cursor
	print "Created Points"

except Exception as e:
	print e.message
	print arcpy.GetMessages()
	print "Think I am done"

endtime = datetime.datetime.now()

print 'It took', endtime-start, 'seconds.'

print ("")
print ("")

os.execv(sys.executable, ["python"] + sys.argv)