import pyb
import utime
import struct

I2C_obj = pyb.I2C(1,pyb.I2C.CONTROLLER,baudrate=100000)

# scan I2C bus to make sure 1 device talking
sensor_addr = I2C_obj.scan() # Check for devices on bus, output is I2C Device Address

