import pyb
import utime
import struct

class Sensor:
    
    def __init__(self,sensor_addr):     
        
        self.sensor_addr = sensor_addr
    
    def readPressureSensor(self):
        
        # pull data
        byte_array = bytearray(7)
        data = I2C_obj.recv(byte_array,self.sensor_addr)
        return data
        
        #status = '{0:08b}'.format(data[0])         
        
        #pressure = '{0:024b}'.format(data[1])
       
        #return status, pressure

if __name__ == '__main__':
           
    I2C_obj = pyb.I2C(1,pyb.I2C.CONTROLLER,baudrate=100000)

    # init
    #Sensor_Addr = 0x28 # I2C Addr From Data Sheet  
    # scan I2C bus to make sure 1 device talking
    sensor_addr = I2C_obj.scan() # Check for devices on bus, output is I2C Device Address   
    
    sensor_obj = Sensor(sensor_addr)
           
    while True:
        utime.sleep (1) # sleep 1 second

        try:
            # WHEN USING CLASS:
            #data = sensor_obj.readPressureSensor()
            
            # FOR NOW:
            byte_array = bytearray(7)
            data = I2C_obj.recv(byte_array,sensor_addr)
            status = '{0:08b}'.format(data[0])
            pressure = '{0:024b}'.format(data[1])
            print(f'{status=},{pressure=}')
            
            # Write the three bytes,
            # wait 5 ms
            # .read
            
            pass

        except KeyboardInterrupt:
            break