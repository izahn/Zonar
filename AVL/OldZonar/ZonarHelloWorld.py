##Zonar API Work
##Zane Kullman
##City Of Columbia GIS
##DO NOT SHARE##

import xml.etree.ElementTree as ET
import requests
import time

def zaneAuth():
    secretKey = getpass.getpass("Enter the secret key: ")
    username = "zakullma"
    ##OTP encrypted PW, requires the secret key to be user entered (see above). This password is only for zonar
    encryptedPW = '<\x1a\r\x07\x00\x0e9C\x13'
    xorWord = lambda ss,cc: ''.join(chr(ord(s)^ord(c)) for s,c in zip(ss,cc*100))
    return {'username':username, "password":xorWord(encryptedPW, secretKey)}

def fireRequest(Payload, Url):
    #Handle Errors here for the varrying status codes, (401, 404, 200-but-error) here
    #For now it'll just return data
    return requests.post(Url, data=Payload)

zonarUrl = "https://col2225.zonarsystems.net/interface.php"
auth = zaneAuth()

payload = auth #start with auth
payload['action'] = 'showposition'
payload['operation'] = 'current'
payload['format'] = 'xml'
payload['version'] = '2'
payload['logvers'] = '3'
payload['target'] = "25"
payload['reqtype'] = "dbid" #Need to figure out how to use fleet, right now it's based off a unique id

r = fireRequest(payload, zonarUrl)
doc = ET.fromstring(r.text)
print r.url
