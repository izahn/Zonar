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
import os
import xml.etree.ElementTree as ET
import threading
import Tkinter as tk

GUI = 0
bPress = False
bQuit = False

mainThread = 0
guiThread = 0

timeDelay = 60*10
timeWindow = 10

#The function that is looped by the program.
#This is given one thread each cycle, while the gui also gets one thread each cycle
def looper():
    global bPress
    global bQuit
    global timeDelay
    global timeWindow
    while bQuit == False:
        if bPress == True:
            errlog = open("C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\errors.log", "w")
            try:
                allname4 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\ALL\\" + "Table21" + ".xml"
                xml_url = "https://col2225.zonarsystems.net/interface.php?action=showopen&operation=showassets&username=gisadmins&password=admin1234&format=xml"
                urllib.urlretrieve(xml_url, allname4)
                tree = ET.parse(allname4)
                root = tree.getroot()
                lookuploc = {}
                lookupstype = {}
                for member in root.findall('asset'):
                    fleet = member.find('fleet').text
                    location = member.find('location').text
                    subtype = member.find('subtype').text
                    lookuploc[fleet] = location
                    lookupstype[fleet] = subtype
            except Exception as e:
                errlog.write("Failed creating lookup table: {0}\n".format(str(e)))

            endtime = int(time.time() - timeDelay)
            starttime = endtime - timeWindow
            tstarttime = str(starttime)
            tendtime = str(endtime)

            start = int(time.time())

            req_list = {"action": "showposition",
            "logvers": "3.6",
            "username": "gisadmins",
            "password": "admin1234",
            "operation": "path",
            "format": "csv",
            "version": "2",
            "starttime": tstarttime,
            "endtime": tendtime}

            #WaterLight
            try:
                allname = "ZonarWaterLight" + tendtime
                allname2_1 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\Temp\\" + allname + "_1" + ".csv"
                allname2_2 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\Temp\\" + allname + "_2" + ".csv"
                allname2_3 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\Temp\\" + allname + "_3" + ".csv"
                allname2_4 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\Temp\\" + allname + "_4" + ".csv"
                allname2 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\Temp\\" + allname + "_5" + ".csv"
                allname3 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\WaterLight\\" + allname + "" + ".csv"

                req_list["location"] = "Electric Distribution"
                req_params = urllib.urlencode(req_list)
                csv_url1 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

                req_list["location"] = "Electric Utility Services"
                req_params = urllib.urlencode(req_list)
                csv_url2 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

                req_list["location"] = "Water Distribution"
                req_params = urllib.urlencode(req_list)
                csv_url3 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

                req_list["location"] = "Water Light Engineering"
                req_params = urllib.urlencode(req_list)
                csv_url4 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

                urllib.urlretrieve(csv_url1, allname2_1)
                urllib.urlretrieve(csv_url2, allname2_2)
                urllib.urlretrieve(csv_url3, allname2_3)
                urllib.urlretrieve(csv_url4, allname2_4)

                f = allname2_1
                csvinputs = [allname2_3, allname2_2, allname2_4]
                appendCsvs(f, csvinputs, allname2)
                writeToOutput(allname2, allname3, lookuploc, lookupstype)
                os.remove(allname2_1)
                os.remove(allname2_3)
                os.remove(allname2_2)
                os.remove(allname2_4)
                os.remove(allname2)
                print "WaterLight Imported"
            except Exception as e:
                errlog.write("Failed WaterLight: {0}\n".format(str(e)))
            #End WaterLight

            #Sewer
            try:
                sewername = "ZonarSewer" + tendtime
                sewer_out = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Sewer\\Temp\\" + sewername + "" + ".csv"

                req_list["location"] = "Sewer and Stormwater - WWTP"
                req_params = urllib.urlencode(req_list)
                sewer_url = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

                urllib.urlretrieve(sewer_url, sewer_out)
                sewer_write = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Sewer\\" + sewername + "" + ".csv"
                writeToOutput(sewer_out, sewer_write, lookuploc, lookupstype)
                print "Sewer Imported"
                os.remove(sewer_out)
            except Exception as e:
                errlog.write("Failed Sewer: {0}\n".format(str(e)))
            #End Sewer

            #Street
            try:
                streetname = "ZonarStreet" + tendtime
                streetout1 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Street\\Temp\\" + streetname + "_1" + ".csv"
                streetout2 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Street\\Temp\\" + streetname + "_2" + ".csv"
                streetout3 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Street\\Temp\\" + streetname + "_5" + ".csv"
                streetout4 = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\Street\\" + streetname + "" + ".csv"

                req_list["location"] = "Street - Grissum"
                req_params = urllib.urlencode(req_list)
                streeturl1 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

                req_list["location"] = "Street Sweepers - Grissum"
                req_params = urllib.urlencode(req_list)
                streeturl2 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

                urllib.urlretrieve(streeturl1, streetout1)
                urllib.urlretrieve(streeturl2, streetout2)

                fstreets = streetout1
                streetinputs = [streetout2]
                appendCsvs(fstreets, streetinputs, streetout3)
                writeToOutput(streetout3, streetout4, lookuploc, lookupstype)
                os.remove(streetout1)
                os.remove(streetout2)
                os.remove(streetout3)
                print "Streets Imported"
            except Exception as e:
                errlog.write("Failed Street: {0}\n".format(str(e)))
            #End Street

            #Solid Waste
            try:
                solidwastename = "ZonarSolidWaste" + tendtime
                solid_out = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\SolidWaste\\Temp\\" + solidwastename + "" + ".csv"

                req_list["location"] = "Solid Waste - Grissum"
                req_params = urllib.urlencode(req_list)
                solid_url = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

                urllib.urlretrieve(solid_url, solid_out)
                solid_write = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\RealTime\\SolidWaste\\" + solidwastename + "" + ".csv"
                writeToOutput(solid_out, solid_write, lookuploc, lookupstype)
                os.remove(solid_out)
                print "Solid Imported"
            except Exception as e:
                errlog.write("Failed Solid Waste: {0}\n".format(str(e)))
            #End Solid Waste

            starttime = endtime+1
            tstarttime = str(starttime)

            endtime = int(time.time() - timeDelay)
            tendtime = str(endtime)

            endtime2 = int(time.time())
            print endtime2
            print start
            timedif = endtime2-start
            print timedif
            if timedif < 2:
                time.sleep(2)
                endtime = int(time.time() - timeDelay)
                tendtime = str(endtime)
                print ("Slept   {0}    {1}".format(tstarttime, tendtime))

            print 'It took', endtime2-start, 'seconds.'
            errlog.close()
        else:
            time.sleep(1)

