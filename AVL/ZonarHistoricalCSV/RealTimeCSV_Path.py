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
import threading

arcpy.env.overwriteOutput = True
outputspace = "C:\\Users\\gisbatch\\AppData\\Roaming\\ESRI\\Desktop10.5\\ArcCatalog\\ScriptAdmin.sde"
sewerFC = outputspace + "\\City.DBO.AVL\\City.DBO.CurrentSewer"
solidFC = outputspace + "\\City.DBO.AVL\\City.DBO.CurrentSolidWaste"
waterlightFC = outputspace + "\\City.DBO.AVL\\City.DBO.CurrentWaterLight"
streetFC = outputspace + "\\City.DBO.AVL\\City.DBO.CurrentStreet"
fields = ['SHAPE', 'asset_id', 'asset_no', 'date', 'time', 'speed', 'heading', 'reason', 'distance', 'latitude', 'longitude', 'zone', 'address', 'odometer', 'exsid', 'acceleration', 'status', 'location', 'subtype']

tstarttime = ""
tendtime = ""
lookuploc = {}
lookupstype = {}

sem = threading.Lock()

##def WaterLight():
##    global lookuploc
##    global lookupstype
##    global waterlightFC
##    global fields
##    global sem
##    global tstarttime
##    global tendtime
##
##    # -------------
##    #WaterLight ---
##    #allname = "ZonarWaterLight" + tendtime
##    allname = "waterlight"
##    waterlight_out1 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\Temp\\" + allname + "_1" + ".csv"
##    waterlight_out2 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\Temp\\" + allname + "_2" + ".csv"
##    waterlight_out3 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\Temp\\" + allname + "_3" + ".csv"
##    waterlight_out4 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\Temp\\" + allname + "_4" + ".csv"
##    waterlight_out = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\Temp\\" + allname + "_5" + ".csv"
##    waterlight_url1 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Electric%20Distribution" + "&starttime=" + tstarttime + "&endtime=" + tendtime
##    waterlight_url2 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Electric%20Utility%20Services" + "&starttime=" + tstarttime + "&endtime=" + tendtime
##    waterlight_url3 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Water%20Distribution" + "&starttime=" + tstarttime + "&endtime=" + tendtime
##    waterlight_url4 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Water%20Light%20Engineering" + "&starttime=" + tstarttime + "&endtime=" + tendtime
##    urllib.urlretrieve(waterlight_url1, waterlight_out1)
##    urllib.urlretrieve(waterlight_url2, waterlight_out2)
##    urllib.urlretrieve(waterlight_url3, waterlight_out3)
##    urllib.urlretrieve(waterlight_url4, waterlight_out4)
##    waterlight_write = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\" + allname + "" + ".csv"
##
##    f = waterlight_out1
##    waterlightinputs = [waterlight_out3, waterlight_out2, waterlight_out4]
##    op = open(waterlight_out, 'wb')
##    output = csv.writer(op, delimiter =',')
##    waterlightfiles = []
##    op1 = open(f, 'rb')
##    rd = csv.reader(op1, delimiter = ',')
##    row0 = rd.next()
##    waterlightfiles.append(row0)
##    for row in rd:
##        waterlightfiles.append(row)
##    for files2 in waterlightinputs:
##        op2 = open(files2, 'rb')
##        rd2 = csv.reader(op2, delimiter = ',')
##        rd2.next()
##        for row2 in rd2:
##            waterlightfiles.append(row2)
##        op2.close()
##    output.writerows(waterlightfiles)
##    op.close()
##    op1.close()
##
##    sem.acquire()
##    with open(waterlight_out, 'rb') as csvinput:
##        with arcpy.da.InsertCursor(waterlightFC,fields) as cur:
##            reader = csv.reader(csvinput)
##            reader.next()
##            for row in reader:
##                for x in range(0,13):
##                    del row[16]
##                a = (float(row[9]),float(row[8]))
##                row.append(lookuploc[row[1]])
##                row.append(lookupstype[row[1]])
##                ept = int(row[3])
##                convt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept))
##                row[2] = convt
##                row.insert(0, a)
##                cur.insertRow(row)
##    sem.release()
##
##    os.remove(waterlight_out1)
##    os.remove(waterlight_out3)
##    os.remove(waterlight_out2)
##    os.remove(waterlight_out4)
##    os.remove(waterlight_out)
##    #End WaterLight
##
##    return
##
##def Sewer():
##    global lookuploc
##    global lookupstype
##    global sewerFC
##    global fields
##    global sem
##    global tstarttime
##    global tendtime
##
##    # --------
##    #Sewer ---
##    #sewername = "ZonarSewer" + tendtime
##    sewername = "sewer"
##    sewer_out1 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Sewer\\Temp\\" + sewername + "_1" + ".csv"
##    sewer_out = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Sewer\\Temp\\" + sewername + "" + ".csv"
##    sewer_url = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Sewer%20and%20Stormwater%20-%20WWTP" + "&starttime=" + tstarttime + "&endtime=" + tendtime
##    urllib.urlretrieve(sewer_url, sewer_out1)
##    sewer_write = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Sewer\\" + sewername + "" + ".csv"
##
##    fsewer = sewer_out1
##    opsewer = open(sewer_out, 'wb')
##    output = csv.writer(opsewer, delimiter =',')
##    sewerfiles = []
##    op1sewer = open(fsewer, 'rb')
##    rdsewer = csv.reader(op1sewer, delimiter = ',')
##    row0 = rdsewer.next()
##    sewerfiles.append(row0)
##    for rows in rdsewer:
##        sewerfiles.append(rows)
##    output.writerows(sewerfiles)
##    opsewer.close()
##    op1sewer.close()
##
##    sem.acquire()
##    with open(sewer_out, 'rb') as sewerinput:
##        with arcpy.da.InsertCursor(sewerFC,fields) as cur2:
##            readersewer = csv.reader(sewerinput)
##            readersewer.next()
##            for row in readersewer:
##                for x in range(0,13):
##                    del row[16]
##                a2 = (float(row[9]),float(row[8]))
##                row.append(lookuploc[row[1]])
##                row.append(lookupstype[row[1]])
##                ept = int(row[3])
##                convt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept))
##                row[2] = convt
##                row.insert(0, a2)
##                cur2.insertRow(row)
##    sem.release()
##
##    os.remove(sewer_out)
##    os.remove(sewer_out1)
##    #End Sewer
##
##    return

