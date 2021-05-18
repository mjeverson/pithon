import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
    ser.flush()
    
#     while True:
#         if ser.in_waiting > 0:
#             line = ser.readline().decode('utf-8').rstrip()
#             print(line)

    while True:
        print("writing packet")
#         packet = bytearray()
#         packet.append(0x00)
        b = b'\x01'
        print("about to write packet")
        print(b)
        ser.write(b)
        print("wrote packet")
        print(b)
        while not ser.in_waiting > 0:
            pass
        
        print("reading bytes")
#         line = ser.readline().decode('utf-8').rstrip()
#         print(line)
        line = ser.read(1)
        print(line)
        if line == b:
            print("VICTORY")
        time.sleep(1)