"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2.
    
@Modifications Made By: Alia Wolken, Eduardo Santos, Andrew Jwaided
"""

import gc
import utime
import pyb
import cotask
import task_share
import ControllerUI


from motor_driver import motordriver
from encoder_reader import Encoder
from ControllerUI import Controller
from pressure_sensor import PressureSensor

def task1_print(shares):
# convert, and print data
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    qTime, qPos, share_init_p, share_off, share_setpoint = shares
        
    sensor_obj = PressureSensor(0,0,0)
    
    T1_state = 1
    S1_print = 1

    while True:
        
        if (T1_state == S1_print): # Done with Controller, Print Vals
            
            time = qTime.get()
            pos = qPos.get()
 
            #print('TIME')
            #print('RAW P')
            pos_raw = (pos)
            #print(f'{pos_raw=}')
            pressure, pressure_diff, depth, init_p  = sensor_obj.RawtoData_P(pos_raw)
            share_init_p.put(init_p)
            #print(f'{time=},{pressure=}{init_p=}')
            print(time,pressure)
            
            T2_state = share_off.get()
            if T2_state == 3:
                T1_state = 2
            
        elif (T1_state == 2):
            T2_state = share_off.get()
            if T2_state == 1:
                T1_state = 1
            
        yield T1_state
            
        
def task2_get(shares):
    """
    Task that recives data.
    
    @param shares: A tuples of a share and queue from which gets data.
    """
    # get data
    qTime, qPos, share_init_p, share_off, share_setpoint = shares[0], shares[1], shares[2], shares[3], shares[4]
    
    enc2 = Encoder("enc2", pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)
    moe2 = motordriver (pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    
#     setpoint_p = 18
#     
#     sensor_obj = PressureSensor(setpoint_p,0,0)
#     setpoint_raw = sensor_obj.PtoRawP(setpoint_p)

    #enc2.zero()
    
    setpoint = share_setpoint.get()
    print("SET POINT")
    print(setpoint)
    sensor_obj = PressureSensor(setpoint,0,0)
    # Paramters for the contoller
    Kp = 5
    controller_obj2 = Controller(Kp, setpoint)
    
    T2_state = 0
    S1_data = 1
    S2_off = 2
    S3_goback = 3
    counter = 0
    counter_s3 = 0
    final_counter = 0
    key = 0
    
    while True:
        if (T2_state == 0):
            if setpoint != 0:
                T2_state = 1
        
        if (T2_state == S1_data): # Closed Loop Controller
            initialP = share_init_p.get()
            
            reader_p_value, temp_val = sensor_obj.readP_Raw() # Reads Raw P & T values
            PWM, time_passed, measured_output = controller_obj2.run(reader_p_value)
            moe2.set_duty_cycle(-PWM) #Ajust motor 2 postion
            # + makes vacuum, - makes ^ pressure
            #counter += 1

            #print(f"{reader_p_value=} {PWM=} {time_passed=} {measured_output=}")
            qTime.put(time_passed)
            qPos.put(measured_output)
            
            if setpoint-6 <= reader_p_value <= setpoint+6:
                print('REACHED SETPOINTT!!')
                moe2.set_duty_cycle(0)
#                T2_state = 2
#                key = 1
            #print('T2_s1')
            
#             if (initialP-6 <= reader_p_value <= initialP+6) & key == 1:
#                 moe2.set_duty_cycle(0)
#                 PWM, time_passed, measured_output = controller_obj2.run(reader_p_value)
#                 qTime.put(time_passed)
#                 qPos.put(measured_output)
#               final_counter += 1
#                 if final_counter == 20:
#                     #print("done")
#                     T2_state = 4
                
#         elif (T2_state == S2_off): # time with motor off, collecting data
#             moe2.set_duty_cycle(0)
#             PWM, time_passed, measured_output = controller_obj2.run(reader_p_value)
#             qTime.put(time_passed)
#             qPos.put(measured_output)
#     
#             counter += 1 
#             if counter == 20:
#                 T2_state = 3
#                 share_off.put(T2_state)
#                 counter = 0
#                 
#         elif (T2_state == 3): # time with motor off, not collecting data
#             counter_s3 += 1
#             if counter_s3 == 20:
#                 controller_obj2.set_setpoint(initialP)
#                 T2_state =1
#                 share_off.put(T2_state)
#                 counter_s3 = 0
# 
#         elif (T2_state == 4):
#             pass

        yield T2_state

         
def task3_setpoint(shares):
# convert, and print data
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    qTime, qPos, share_init_p, share_off, share_setpoint = shares

    setpoint_p = NaN
    sensor_obj = PressureSensor(setpoint_p,0,0)
    setpoint_raw = sensor_obj.PtoRawP(setpoint_p)
    moe2 = motordriver (pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
# Initialize the USB VCP
    usb_vcp = pyb.USB_VCP()
    #ord(input number) o
    while True:
        # Read data from the USB VCP
        #data = usb_vcp.any
        data = usb_vcp.readline()
        if data:  # Check if data is not empty
            try:
                number = int(data)
                if 1 <= number <= 5:
                    print("Number {} pressed.".format(number))
                    if number == 1:
                        setpoint_p = 14.7
                        setpoint_raw = sensor_obj.PtoRawP(setpoint_p)
                        share_setpoint.put(setpoint_raw)
                    if number == 2:
                        setpoint_p = 18
                        setpoint_raw = sensor_obj.PtoRawP(setpoint_p)
                        share_setpoint.put(setpoint_raw)
                    if number == 3:
                        setpoint_p = 13
                        setpoint_raw = sensor_obj.PtoRawP(setpoint_p)
                        share_setpoint.put(setpoint_raw)
                    # Do something based on the pressed number
                else:
                    print("Invalid number. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            moe2.set_duty_cycle(0)
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
    
    share_setpoint = task_share.Share('h', thread_protect=False, name="setpoint")
    
    # Create a share and a queue to test function and diagnostic printouts
    #share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    #q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
    #                      name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_print, name="Task_1", priority=1, period=60,
                        profile=True, trace=False, shares=(qTime, qPos, init_p, share_off, share_setpoint))
    task2 = cotask.Task(task2_get, name="Task_2", priority=2, period=50,
                        profile=True, trace=False, shares=(qTime, qPos, init_p, share_off, share_setpoint))
    task3 = cotask.Task(task1_print, name="Task_3", priority=3, period=10,
                        profile=True, trace=False, shares=(qTime, qPos, init_p, share_off, share_setpoint))
    
    # bug report in readme, only works when data task is running faster than printing task
    
    # Ex: motor controller, time constant half second => run 10 times faster
    
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task2)
    
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    #print(task1.get_trace())
    print('') 
