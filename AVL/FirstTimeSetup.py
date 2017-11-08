##City Of Coumbia GIS
##Jeffrey King
##Zonar First Time Setup

import urllib
import os

print "Starting Zonar setup"

## Turn off Kaspersky Antivirus temporarily,
## or it will yell at you when you try this
url = 'https://bootstrap.pypa.io/get-pip.py'
path = 'C:\Python27'
dir_Pre = '\ArcGIS'
dir_Post = ''
dir_Post64 = ''
max_vers = 0
max_vers64 = 0

flag_64bit = 0
for root, dirs, files in os.walk(path):
    for folder in dirs:
        if (folder[:6] == dir_Pre[1:]):
            if (folder[6] != 'x' ):
                cur_vers = float(folder[6:])
                if (cur_vers > max_vers):
                    max_vers = cur_vers
                    dir_Post = folder[6:]
            else:
                cur_vers = float(folder[9:])
                flag_64bit = 1
                if (cur_vers > max_vers64):
                    max_vers64 = cur_vers
                    dir_Post64 = folder[6:]



print "You are using ArcMap version " + dir_Post

print "Pulling get-pip for easy installation"
urllib.urlretrieve(url, 'C:\Python27' + dir_Pre + dir_Post + '\get-pip.py')
os.system('C:\Python27' + dir_Pre + dir_Post + '\python C:\Python27' + dir_Pre + dir_Post + '\get-pip.py')

print "Installing Requests"
os.system('C:\Python27' + dir_Pre + dir_Post + '\Scripts\pip install requests')
os.system('C:\Python27' + dir_Pre + dir_Post + '\Scripts\pip install pyOpenSSL ndg-httpsclient pyasn1')

if (flag_64bit == 1):
    print "Pulling get-pip for easy installation (64 bit)"
    urllib.urlretrieve(url, 'C:\Python27' + dir_Pre + dir_Post64 + '\get-pip.py')
    os.system('C:\Python27' + dir_Pre + dir_Post64 + '\python C:\Python27' + dir_Pre + dir_Post64 + '\get-pip.py')

    print "Installing Requests (64 bit)"
    os.system('C:\Python27' + dir_Pre + dir_Post64 + '\Scripts\pip install requests')
    os.system('C:\Python27' + dir_Pre + dir_Post64 + '\Scripts\pip install pyOpenSSL ndg-httpsclient pyasn1')

print "Finished!"
