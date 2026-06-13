import serial

#ser = serial.Serial('/dev/cu.usbmodem14103', 115200, timeout=1)
ser2 = serial.Serial('/dev/cu.usbmodem14203', 115200, timeout=1)
ser3 = serial.Serial('/dev/cu.usbserial-0001', 115200, timeout=1)

#if ser.is_open:
    #print(f"Connected to: {ser.port}")
#if ser2.is_open:
    #print(f"Connected to: {ser2.port}")

if ser3.is_open:
    print(f"Connected to: {ser3.port}")

while True:

    if(ser3.in_waiting > 0):

        line = ser3.readline()
        line = line.decode('utf-8')
        feature_vector = line.replace("\r\n", "").split(",", 3)
        print(feature_vector)