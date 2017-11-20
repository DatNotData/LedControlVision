import serial
import time
arduino = serial.Serial('COM6', 9600)
f = open('buffer.txt', 'r')

def send_data(x):
    time.sleep(0.05)
    arduino.write(str.encode(x))

def get_data():
    f = open('buffer.txt','r')
    x = f.read()
    f.close()
    return x

while True:
    d = get_data()
    print(d)
    send_data(d)