def Street():
    global lookuploc
    global lookupstype
    global streetFC
    global fields
    global sem
    global tstarttime
    global tendtime

    # ---------
    #Street ---
    #streetname = "ZonarStreet" + tendtime
    streetname = "street"
    street_out1 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Street\\Temp\\" + streetname + "_1" + ".csv"
    street_out2 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Street\\Temp\\" + streetname + "_2" + ".csv"
    street_out = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Street\\Temp\\" + streetname + "_3" + ".csv"
    street_url1 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Street%20-%20Grissum" + "&starttime=" + tstarttime + "&endtime=" + tendtime
    street_url2 = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Street%20Sweepers%20-%20Grissum" + "&starttime=" + tstarttime + "&endtime=" + tendtime
    urllib.urlretrieve(street_url1, street_out1)
    urllib.urlretrieve(street_url2, street_out2)
    street_write = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Street\\" + streetname + "" + ".csv"

    fstreets = street_out1
    streetinputs = [street_out2]
    opstreets = open(street_out, 'wb')
    output = csv.writer(opstreets, delimiter =',')
    streetfiles = []
    op1streets = open(fstreets, 'rb')
    rdstreets = csv.reader(op1streets, delimiter = ',')
    row0 = rdstreets.next()
    streetfiles.append(row0)
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

    sem.acquire()
    with open(street_out, 'rb') as streetinput:
        with open(street_write, 'wb') as streetoutput2:
            reader2 = csv.reader(streetinput)
            writer2 = csv.writer(streetoutput2)
            wr2 = []
            row02 = reader2.next()
            row02.append('Location')
            row02.append('Subtype')
            row02.append('Starttime')
            row02.append('Endtime')
            for x in range(0,12):
                del row02[17]
            wr2.append(row02)
            for row in reader2:
                row.append(lookuploc[row[1]])
                row.append(lookupstype[row[1]])
                row.append(tstarttime)
                row.append(tendtime)
                ept2 = int(row[3])
                convt2 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept2))
                row[2] = convt2
                for x in range(0,12):
                    del row[17]
                wr2.append(row)
            writer2.writerows(wr2)
##        with arcpy.da.InsertCursor(streetFC,fields) as cur3:
##            readerstreet = csv.reader(streetinput)
##            readerstreet.next()
##            for row in readerstreet:
##                for x in range(0,13):
##                    del row[16]
##                a3 = (float(row[9]),float(row[8]))
##                row.append(lookuploc[row[1]])
##                row.append(lookupstype[row[1]])
##                ept = int(row[3])
##                convt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept))
##                row[2] = convt
##                row.insert(0, a3)
##                cur3.insertRow(row)
    sem.release()