#function called by looper to writeoutput for each vehicle to csvs
def writeToOutput(out, write, lookuploc, lookupstype):
    with open(out, 'rb') as fileIn:
        with open(write, 'wb') as fileOut:
            reader = csv.reader(fileIn)
            writer = csv.writer(fileOut)
            rowWriter = []
            row = reader.next()
            row.append('Location')
            row.append('Subtype')
            for x in range(0,12):
                del row[17]
            rowWriter.append(row)
            for row in reader:
                if(len(row) == 29):
                    row.append(lookuploc[row[1]])
                    row.append(lookupstype[row[1]])
                    ept = int(row[3])
                    convt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept))
                    row[2] = convt
                    for x in range(0,12):
                        del row[17]
                    rowWriter.append(row)
            writer.writerows(rowWriter)
    return

#function called before writeToOutput in the case that there are more than one
#csv inputs that must be appended together
def appendCsvs(f, csvinputs, out):
    op = open(out, 'wb')
    output = csv.writer(op, delimiter =',')
    csvfiles = []
    op1 = open(f, 'rb')
    rd = csv.reader(op1, delimiter = ',')
    for row in rd:
        csvfiles.append(row)
    for files in csvinputs:
        op2 = open(files, 'rb')
        rd2 = csv.reader(op2, delimiter = ',')
        rd2.next()
        for row2 in rd2:
            csvfiles.append(row2)
        op2.close()
    output.writerows(csvfiles)
    op.close()
    op1.close()
    return

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)

class App():
    def __init__(self, master):
        global bPress
        global GUI
        bPress = False

        self.button = tk.Button(GUI, text='START')
        self.button2 = tk.Button(GUI, text='STOP')
        self.button3 = tk.Button(GUI, text='QUIT (Safe Thread Destruction)', bg='red')
        self.button.bind("<Button-1>", self.setButton)
        self.button2.bind("<Button-1>", self.resetButton)
        self.button3.bind("<Button-1>", self.quitButton)

        GUI.grid_propagate(False)
        GUI.grid_rowconfigure(0, weight=1)
        GUI.grid_columnconfigure(0, weight=10)
        GUI.grid_columnconfigure(1, weight=10)
        GUI.grid_columnconfigure(2, weight=1)

        self.button.grid(row=1, column=0, sticky='nsew')
        self.button2.grid(row=1, column=1, sticky='nsew')
        self.button3.grid(row=1, column=2, sticky='nsew')

        txt_frm = tk.Frame(GUI, width=720, height=480)
        txt_frm.grid(row=0, column=0, columnspan=3, sticky='nsew')

        txt_frm.grid_propagate(False)
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)

        self.T = tk.Text(txt_frm, borderwidth=3, relief='sunken')
        self.T.grid(row=0, column=0, sticky='nsew')

        self.scroll = tk.Scrollbar(txt_frm, command=self.T.yview)
        self.scroll.grid(row=0, column=1, sticky='nsew')

        GUI.geometry("720x480")
        GUI.minsize(720,505)
        GUI.maxsize(720,505)

        self.master = master

    def setButton(self, event):
        global bPress
        bPress = True
        self.T.insert(tk.END, "Running...." + str(datetime.datetime.now()) + "\n")
        return

    def resetButton(self, event):
        global bPress
        bPress = False
        self.T.insert(tk.END, "Script has stopped." + str(datetime.datetime.now()) + "\n")
        return

    def quitButton(self, event):
        global bQuit
        global GUI
        bQuit = True
        GUI.destroy()
        return

def guiTH():
    global GUI
    GUI = tk.Tk()
    app = App(GUI)
    GUI.mainloop()

def main():
    global mainThread
    global guiThread
    mainThread = Thread(looper)
    guiThread = Thread(guiTH)
    guiThread.start()
    mainThread.start()
    guiThread.join()
    mainThread.join()

if __name__ == '__main__':
    main()




