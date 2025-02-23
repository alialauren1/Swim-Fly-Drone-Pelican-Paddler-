# Swim-Fly-Drone-Research-Project-

This project entails constructing a submersible chamber capable of reaching
specified depths. The system will operate in a closed loop, actuating until it 
reaches a desired pressure depth.

This project was proposed to Dr. Ghalamchi to be a senior project, where worked together to set the goal of improving previous tests on waterproof drones that can take off from underwater to allow for a drone that can float on top of the water surface as well as have added support to be pushed up from underwater. The new design needs to be detachable from the built waterproof drone to compare its new features in tests. The detacheable buoyancy control device was successfully tested at the end of the senior porject course. However, there is still work to do for aerial flight and thus testing of the whole system together. This is now a continued research project between Alia Wolken and Dr. Ghalamchi. 

"How it works" for Buoyancy Control Device:
Pressure can be directly correlated to depth, given a liquid's density.
   This system takes a desired pressure setpoint and controls a motor-driven syringe system to
   pressurize a chamber to the setpoint. It waits a period of time, as if it were underwater collecting data,
   and then returns to the initial pressure, as if it were returning to the water surface. 

### Schematic

The schematic below shows a very general diagram of how components are being powered and communicating with one another. 
The power supply provides power to the motor. The power supply was set to 12V with a 0.5 A current limit. 

<img width="355" alt="Schematic" src="https://github.com/alialauren1/ME405-Term-Project/assets/157066441/69f9537e-9c2f-4ec5-904a-f615c2763568">

Figure 1. Schematic of components

## Hardware design
We have integrated Ametck Pittman's PG6712A077-R3 motor to a 50 CC syringe. Utilizing this motor, we've have attached a worm gear and gears to ensure sufficient torque to be generated. These gears are attached to a pinion and aligned with a rack that allows for the syringe to be moved back and forth. This allows
for the system to achieve the desired weight to submerge the whole system.

The gears were selected from McMaster. This is so in the future, they can be ordered parts. For now, we used the CAD files to 3D print them for budget reasons. While sizing and choosing the number of teeth we would need for our system, we calculated to torque that the motor needed to have to overcome the friction force between the piston and syringe.

The pressure sensor we selected is the SSCMANV030PA2A3 Honeywell Pressure Sensor. It measures absolute pressure, with a range from 0-30 psi. Is allows liquid media on the port, which will come of use in future quarters when we test our system underwater. 

<img width="182" alt="Screenshot 2024-03-19 at 8 53 00 PM" src="https://github.com/alialauren1/ME405-Term-Project/assets/157066441/83f965b6-e449-474c-9980-f4381207573f">

Figure 2. SSCMANV030PA2A3 Honeywell Pressure Sensor

<img width="697" alt="Screenshot 2025-02-22 at 9 59 54 PM" src="https://github.com/user-attachments/assets/607a9807-954a-4623-b921-8044b39f7e3f" />

Figure 3. Hardware all connected

<img width="690" alt="Screenshot 2025-02-22 at 9 46 14 PM" src="https://github.com/user-attachments/assets/02b90a8d-7c07-4a28-bb6b-b3a3a456d631" />

Figure 4. Pins PB_10, PB_4, and PB_5 were used to connect to the motor driver

<img width="368" alt="Screenshot 2025-02-22 at 10 02 44 PM" src="https://github.com/user-attachments/assets/91c40f9c-172e-48d8-98d4-8ed98caa694d" />
<img width="409" alt="Screenshot 2025-02-22 at 10 02 55 PM" src="https://github.com/user-attachments/assets/df3ba265-2767-4cb6-bf9b-52eb32e00a57" />

Figure 5. L298N Motor Drive Controller Board

## Software design
To measure pressure, we used a Honeywell Board Mount Pressure Sensor, which uses I^2C communication. A class was made to use this sensor. Details on how the data was collected and process is linked below. Pressure Sensor: SSCMANV030PA2A3
https://alialauren1.github.io/ME405-Term-Project/index.html#autotoc_md1

Attaching the sensor and the Ametek motor to our Nucleo, we were able to program both components to get a functioning product.

### Tasks and States
The Tasks and States used in the main program are shown in diagrams linked on the page below.
https://alialauren1.github.io/ME405-Term-Project/index.html#T_S_sec

## Testing and Results

### Preliminary
We want our chamber to be able to acheive at minimum, 5 ft depth. Calculations were run, shown below, to determine the pressure that coincides with a depth of 5 ft in water. Being a little under 16.5 psi, we decided to run initial tests at 16.5 psi.

