import time
import serial
import boto3
from credentials import AWS_KEY, AWS_SECRET, REGION
from flask import json

sqs = boto3.resource('sqs', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
queue = sqs.get_queue_by_name(QueueName='PiQueue')
out= ""                            
# configure the serial connections (the parameters differs on the device you are connecting to)
# Get the queue
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600
)

ser.isOpen()

print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

input=1
while 1 :
    for message in queue.receive_messages(MaxNumberOfMessages=1):
        data = message.body
        print message.body
        ######## Add code here to send thru serial. Use 'data' variable which is in json form ########
        if (data[2:7] == "Music"):
            print("sending m on serial \n")
            ser.write("m")
        elif (data[2:7] == "Snack"):
            print("sending t on serial \n")
            ser.write("t")
        else:
            print("input is NONE \n")
            input = None

        ######## Add code here to send thru serial. Use 'data' variable which is in json form ########
        message.delete()
        time.sleep(0.7)
    input=None
    if input == None:
            while ser.inWaiting() > 0:
                out += ser.read(size=21)

            if out != '':
                print ">>" + out
    temp,speed,rpm = out.split(",")
    if temp == 0:
        #Do nothing
    else:
        table.put_item(
           Item={
                    "Temperature": temp,
                    "Speed": speed,
                    "RPM": rpm,
                }
            )
        print "Pushed " + temp + " " + speed + " " + rpm
        out=''

