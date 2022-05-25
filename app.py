from flask import Flask, send_from_directory,render_template
import time
import RPi.GPIO as GPIO

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

from flask import Flask, request, redirect, send_from_directory, render_template

from multiprocessing import Process, Value, Pipe, Array,Manager

from ctypes import c_char_p

now = datetime.now().time() # timeobject

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



def nfcLoop(x):
    now=datetime.now().time() 
    try:
        pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        #pn532 = PN532_I2C(debug=False, reset=20, req=16)
        #pn532 = PN532_UART(debug=False, reset=20)
        
        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC card...')
        scanned_id = ''
        last_scanned = ''
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            
            #data = pn532.ntag2xx_read_block
            # Try again if no card is available.
            if uid is None:
                continue
            #print('Found card with UID:', [hex(i) for i in uid])
            base64_bytes = base64.b64encode(uid)     
            
            f = open("static/Attendance.json","r")
            attd = json.loads(f.read())

            gotName = False;
            for item in attd['students']:
                if(item['uid'] == base64_bytes.decode("ascii")):              
                    print("1:", item['student'])
                    f.close()
                    scanned_id = item['student']

                    last_scanned = scanned_id
                    string.value = last_scanned

                    now = datetime.now().time() # timeobject
                    item['time'] = str(now)
                    with open("static/Attendance.json","w") as outfile:
                        outfile.write(json.dumps(attd))
                    gotName= True
                    break;
            

            #we have not found the student in the list
            #add a new entry to the json
            if not gotName:
                f = open("static/Attendance.json","w")
                attd["students"].append({'uid':base64_bytes.decode("ascii"),'student':'Jack','time':str(now)})
            
                print(attd["students"])
            
                f.write(json.dumps(attd))
            
                f.close()          
                
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()



@app.route("/")

def home():
    return render_template ("index.html")


@app.route("/static/<path:path>")
def send_static(path):
       return send_from_directory('static',path)

@app.route("/checkin",methods = ["GET","POST"])
def checkin():
    temp = string.value
    string.value=''
    return temp

@app.route("/platform", methods = ["POST"])
def updatePlatform():
    #write code here to make a POST request
    #with authority to the nuvu platform attendance
    print("hello")
    return redirect("/checkin")

if __name__ == '__main__':
   manager = Manager()
   string = manager.Value(c_char_p, "Hello")
   p = Process(target=nfcLoop, args=(string,))
   p.start()
   app.run(debug=True, use_reloader=False)
   p.join()
   


