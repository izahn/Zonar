##Zane's login credentials to zonar, encrypted behind another password
##City Of Coumbia GIS
##Zane Kullman
##No Longer Updated since 2/15, see auth.py
##DO NOT SHARE##

import getpass

def zaneAuth():
    secretKey = getpass.getpass("Enter the secret key: ")
    username = "zakullma"
    ##OTP encrypted PW, requires the secret key to be user entered (see above). This password is only for zonar
    encryptedPW = '\x1c\x0e\x1c\x18\x1e\x02\x1c\x17P'
    xorWord = lambda ss,cc: ''.join(chr(ord(s)^ord(c)) for s,c in zip(ss,cc*100))
    return {'username':username, "password":xorWord(encryptedPW, secretKey)}
