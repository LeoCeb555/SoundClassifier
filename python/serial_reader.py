import serial

ser = serial.Serial('/dev/cu.usbmodem14103', 115200, timeout=1)

if ser.is_open:
    print(f"Connected to: {ser.port}")

user = ""

while True:

    if(ser.in_waiting > 0):

        line = ser.readline()
        decoded_line = line.decode('utf-8').strip()
        print(decoded_line)