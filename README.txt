Name: Sai Tejah Srikanth
Student id: 210971200

Instructions to be followed:

1. Open 'Terminal'

2. Unzip the file 'cr_week8_test.zip' using following command:
 $ unzip cr_week8_test.zip -d ~/catkin_ws/src/
3. Run the following set of commands

    $ cd ~/catkin_ws # Moving to the catkin workspace
    
    $ catkin_make # Compiles the catkin package
    
    $ roscore # starts the master, parameters and rosout
 
4. Run the launch.xml in a "New Terminal"
     $ source ./devel/setup.bash # sources your environment setup file
     
     $ roslaunch cr_week8_test launch.xml # runs the launch file
