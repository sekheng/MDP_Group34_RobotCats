# MDP_Group34_RobotCats
10 weeks project to program and build an obstacle-avoidance robot. 

## Video Demo
### Click on the image to go to the YouTube Video
[![Insert Image Here](https://user-images.githubusercontent.com/13762085/204751905-fe43fe3a-0187-4634-9951-2607428af7c1.png)](https://youtu.be/fcFpHun6Xqw)
By combining various disciplines into one project, it challenges the team to learn various technology such as Android, RPI, Path-Finding, and STM.
The result is an obstacle-avoidance robot that can navigate efficiently across the maze.

## Android
### Bluetooth Communication
Using Android's Bluetooth API, it creates a thread to discover new bluetooth devices, connect to new devices and once connected, that thread will begin to listen for incoming data and be responsible for re-establishing connection if that connection is lost.

<img src='https://user-images.githubusercontent.com/13762085/204764721-0141a9c3-e2c6-4550-b249-a1c1208147b7.png' width=480 height=640/>

*UI to display what devices are discovered and paired to improve user experience*

This Bluetooth connection is used to communicate with the RPI board and transmit the data in JSON format so that the RPI board can parse the data then instruct the robot and it’s algorithm on what to do according to the user input.

### User Interface
To improve code readability and prevent unnecessary hardcoding, RecyclerView is used extensively so that the UI is created based on the hardcoded numbers meant for the rows and columns of the grid. RecyclerView is also used for navigating between individual controls to prevent the clutter on the screen shown below.

*before*

<img src='https://user-images.githubusercontent.com/13762085/204767314-d51f97ab-02ec-45f8-834e-1729d82bc91c.png' width=800 height=300/>

*after*

<img src='https://user-images.githubusercontent.com/13762085/204766931-1968407f-8e79-4b06-9ef8-06291df41d07.png' width=300 height=300/>

To also know what grid the user is pressing and prevent fat-finger, each grid box is very large with its coordinate directly displayed inside the box so that the user can input the obstacle immediately.

<img src='https://user-images.githubusercontent.com/13762085/204766697-d6cb4a46-12cb-47e7-be62-1a2fa8605774.png' width=480 height=640/>
