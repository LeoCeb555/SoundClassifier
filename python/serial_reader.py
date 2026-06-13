import serial

#ser = serial.Serial('/dev/cu.usbmodem14103', 115200, timeout=1)
ser2 = serial.Serial('/dev/cu.usbmodem14203', 115200, timeout=1)

#if ser.is_open:
    #print(f"Connected to: {ser.port}")
if ser2.is_open:
    print(f"Connected to: {ser2.port}")

user = ""

while True:

    if(ser2.in_waiting > 0):

        line = ser2.readline()
        decoded_line = line.decode('utf-8').strip()
        print(decoded_line)