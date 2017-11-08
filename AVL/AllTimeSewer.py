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

start = datetime.datetime.now()
print start
pstarttime = arcpy.GetParameterAsText(0)
#pstarttime = "4/3/2017 00:00:00 AM"
pattern = '%m/%d/%Y %H:%M:%S'
epochtime = int(time.mktime(time.strptime(pstarttime[:-3], pattern)))
starttime = epochtime
endtime = starttime + 86400
tstarttime = str(starttime)
tendtime = str(endtime)

allname = "ZonarALL" + tendtime
allname2_1 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\AllTime\\Sewer\\Temp\\" + allname + "_1" + ".csv"
allname2 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\AllTime\\Sewer\\Temp\\" + allname + "_5" + ".csv"
allname3 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\AllTime\\Sewer\\" + allname + "" + ".csv"
csv_url1 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Sewer%20-%20WWTP" + "&starttime=" + tstarttime + "&endtime=" + tendtime
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

allname4 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\ALL\\" + "Table21" + ".xml"
xml_url = "https://col2225.zonarsystems.net/interface.php?action=showopen&operation=showassets&username=gisadmins&password=admin1234&format=xml"
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
			if(len(row) == 29):
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

#arcpy.SetParameter(1, fcout)
endtime = datetime.datetime.now()

print 'It took', endtime-start, 'seconds.'
#print allname3

print ("")
print ("")