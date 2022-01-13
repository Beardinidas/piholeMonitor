# piholeMonitor
Uses Blinkt library on a RaspberryPi to Display PiHole Status and Add Percentage

You will require to have your PiHole Instance on a seprate RaspberryPi than the device this runs on  

# Auto Start Script
sudo nano /etc/rc.local  
Add the the location the script will run from to the end of the file    
i.e "python3 /home/username/projects/piholeMonitor/main.py &"  
ensure the file ends with "exit 0"  


# Features
Blinkt features 8 super bright RGB LEDs that neatly fit onto your RaspberryPi's GPIO  
AD blocked percentage is displayed as GREEN LEDs filling up the BLINKT module  
If no connection to your PiHole instance is detected - LEDs will radiate in  RED  

If PiHole is disabled the LEDS will cycle through through colours running up and down the Module

Lights switch off at: 22:00  
Lights Switch on at: 07:59:59 


# TODO
Add list of colours that can be easily switched to for displaying Ad percentage  
