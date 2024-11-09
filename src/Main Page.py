"""! \mainpage 
   \section intro_sec Introduction
   
   The purpose of this project was to develop a preliminary depth control chamber.
   
   Pressure can be directly correlated to depth, given a liquid's density.
   This project takes a desired pressure setpoint and controls a motor-driven syringe system to
   pressurize a chamber to the setpoint. It waits a period of time, as if it were underwater collecting data,
   and then returns to the initial pressure, as if it were returning to the water surface. 
 
   \section soft_org_sec Software Description and Organization
   
   The main program uses three classes to do our desired function.
   It contains multiple tasks in which it multitasks between one another. 
   
   Following a brief description of the main program, the classes used are mentioned. 
   
   ## Main Program
   The main program initially collects a setpoint pressure, which is the desired pressure the user wants to go to.
   Then, as the program multitasks, is uses the Pressure Sensor class to essentially interpret and collect pressure values.
   It works with the Closed-Loop Controller class to run the motor driver based on calculated error between setpoint and current pressure.
   The program with run the controller until reaching the setpoint, in which it turns the motor off for a time duration.
   Then, the program will use both the Pressure Sensor and Closed-Loop Controller classes again to return the chamber to the initial pressure from start up.
   
   Throughout the duration of the program, if there are pressure values being collected, there will be values printed.
   This occurs by the program multitasking between data collection and printing. 
   
   ##Pressure Sensor Class
   To measure pressure, we used a Honeywell Board Mount Pressure Sensor, which uses I^2C communication. The sensor transmits data in byte arrays. The first byte being status, next two being pressure, and following two being temperature. A PressureSensor class was created to process the data from bytes into counts and then interpretable values of pressure in [psi] and temperature in [Farenheight].

   Two types of data were collected. One being pressure, our primary focus, and the other temperature, for future use. You can read more about our pressure sensor and its I^2C communication using the links included at the bottom of the readme. 
    
 * def __init__:
         Initialize the PressureSensor Object.
         Collect initial data values for status and initial pressure. 
 * def readP_Raw:
         Reads Raw Status, Pressure, and Temperature Data from Sensor
 * def PtoRawP:
         Converts setpoint pressure from units of psi to counts.
 * def RawtoData_P:
         Converts raw pressure data in units of counts to [psi].
         Then pressure difference from initial pressure and thus displacement depth
 * def RawtoData_T:
         Converts raw pressure data in units of counts to [Fahrenheit].
    
     ### Status
    To interpret the status output from the pressure sensor, the table below was used, provided from the manual, "I^2C Communications with Honeywell Digital Output Pressure". 

    <img width="294" alt="Screenshot 2024-03-17 at 9 48 11 PM" src="https://github.com/alialauren1/ME405-Term-Project/assets/157066441/f21555c3-b900-4082-98ba-afea877355a0">

    The class was written to always print the status upon calling it. Throughout our use and application of the class, the status of the sensor was always S1 = 0 and S0 = 0, indicating we were in a normal operation, whilst collecting valid data.  

    ### Pressure
    To calculate the pressure from the digital output, the pressure sensor transfer function shown below was used, also provided from the manual, "I^2C Communications with Honeywell Digital Output Pressure". The equation was rearranged to solve for Pressure. 

    <img width="326" alt="Screenshot 2024-03-17 at 9 38 54 PM" src="https://github.com/alialauren1/ME405-Term-Project/assets/157066441/e8322335-e550-4d0f-b144-daa90d571818">

    Where,

    <img width="347" alt="Screenshot 2024-03-17 at 9 41 27 PM" src="https://github.com/alialauren1/ME405-Term-Project/assets/157066441/81dee95d-3d2a-44a9-8cc6-a6c065db89b8">

    ### Temperature
    The temperature conversion function shown below was also provided in the Honeywell I^2C manual. Although, it was modified to convert the temperature into Fahrenheit. 

    <img width="249" alt="Screenshot 2024-03-17 at 9 46 18 PM" src="https://github.com/alialauren1/ME405-Term-Project/assets/157066441/79dcab9f-85fb-4055-beed-cf1e42050b7f">

    ### Setpoint Conversion
    A definition in the pressure sensor class was made to convert pressure values in [psi] to counts. This was to aid user input of a setpoint. They may now type a setpoint in [psi] and it gets converted to interpretable data, that being counts, for use in our Closed-Loop Controller Class. 
     
         
   ##Motor Driver Class
   
   This class implements a motor driver, setting the duty cycle for the motor.
   It allows for initialization of the motor pins and timer.
   
 * def __init__:
         Creates a motor driver by initializing GPIO pins and turning off the motor for safety. 
 * def set_duty_cycle:
         This method sets the duty cycle to be sent to the motor to the given level.
         Positive values cause torque in one direction, negative values
         in the opposite direction.
         
   ##Closed-Loop Controller Class
   
   This class is a closed-loop control system with proportional control.
   
 * def __init__: Inits the Controller object with the provided proportional gain and set points.
 * def run: Runs the controller and calculation for the actual values based by the measured output.
 * def set_setpoint:
        Takes in a desired set point. 
        Sets new setpoint for class
 * def set_Kp:
        Takes in a desired Kp value.
        Sets new Kp for class
         
        
   \section T_S_sec Tasks and States for Main Program
   This section describes the tasks and corresponding states used in our main program.
   Our main program handles multitasking between different tasks using cotask.
  
   ## Task Diagram
   Below is the task diagram for our main program. There are two tasks.
   \image html ME405_Main_Task_Diagram.png "ME405 Main Program Task Diagram" width=500px height=240px
   ### Task 1:
   * Gets time and pressure out of a queue and the current Task 2 value out of a share.
   * Converts pressure from units of counts to [psi] and displays value along with corresponding depth underwater in [ft] and time duration.
   ### Task 2:
   * Converts desired setpoint from units of [psi] to counts using Pressure Sensor Class
   * Reads pressure sensor data in units of counts from Pressure Sensor Class.
   * Runs closed-loop controller with pressure counts comparing against setpoint to send motor PWM commands.
   * Puts time duration and pressure into queue
   
   ## Finite State Machines
   Below are the Finite State Machines (FSM) corresponding to the two tasks in our main program.
   \image html ME405_FSM_Task_1.png "ME405 FSM Task 1" width=580px height=290px
   \image html ME405_FSM_Task_2.png "ME405 FSM Task 2" width=620px height=400px
 
"""
 