import utime
import cqueue

class Controller:
    def __init__(self, kp, set_point):
         self.kp = kp
         self.set_point = set_point
         #self.measured_output = 0
         self.start = utime.ticks_ms()
         

    def run(self, measured_output):
         #actuation value is Kp*(theta_set - enc2.read() value
         #self.measured_output = measured_output
        err = self.set_point - measured_output
        actuation = self.kp*err
        current_time = utime.ticks_ms()
         #if not self.time_value.full():
        self.time_passed = utime.ticks_diff(current_time, self.start)
        #self.time_value.put(self.time_passed)
        #self.position.put(measured_output)
         #utime.sleep_ms(10) # does this go in main or control?
        return actuation, self.time_passed, measured_output
        
    def set_setpoint(self, desired_set_point):
        self.set_point = float(desired_set_point)
        
    def set_Kp(self, desired_Kp):
        self.kp = desired_Kp
        