import serial
from time import sleep


def control_gate(serial,command):
    '''
    commend : int
    serial : serial.Serial("/dev/cu.usbmodem141401",9600)
    open : commend = 1
    close : commend = 0
    '''
    if command == 1:
        serial.write('H'.encode())
    elif command == 0:
        serial.write('L'.encode())

def show_LCD(serial, command, line, userName=""):
    '''
    commend : int
    line : int
    serial : serial.Serial("/dev/cu.usbmodem145401",9600)
    access : commend = 1
    error : commend = 0
    '''
    if command == 1:
        serial.write('A'.encode())
        # sleep(3)
        serial.write(userName.encode())
    elif command == 0:
        serial.write('B'.encode())
    

if __name__ == "__main__":
    s = serial.Serial("/dev/cu.usbmodem145401",9600)
    sleep(5)

    show_LCD(s,1,1,"abc")