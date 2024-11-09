import pyb
import utime
import struct


# init
I2C_obj = pyb.I2C(1,pyb.I2C.CONTROLLER,baudrate=100000)

#Sensor_Addr = 0x28 # I2C Addr From Data Sheet  
byte_array = bytearray(7)
# scan I2C bus to make sure 1 device talking
sensor_addr = I2C_obj.scan() # Check for devices on bus, output is I2C Device Address

# pull data
data = I2C_obj.recv(byte_array,sensor_addr)

status = '{0:08b}'.format(data[0])
print(f'{status=}')

while True:
    utime.sleep (1) # sleep 1 second
    
    try:
        #addr = readSensor()
        byte_array = bytearray(7)
        
        # pull data
        data = I2C_obj.recv(byte_array,addr)

        status = '{0:08b}'.format(data[0])
        print(f'{status=}')
        
        # send a command of three bytes to sensor
        # Define Command: 0xAA, 0x00, 0x00
        # write command to sensor at register addr
        
        # wait 5-10 ms
        
        # read from sensor (maybe with .read)
        # read 7 bytes for addr
        

        
        pass
    
    except KeyboardInterrupt:
        break