<img width="558" alt="Screenshot 2024-03-19 at 9 05 30 PM" src="https://github.com/alialauren1/ME405-Term-Project/assets/157066441/ff3288be-28b8-42c2-b472-b3d4093e939d">

In order to test our project sensors and motor control, we ran multiple tests in order to find our optimal Kp value. The results are presented in the plot down below. This was preliminary testing. 

<img width="605" alt="Screenshot 2024-03-17 at 10 32 32 PM" src="https://github.com/alialauren1/ME405-Term-Project/assets/157066441/ac451cf5-9cc9-4dc5-884a-5c23263242ac">

Figure 9. Plot of Pressure vs Time inside the syringe. Each line represents a different run of data collected while altering the Kp value.

During our testing, we initially set Kp to 5 (shown in blue) and then increased it to 10 (shown in orange). Observing the graph, it's evident that increasing the Kp value led to faster attainment of the target pressure of 16.5 [psi].

While testing to achieve for efficiency in reaching the desired pressure, it's essential to consider what our system will be attached to. Our system with the syringe and pressure sensor will be attached to a drone. Rapid pressure and volume changes may introduce a moment within the drone body, causing the drone to loose control. Therefore, we must weigh the trade-offs between achieving rapid pressure targets and maintaining system stability.

As we continue to test our project, further tests will be necessary to determine the optimal balance between speed, the system stability and accuracy. This process may involve fine-tuning parameters beyond just changing the Kp. This may incude making the chamber of the system bigger and other factors.

### Lab Demo Results and Functionality of Product
The below plot shows the pressure inside the syringe. The autonomous journey is one in which the system reaches the desired setpoint, waits for a duration, and then returns to the initial pressure. 

<img width="360" alt="image" src="https://github.com/alialauren1/ME405-Term-Project/assets/157066441/75d0b395-c743-4855-a188-f06f3c17799e">

Figure 4. Plot of Pressure vs Time inside the syringe with a setpoint of 17 [psi].  

This journey mimics future developement of our larger senior project in which this pressure chamber will be attached to a drone. We anticipate it will be beneficial for some remote or signal to send a desired depth as the setpoint to the system, in which the chamber will submerge with the drone, going to that depth. It will remain there, possible to collect data, and then autonomously return to the surface. 
We are satisfied with the final results. The chamber is able to reach pressures higher than a pressure corresponding to 5ft, which was what we wanted to achieve.
It is also able to maintain the increase in pressure while the motor is turned off, which is a satisfying result. 

The system also works at lower than atmosphere pressures. In the plot below, the setpoint was chosen as 13 psi. However, in another test, we were able run the system with an even lower setpoint of 10 psi. Although this is less necessary to have, it is satisfying to see that ability. 

<img width="349" alt="Screenshot 2024-03-19 at 8 38 33 PM" src="https://github.com/alialauren1/ME405-Term-Project/assets/157066441/a8d9b7e9-7423-4f52-975f-87fc786d1f34">

Figure 5. Plot of Pressure vs Time inside the syringe with a setpoint of 13 [psi].  

### Software and Sensors
We learned that the data being output from our pressure sensor was in counts. This led to the creation of a definition in our PressureSensor class to interpret the counts into a unit of measurement that could be easily interpretted, that being [psi]. Since our Closed-Loop Controller class uses the pressure sensor output in counts to correct for a desired pressure, an additional definition was made to interpret user desired setpoint input from [psi] to counts. 

## Safety
Our project prioritizes user safety through thoughtful design considerations. By utilizing small gears, we have effectively reduced the risk of injuries to the user. Once the system has been fully assembled, all moving components and electrical elements will be enclosed and inaccessible to the user. This design ensures that users are protected from potential hazards during the system's operation.

## Additional files

Pressure sensor datasheet:
[SSCMANV030PA2A3 Honeywell.pdf](https://github.com/alialauren1/ME405-Term-Project/files/14630972/SSCMANV030PA2A3.Honeywell.pdf)

I2C Communications with Honeywell Pressure Sensors:
[sps-siot-i2c-comms-digital-output-pressure-sensors-tn-008201-3-en-ciid-45841.pdf](https://github.com/alialauren1/ME405-Term-Project/files/14630975/sps-siot-i2c-comms-digital-output-pressure-sensors-tn-008201-3-en-ciid-45841.pdf)
