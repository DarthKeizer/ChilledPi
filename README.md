# Chilledpy
Basic python script activating a fan with standard GPIO when rebooting your raspberry pi. Adjust the script to you own liking.

# How To
Sudo crontab -e and add the following code below:
@reboot sudo python /path/to/ChilledPi.py

# Information
This python script uses RPi.GPIO, this script uses default temperatures and default GPIO pins. You can adjust all to you own liking.
