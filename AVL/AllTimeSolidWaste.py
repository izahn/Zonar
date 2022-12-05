#-------------------------------------------------------------------------------
# Name:        CSV Import From Zonar
# Author:      Rich Buford
# Created:     01/03/2017
# Copyright:   (c) richbuford 2017
#-------------------------------------------------------------------------------

import csv
import time
import datetime
import urllib
import arcpy
import os
import xml.etree.ElementTree as ET
from arcpy import env
import glob

arcpy.env.overwriteOutput = True

start = datetime.datetime.now()
print start

analysisBool = arcpy.GetParameterAsText(2)
#analysisBool = True
target = arcpy.GetParameterAsText(1)
#target = "1651"
pstarttime = arcpy.GetParameterAsText(0)
#pstarttime = "4/3/2017 00:00:00 AM"
pattern = '%m/%d/%Y %H:%M:%S'
epochtime = int(time.mktime(time.strptime(pstarttime[:-3], pattern)))
starttime = epochtime
endtime = starttime + 86400
tstarttime = str(starttime)
tendtime = str(endtime)

outFolder = "C:\\Users\\jmking\\Documents\\AVL_Local"
outWorkspace = "AVL.gdb"

arcpy.CreateFileGDB_management(outFolder, outWorkspace)
env.workspace = outFolder + "\\" + outWorkspace

allname = "ZonarALL" + tendtime
allname2_1 = "C:\\Users\\jmking\\Documents\\AVL_Local\\SolidWaste\\" + allname + "_1" + ".csv"
allname2 = "C:\\Users\\jmking\\Documents\\AVL_Local\\SolidWaste\\" + allname + "_5" + ".csv"
allname3 = "C:\\Users\\jmking\\Documents\\AVL_Local\\SolidWaste\\" + allname + "" + ".csv"

req_list = {"action": "showposition",
            "logvers": "3.6",
            "username": "gisadmins",
            "password": "admin1234",
            "operation": "path",
            "format": "csv",
            "version": "2"}

if(target and analysisBool == True):
    req_list["type"] = "Standard"
    req_list["reqtype"] = "fleet"
    req_list["target"] = target
else:
    req_list["location"] = "Solid Waste - Grissum"

req_list["starttime"] = tstarttime
req_list["endtime"] = tendtime

req_params = urllib.urlencode(req_list)
csv_url1 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params
urllib.urlretrieve(csv_url1, allname2_1)

f = allname2_1

op = open(allname2, 'wb')
output = csv.writer(op, delimiter =',')

csvfiles2 = []

op1 = open(f, 'rb')
rd = csv.reader(op1, delimiter = ',')
for row in rd:
    csvfiles2.append(row)

output.writerows(csvfiles2)

op.close()
op1.close()

allname4 = "C:\\Users\\jmking\\Documents\\AVL_Local\\SolidWaste\\" + "Table21" + ".xml"

req_list = {"action": "showopen",
            "username": "gisadmins",
            "password": "admin1234",
            "operation": "showassets",
            "format": "xml"}

req_params = urllib.urlencode(req_list)
xml_url = "https://col2225.zonarsystems.net/interface.php?%s" % req_params
urllib.urlretrieve(xml_url, allname4)

tree = ET.parse(allname4)
root = tree.getroot()

lookup = {}
for member in root.findall('asset'):
    fleet = member.find('fleet').text
    location = member.find('location').text
    lookup[fleet] = location

with open(allname2, 'rb') as csvinput:
    with open(allname3, 'wb') as csvoutput:
        reader = csv.reader(csvinput)
        writer = csv.writer(csvoutput)

        wr = []
        row0 = reader.next()
        row0.append('Location')
        for x in range(0,12):
            del row0[17]

        wr.append(row0)

        for row in reader:
            row.append(lookup[row[1]])
            ept = int(row[3])
            convt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept))
            row[2] = convt
            for x in range(0,12):
                del row[17]
            wr.append(row)

        writer.writerows(wr)

print "ALL Imported"
os.remove(allname2_1)
os.remove(allname2)

if(analysisBool == True and target):
    pickups = "pickups"
    pickups_Lyr = "pickups_lyr"
    arcpy.CopyFeatures_management("Database Connections\\ARCSDE_10.sde\\City.DBO.Services\\City.DBO.Solid_Waste", pickups)
    arcpy.MakeFeatureLayer_management(pickups, pickups_Lyr)

    routePolys = "routes"
    routePolys_Lyr = "routes_lyr"
    arcpy.CopyFeatures_management("Database Connections\\ARCSDE_10.sde\\City.DBO.PW_solid_waste\\City.DBO.Truck_Routes_Current", routePolys)
    arcpy.MakeFeatureLayer_management(routePolys, routePolys_Lyr)

    sr = arcpy.Describe(routePolys_Lyr).spatialReference

    outFeat = "outFeat"
    outFeat_Lyr = "points_lyr"
    arcpy.MakeXYEventLayer_management(allname3, "Lon", "Lat", outFeat_Lyr)
    arcpy.Project_management(outFeat_Lyr, outFeat, sr)
    arcpy.MakeFeatureLayer_management(outFeat, outFeat_Lyr)

    summedPolys = "summPolys"
    summedPolys_Lyr = "summPolys_Lyr"
    arcpy.SpatialJoin_analysis(routePolys_Lyr, outFeat_Lyr, summedPolys)
    arcpy.MakeFeatureLayer_management(summedPolys, summedPolys_Lyr)

    summedPickups = "summPickups"
    arcpy.SpatialJoin_analysis(summedPolys_Lyr, pickups_Lyr, summedPickups)

    maxim = []
    routeList = []
    with arcpy.da.SearchCursor(summedPickups, ['Join_Count', 'Join_Count_1', 'route']) as cursor:
        for row in cursor:
            if row[0] > 100:
                maxim.append([row[0], row[1], row[2]])

    for each in maxim:
        print "\n", each[0], " - ", each[1], " - ", each[2]
        route = each[2]

        arcpy.SelectLayerByAttribute_management(routePolys_Lyr, "NEW_SELECTION", "route='" + route + "'")
        arcpy.SelectLayerByLocation_management(outFeat_Lyr, "INTERSECT", routePolys_Lyr)

        featList = []
        fmax = -1
        fmin = -1
        with arcpy.da.SearchCursor(outFeat_Lyr, ['Time_CDT_']) as cursor:
            for row in cursor:
                if row[0] > fmax:
                    fmax = row[0]
                if (row[0] < fmin) or (fmin == -1):
                    fmin = row[0]

        mins = float(fmax-fmin)
        avgPU = float(mins/each[1])

        print 'fmax: ', fmax
        print 'fmin: ', fmin
        print 'Route ', route, ' with ', avgPU, 's avg pickup time'

#arcpy.SetParameter(1, fcout)
endtime = datetime.datetime.now()

print 'It took', endtime-start, 'seconds.'
#print allname3

print ("")
print ("")