##    os.remove(street_out1)
##    os.remove(street_out2)
##    os.remove(street_out)
    #End Street

    return

##def SolidWaste():
##    global lookuploc
##    global lookupstype
##    global solidFC
##    global fields
##    global sem
##    global tstarttime
##    global tendtime
##
##    # --------------
##    #Solid Waste ---
##    #solidwastename = "ZonarSolidWaste" + tendtime
##    solidwastename = "solidwaste"
##    solid_out1 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\SolidWaste\\Temp\\" + solidwastename + "_1" + ".csv"
##    solid_out = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\SolidWaste\\Temp\\" + solidwastename + "" + ".csv"
##    solid_url = "http://col2225.zonarsystems.net/interface.php?action=showposition&logvers=3.6&username=gisadmins&password=admin1234&operation=path&format=csv&version=2&location=Solid%20Waste%20-%20Grissum" + "&starttime=" + tstarttime + "&endtime=" + tendtime
##    urllib.urlretrieve(solid_url, solid_out1)
##    solid_write = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\SolidWaste\\" + solidwastename + "" + ".csv"
##
##    fsolid = solid_out1
##    opsolid = open(solid_out, 'wb')
##    output = csv.writer(opsolid, delimiter =',')
##    solidfiles = []
##    op1solid = open(fsolid, 'rb')
##    rdsolid = csv.reader(op1solid, delimiter = ',')
##    row0 = rdsolid.next()
##    solidfiles.append(row0)
##    for rows in rdsolid:
##        solidfiles.append(rows)
##    output.writerows(solidfiles)
##    opsolid.close()
##    op1solid.close()
##
##    sem.acquire()
##    with open(solid_out, 'rb') as solidinput:
##        with arcpy.da.InsertCursor(solidFC,fields) as cur4:
##            readersolid = csv.reader(solidinput)
##            readersolid.next()
##            for row in readersolid:
##                for x in range(0,13):
##                    del row[16]
##                a4 = (float(row[9]),float(row[8]))
##                row.append(lookuploc[row[1]])
##                row.append(lookupstype[row[1]])
##                ept = int(row[3])
##                convt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept))
##                row[2] = convt
##                row.insert(0, a4)
##                cur4.insertRow(row)
##    sem.release()
##
##    os.remove(solid_out)
##    os.remove(solid_out1)
##    #End Solid Waste'
##
##    return

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)

def looker():
    global lookuploc
    global lookupstype

    xml_table = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\ALL\\" + "lookup_table" + ".xml"
    xml_url = "https://col2225.zonarsystems.net/interface.php?action=showopen&operation=showassets&username=gisadmins&password=admin1234&format=xml"
    urllib.urlretrieve(xml_url, xml_table)
    tree = ET.parse(xml_table)
    root = tree.getroot()
    lookuploc = {}
    lookupstype = {}
    for member in root.findall('asset'):
        fleet = member.find('fleet').text
        location = member.find('location').text
        subtype = member.find('subtype').text
        lookuploc[fleet] = location
        lookupstype[fleet] = subtype

def main():
    global tendtime
    global tstarttime

    start = datetime.datetime.now()
    endtime = int(time.time() -120)
    starttime = endtime - 10
    tstarttime = str(starttime)
    tendtime = str(endtime)

    while True:
        start = datetime.datetime.now()
        looker()

        #Make Threads
##        SolidWaste_Thread = Thread(SolidWaste)
        Street_Thread = Thread(Street)
##        Sewer_Thread = Thread(Sewer)
##        WaterLight_Thread = Thread(WaterLight)
        print "Make Threads"

##        #Start Threads
##        SolidWaste_Thread.start()
        Street_Thread.start()
##        Sewer_Thread.start()
##        WaterLight_Thread.start()
        print "Start Threads"

        #Join Threads
##        SolidWaste_Thread.join()
        Street_Thread.join()
##        Sewer_Thread.join()
##        WaterLight_Thread.join()
        print "Join Threads"

        time.sleep(10)
        starttime = endtime+1
        tstarttime = str(starttime)

        endtime = int(time.time() - 120)
        tendtime = str(endtime)


        print 'All imported'
        end = datetime.datetime.now()
        print 'It took', end-start, 'seconds.'
if __name__ == '__main__':
    main()
