"""!
@file main.py
    This file runs two tasks, using two intershared variables and two queues.
    Task 1 processes and prints the data from the queues.
    Task 2 stores the data from the sensor into the queues.
    
    This file was modified from basic_tasks.py, author: JR Ridgely.
    The copyright from the basic_tasks file is included below. 
    
@author Alia Wolken, Eduardo Santos, Andrew Jwaideh
@date   2024-Sept-24

@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import utime
import pyb
import cotask
import task_share
import Closed_Loop_Controller

from motor_driver import motordriver
from Closed_Loop_Controller import Controller
from pressure_sensor import PressureSensor

def task1_print(shares):
# convert, and print data
    """!
    Task which:
    - Gets time and pressure out of a queue and the current Task 2 value out of a share.
    - Converts pressure from units of counts to [psi] and displays value along with corresponding depth underwater in [ft] and time duration.
    @param shares: A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    qTime, qPos, share_init_p, share_off = shares
        
    sensor_obj = PressureSensor(0,0,0)
    
    T1_state = 1
    S1_print = 1
    
    print('In Task 1')

    while True:
        
        if (T1_state == S1_print): # STATE 1: Done with Controller, Print Vals
            
            time = qTime.get() # Pull Time from Queue
            pos = qPos.get() # Pull Pressure from Queue

            pos_raw = (pos) 
            pressure, pressure_diff, depth, init_p  = sensor_obj.RawtoData_P(pos_raw) # Converts Pressure from [counts] to [psi] 
            share_init_p.put(init_p) 
            print(time,pressure,depth) # Prints time, pressure [psi] and depth [ft]
            
            T2_state = share_off.get() # Determine Task2's state
            if T2_state == 3: # Task2's state 3 indicates no data collection occuring, therefore, no printing needed
                T1_state = 2
            
        elif (T1_state == 2): # STATE 2: Dont Print Vals (no vals to print)
            T2_state = share_off.get() # Determine Task2's state
            if T2_state == 1: # Task2's state 1 indicates data is being collected
                T1_state = 1 # Transition back to printing data
            
        yield T1_state
        print('T1_state')
            
        
def task2_get(shares):
    """!
    Task that:
    - Converts desired setpoint from units of [psi] to counts using Pressure Sensor Class
    - Reads pressure sensor data in units of counts from Pressure Sensor Class.
    - Runs closed-loop controller with pressure counts comparing against setpoint to send motor PWM commands.
    - Puts time duration and pressure into queue 
    @param shares: A tuples of a share and queue from which gets data.
    """
    
    # get data
    qTime, qPos, share_init_p, share_off = shares[0], shares[1], shares[2], shares[3]

    moe2 = motordriver (pyb.Pin.board.PB10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3) # !!!!!!!!!!!!!! Had to update this 
    
    setpoint_p = 14.3 # Setpoint in [psi]
    sensor_obj = PressureSensor(setpoint_p,0,0) # Conversion in PressureSensor class from [psi] to counts
    setpoint_raw = sensor_obj.PtoRawP(setpoint_p) # Setpoint in [counts]
    
    # Paramters for the contoller
    Kp = 2
    controller_obj2 = Controller(Kp, setpoint_raw)
    
    print('Task 2')
    
    T2_state = 1
    S1_data = 1
    S2_off = 2
    S3_goback = 3
    counter = 0
    counter_s3 = 0
    final_counter = 0
    key = 0
    
    while True:
        
        if (T2_state == S1_data): # Collect Data & Run Closed Loop Controller
            initialP = share_init_p.get() # Initial Pressure taken during initialization of PressureSensor Class
            
            reader_p_value, temp_val = sensor_obj.readP_Raw() # Reads Raw P & T values
            PWM, time_passed, measured_output = controller_obj2.run(reader_p_value) # Runs Closed-Loop Controller 
            moe2.set_duty_cycle(-PWM) # Ajusts motor 2 postion 
            
            qTime.put(time_passed)       # stores time passed in queue to print 
            qPos.put(measured_output)    # stores measured pressure [counts] in queue to print 
            
            # If Desired Pressure is Reached
            if setpoint_raw-6 <= reader_p_value <= setpoint_raw+6: # Allowable range to consider "reaching" setpoint
                print('REACHED SETPOINTT!!')
                T2_state = 2 
                key = 1
            
            # If System has been Returned to Initial Pressure
            if (initialP-6 <= reader_p_value <= initialP+6) & key == 1: # Allowable range to consider "reaching" return pressure
                moe2.set_duty_cycle(0) # turn motor off
                PWM, time_passed, measured_output = controller_obj2.run(reader_p_value) 
                qTime.put(time_passed)       # stores time passed in queue to print 
                qPos.put(measured_output)    # stores measured pressure [counts] in queue to print l
                final_counter += 1       
                if final_counter == 20:      # collects 20 more data points at returned pressure
                    T2_state = 4
                
        elif (T2_state == S2_off): # time with motor off, collecting data
            moe2.set_duty_cycle(0)
            PWM, time_passed, measured_output = controller_obj2.run(reader_p_value)
            qTime.put(time_passed)         # stores time passed in queue to print 
            qPos.put(measured_output)      # stores measured pressure [counts] in queue to print 
    
            counter += 1                   # collects 20 more data points at setpoint pressure
            if counter == 20:  
                T2_state = 3               
                share_off.put(T2_state)
                counter = 0 # clear counter
                
        elif (T2_state == 3): # time with motor off, not collecting data, resets setpoint to initial pressure 
            counter_s3 += 1
            if counter_s3 == 4: # only run for a few counts
                controller_obj2.set_setpoint(initialP)
                T2_state =1
                share_off.put(T2_state)
                counter_s3 = 0

        elif (T2_state == 4): # does nothing
            pass

        yield T2_state
        print('T2_state')

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")
    
    qTime = task_share.Queue('L', 100, thread_protect=False, overwrite=False,
                          name="Queue Time")
    qPos = task_share.Queue('L', 100, thread_protect=False, overwrite=False,
                          name="Queue Pos")
    init_p = task_share.Share('h', thread_protect=False, name="initial pressure")
    share_off = task_share.Share('h', thread_protect=False, name="Share Off")
    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_print, name="Task_1", priority=1, period=60,
                        profile=True, trace=False, shares=(qTime, qPos, init_p, share_off))
    task2 = cotask.Task(task2_get, name="Task_2", priority=2, period=50,
                        profile=True, trace=False, shares=(qTime, qPos, init_p, share_off))
    
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            #cotask.task_list.pri_sched() # uncomment if want to run on command
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print('') 
