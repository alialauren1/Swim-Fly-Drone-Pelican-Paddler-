"""!
@file pressure_sensor.py
    This file is a class that implements Pressure Sensor: SSCMANV030PA2A3 from Honeywell
    It allows for initialization of setpoint (in [psi]), and Pressure and Temperature in units of counts.
    
    This class can:
    - Convert setpoint in [psi] to units of counts.
    - Read the pressure and temperature in [counts]
    - Convert pressure in [psi] and temperature in [F]
    - Convert the pressure to corresponding depth under water [ft]
  
@author Alia Wolken, Eduardo Santos, Andrew Jwaideh
@date   2024-March-15 
"""

import pyb
import utime
import struct

class PressureSensor:
    """!
    This class represents pressure sensor data collection and processing. 
    @author Alia Wolken, Eduardo Santos, Andrew Jwaideh
    """
    
    def __init__(self,Setpoint,P_Counts,T_Counts):
        """!
        Here we initialize the PressureSensor Object. Where we have the
        following:
        
        @param Setpoint: The desired pressure setpoint, in [psi]
        @param P_Counts: The raw pressure data in counts
        @param T_Counts: The raw temperature data in counts
        
        """           
        self.I2C_obj = pyb.I2C(1,pyb.I2C.CONTROLLER,baudrate=100000)
        
        # scan I2C bus to make sure 1 device talking
        sensor_addr = self.I2C_obj.scan() # Check for devices on bus, output is I2C Device Address
        #Sensor_Addr = 0x28 # I2C Addr From Data Sheet
        
        # COLLECT INITIAL DATA VALUES
        self.byte_array = bytearray(7)
        data = self.I2C_obj.recv(self.byte_array,0x28) # receive data from I2C, store in bytearray
        # COLLECT INTIAL P VALUE
        self.init_p = data[1] | ((data[0] & 0x3F) << 8) # 16bit pressure val
        # COLLECT INITIAL STATUS
        status = (data[0] & 0xC0) >> 6 # extract first byte, shift 6 positions and store
        print(f'{status=}') 
        
    def readP_Raw(self):
        """!
        Reads Raw Status, Pressure, and Temperature Data from the sensor.
        
        @param returns: A tuple containing raw pressure and temperature data.
        """
        
        # need to keep pressure values in raw counts to have max precision
        
        data = self.I2C_obj.recv(self.byte_array,0x28) # receive data from I2C, store in bytearray

        status1 = '{0:08b}'.format(data[0]) # extract first byte 
        status2 = (data[0] & 0xC0) >> 6 # extract first byte, shift 6 positions and store
        #print(f'{status1=},{status2=}')
        
        #print('first p val',self.init_pressure)

        pressCounts = data[1] | ((data[0] & 0x3F) << 8) # 16bit pressure val
        tempCounts = ((data[3] & 0xE0) >> 5) | (data[2] << 3) # 12bit temp val
        
        return pressCounts, tempCounts
    
    def PtoRawP(self,Setpoint): #pressure conversion from pressure [psi] to raw counts
        """!
        Converts setpoint pressure from units of psi to counts.
        
        @param Setpoint: The desired pressure setpoint in psi.
        @param return: The pressure setpoint in raw counts.
        """
        P_MAX = 30 #[psi]
        P_MIN = 0  #[psi]
        O_MAX = 0.9 * pow(2,14) # Max output val from sensor
        O_MIN = 0.1 * pow(2,14) # Max input val from sensor
        setpoint_raw = ((Setpoint)-P_MIN)*(O_MAX - O_MIN)/(P_MAX - P_MIN)+O_MIN
        return setpoint_raw
    
    def RawtoData_P(self,P_Counts): #pressure conversion from raw counts to pressure [psi]
        """!
        Converts raw pressure data in units of counts to [psi].
        Then pressure difference from initial pressure and thus displacement depth.
        
        @param P_counts: Raw pressure data in counts.
        @param return: A tuple containing pressure, pressure difference, depth, and initial pressure.
        """
        
        P_MAX = 30 #[psi]
        P_MIN = 0  #[psi]
        O_MAX = 0.9 * pow(2,14) # Max output val from sensor 
        O_MIN = 0.1 * pow(2,14) # Min output val from sensor
        
        # INITIAL PRESSURE [COUNTS -> PSI] FROM EQUN 2 DATA SHEET
        self.init_pressure = (((self.init_p - O_MIN) * (P_MAX - P_MIN) / (O_MAX - O_MIN)) + P_MIN) #[psi]
        
        # CURRENT PRESSURE [COUNTS -> PSI] FROM EQUN 2 DATA SHEET
        pressure = ((P_Counts - O_MIN) * (P_MAX - P_MIN) / (O_MAX - O_MIN) + P_MIN) #[psi]
        self.p_diff = pressure - self.init_pressure # [psi] pressure different from initial 

        # DEPTH FROM INIT PRESSURE (DISPLACEMENT DEPTH)
        gravity = 32.17405 # [ft/s^2]
        density = 62.3 # [lb/ft^3]
        depth = self.p_diff*144*32.174/(gravity*density) # [ft] 
        
        return pressure, self.p_diff, depth, self.init_p
    
    def RawtoData_T(self,T_Counts): #pressure conversion from raw counts to pressure [psi]
        """!
        Converts raw temperature data to Fahrenheit.
        
        @param T_Counts: Raw temperature data in counts.
        @param return: Temperature in Fahrenheit.
        """
        
        # CURRENT TEMP [COUNTS -> FAHRENHEIT]
        T_COUNTS = pow(2,11) - 1
        # EQUATION 3 FROM DATASHEET
        temperature = (T_Counts*200/2047 - 50)*(9/5)+32  #[Fahrenheit]

        return temperature
   
if __name__ == "__main__":
        
    # init
    setpoint = 15.3
    sensor_obj = PressureSensor(0,0,0)

    while True:
        try:
            utime.sleep (0.5) # sleep 1 second

            rawP_val, rawT_val = sensor_obj.readP_Raw()
            pressure, pressure_diff, depth, init_p = sensor_obj.RawtoData_P(rawP_val)
            temp = sensor_obj.RawtoData_T(rawT_val)
            
            print('--------------------')
            print(f'{setpoint=}')
            print('Raw Setpoint =',sensor_obj.PtoRawP(setpoint))
            print('---')
            print('Raw P Val = ',rawP_val)
            print(f'{pressure=} ')
            print(f'{pressure_diff=} ')
            print(f'{temp=}')
            print(f'{depth=}')
            print(f'{init_p=}')
            #pressure1, pressure_diff1, depth1, init_p1, initial_p_cob = sensor_obj.RawtoData_P(init_p)
            #print(initial_p_cob)
           
        except KeyboardInterrupt:
            break
    