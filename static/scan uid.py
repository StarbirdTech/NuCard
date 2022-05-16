"""
This example shows connecting to the PN532 with I2C (requires clock
stretching support), SPI, or UART. SPI is best, it uses the most pins but
is the most reliable and universally supported.
After initialization, try waving various 13.56MHz RFID cards over it!
"""
from datetime import datetime
import time,json, base64
import RPi.GPIO as GPIO

from pn532 import *

now = datetime.now().time() # timeobject

if __name__ == '__main__':
    try:
        pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        #pn532 = PN532_I2C(debug=False, reset=20, req=16)
        #pn532 = PN532_UART(debug=False, reset=20)
        
        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC card...')
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
            
            #data = pn532.ntag2xx_read_block
            # Try again if no card is available.
            if uid is None:
                continue
            print('Found card with UID:', [hex(i) for i in uid])
            base64_bytes = base64.b64encode(uid)     
            
            
            f = open("/static/Attendance.json","r")
            attd = json.loads(f.read())

            gotName = False;
            for item in attd['students']:
                if(item['uid'] == base64_bytes.decode("ascii")):              
                    print(item['student'])
                    f.close()
                    now = datetime.now().time() # timeobject
                    item['time'] = str(now)
                    with open("/static/Attendance.json","w") as outfile:
                        outfile.write(json.dumps(attd))
                    gotName= True
                    break;
              
            
            #we have not found the student in the list
            #add a new entry to the json
            if not gotName:
                f = open("/static/Attendance.json","w")
                attd["students"].append({'uid':base64_bytes.decode("ascii"),'student':'Jack','time':str(now)})
            
                print(attd["students"])
            
                f.write(json.dumps(attd))
            
                f.close()
                #attd["students"] = 

            #1st create a python object that has
                #the UID from the nfc chip
                #the student name from the nfc chip
                #the current time
                
            #2nd append that python to the json 'students' array            
            
            
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
