from logging import info
from bluepy.btle import Scanner, DefaultDelegate
import paho.mqtt.client as mqtt
import json
from pprint import pprint
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)
client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)
while (True):
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10.0,passive=True)

    for dev in devices:
        print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        data = dev.getScanData()
        info = data[0]
        description = data[1]
        pprint(info)
        pprint(description)
        date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
        payload = {
        "measurement": "advertisment",
        "tags": {
            "Device": dev.addr,
            "Flag": info[1],
            "type": description[1],


            },
        "time": date ,
        "fields": {
            "UUID_tag": description[2],
            "Flag_Value":info[2],

         }   
        }
        #a = [dev.addr,dev.rssi,data]
        OutData = json.dumps(payload)
        client.publish('raspberry/topic', payload=OutData, qos=0, retain=False)
        for (adtype, desc, value) in dev.getScanData():
            print ("  %s = %s" % (desc, value))
            print("data type of adtype is", type(adtype), "and its value is", adtype)
            print("data type of desc is", type(desc), "and its value is", desc)
            print("data type of value is", type(value), "and its value is", value)
