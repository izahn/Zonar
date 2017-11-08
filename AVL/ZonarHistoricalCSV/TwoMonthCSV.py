#-------------------------------------------------------------------------------
# Name:        CSV Import From Zonar
# Author:      Rich Buford & Jeff King
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

endtime = int(time.time())
starttime = endtime - 60
tstarttime = str(starttime)
tendtime = str(endtime)

#WaterLight
allname = "ZonarWaterLight" + tendtime
allname2_1 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\WaterLight\\Temp\\" + allname + "_1" + ".csv"
allname2_2 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\WaterLight\\Temp\\" + allname + "_2" + ".csv"
allname2_3 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\WaterLight\\Temp\\" + allname + "_3" + ".csv"
allname2_4 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\WaterLight\\Temp\\" + allname + "_4" + ".csv"
allname2 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\WaterLight\\Temp\\" + allname + "_5" + ".csv"
allname3 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\WaterLight\\" + allname + "" + ".csv"
csv_url1 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Electric%20Distribution" + "&starttime=" + tstarttime + "&endtime=" + tendtime
csv_url2 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Electric%20Utility%20Services" + "&starttime=" + tstarttime + "&endtime=" + tendtime
csv_url3 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Water%20Distribution" + "&starttime=" + tstarttime + "&endtime=" + tendtime
csv_url4 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Water%20Light%20Engineering" + "&starttime=" + tstarttime + "&endtime=" + tendtime
urllib.urlretrieve(csv_url1, allname2_1)
urllib.urlretrieve(csv_url2, allname2_2)
urllib.urlretrieve(csv_url3, allname2_3)
urllib.urlretrieve(csv_url4, allname2_4)
f = allname2_1
csvinputs = [allname2_3, allname2_2, allname2_4]
op = open(allname2, 'wb')
output = csv.writer(op, delimiter =',')
csvfiles2 = []
op1 = open(f, 'rb')
rd = csv.reader(op1, delimiter = ',')
for row in rd:
    csvfiles2.append(row)
for files2 in csvinputs:
    op2 = open(files2, 'rb')
    rd2 = csv.reader(op2, delimiter = ',')
    rd2.next()
    for row2 in rd2:
        csvfiles2.append(row2)
    op2.close()
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
            row.append(lookup[row[1]])
            ept = int(row[3])
            convt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept))
            row[2] = convt
            for x in range(0,12):
                del row[17]
            wr.append(row)
        writer.writerows(wr)
print "WaterLight Imported"
os.remove(allname2_1)
os.remove(allname2_3)
os.remove(allname2_2)
os.remove(allname2_4)
os.remove(allname2)
#End WaterLight

#Sewer
sewername = "ZonarSewer" + tendtime
sewer_out = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\Sewer\\Temp\\" + sewername + "" + ".csv"
sewer_url = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Sewer%20and%20Stormwater%20-%20WWTP" + "&starttime=" + tstarttime + "&endtime=" + tendtime
urllib.urlretrieve(sewer_url, sewer_out)
sewer_write = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\Sewer\\" + sewername + "" + ".csv"
with open(sewer_out, 'rb') as sewerinput:
    with open(sewer_write, 'wb') as seweroutput:
        readersewer = csv.reader(sewerinput)
        writersewer = csv.writer(seweroutput)
        Sewer = []
        rowsewer = readersewer.next()
        rowsewer.append('Location')
        for x in range(0,12):
            del rowsewer[17]
        Sewer.append(rowsewer)
        for row in readersewer:
            row.append("Sewer")
            ept = int(row[3])
            convt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept))
            row[2] = convt
            for x in range(0,12):
                del row[17]
            Sewer.append(row)
        writersewer.writerows(Sewer)
print "Sewer Imported"
os.remove(sewer_out)
#End Sewer

#Street
streetname = "ZonarStreet" + tendtime
streetout1 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\Street\\Temp\\" + streetname + "_1" + ".csv"
streetout2 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\Street\\Temp\\" + streetname + "_2" + ".csv"
streetout3 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\Street\\Temp\\" + streetname + "_5" + ".csv"
streetout4 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\Street\\" + streetname + "" + ".csv"
streeturl1 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Street%20-%20Grissum" + "&starttime=" + tstarttime + "&endtime=" + tendtime
streeturl2 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Street%20Sweepers%20-%20Grissum" + "&starttime=" + tstarttime + "&endtime=" + tendtime
urllib.urlretrieve(streeturl1, streetout1)
urllib.urlretrieve(streeturl2, streetout2)
fstreets = streetout1
streetinputs = [streetout2]
opstreets = open(streetout3, 'wb')
output = csv.writer(opstreets, delimiter =',')
streetfiles = []
op1streets = open(fstreets, 'rb')
rdstreets = csv.reader(op1streets, delimiter = ',')
for rows in rdstreets:
    streetfiles.append(rows)
for files2s in streetinputs:
    op2streets = open(files2s, 'rb')
    rd2streets = csv.reader(op2streets, delimiter = ',')
    rd2streets.next()
    for row2s in rd2streets:
        streetfiles.append(row2s)
    op2streets.close()
output.writerows(streetfiles)
opstreets.close()
op1streets.close()
with open(streetout3, 'rb') as csvinput2:
    with open(streetout4, 'wb') as csvoutput2:
        reader2 = csv.reader(csvinput2)
        writer2 = csv.writer(csvoutput2)
        wr2 = []
        row02 = reader2.next()
        row02.append('Location')
        for x in range(0,12):
            del row02[17]
        wr2.append(row02)
        for row in reader2:
            row.append(lookup[row[1]])
            ept2 = int(row[3])
            convt2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept2))
            row[2] = convt2
            for x in range(0,12):
                del row[17]
            wr2.append(row)
        writer2.writerows(wr2)
print "Streets Imported"
os.remove(streetout1)
os.remove(streetout2)
os.remove(streetout3)
#End Street

#Solid Waste
solidwastename = "ZonarSolidWaste" + tendtime
solid_out = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\SolidWaste\\Temp\\" + solidwastename + "" + ".csv"
solid_url = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Solid%20Waste%20-%20Grissum" + "&starttime=" + tstarttime + "&endtime=" + tendtime
urllib.urlretrieve(solid_url, solid_out)
solid_write = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\TwoMonth\\SolidWaste\\" + solidwastename + "" + ".csv"
with open(solid_out, 'rb') as solidinput:
    with open(solid_write, 'wb') as solidoutput:
        readersolid = csv.reader(solidinput)
        writersolid = csv.writer(solidoutput)
        SW = []
        rowsolid = readersolid.next()
        rowsolid.append('Location')
        for x in range(0,12):
            del rowsolid[17]
        SW.append(rowsolid)
        for row in readersolid:
            row.append("Solid Waste")
            ept = int(row[3])
            convt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept))
            row[2] = convt
            for x in range(0,12):
                del row[17]
            SW.append(row)
        writersolid.writerows(SW)
os.remove(solid_out)
print "Solid Imported"
#End Solid Waste

#arcpy.SetParameter(1, fcout)
endtime = datetime.datetime.now()

print 'It took', endtime-start, 'seconds.'
#print allname3

print ("")
print ("")
