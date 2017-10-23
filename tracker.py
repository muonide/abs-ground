#!/usr/bin/env python
"""
Antenna Tracker Controller for Trident Antenna Array and RFD Radio Controller

Author:	Trevor Gahl, CpE
Based on work from Austin Langford, AEM, Scott Miller, CpE, Dylan Trafford, CpE, and David Schwerr, CS of the Minnesota/Montana Space Grant Consortia
Software created for use by the National Space Grant Consortium
Purpose: To acquire the location of a balloon in flight, and aim the array of antennae at the balloon
Additional Features: RFD 900 based Command Center and Image Reception
Creation Date: March 2016
Last Edit Date: August 2, 2017
"""

# System imports
import sys
import os
import time as t
from datetime import *
import serial
import serial.tools.list_ports
import threading

# Scientific libraries
import math
# database section, help from:
# http://www.tutorialspoint.com/python/python_database_access.htm
import numpy as np
import matplotlib
import geomag
import base64					   # = encodes an image in b64 Strings (and decodes)
import hashlib					  # = generates hashes

# Imports from files
from server import *
from ServoController import *			# Module for controlling Mini Maestro
from PointingMath import *				# Functions for calculating angles and distances
from BalloonUpdate import *				# Class to hold balloon info
from GetData import *					# Module for tracking methods
from Payloads import *					# Module for handling payloads
import maestro.py

# Data collection devices

from Adafruit_BNO055 import BNO055


class IMU:
    
    def __init__():
        bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
        
        if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

    def calibrateIMU():

        ##forloop
        # status, self_test, error = bno.get_system_status()
        # print('System status: {0}'.format(status))
        # print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
        # # Print out an error if system status is in error mode.
        # if status == 0x01:
        #     print('System error: {0}'.format(error))
        #     print('See datasheet section 4.3.59 for the meaning.')
        sys, gyro, accel, mag = bno.get_calibration_status()
        # Print everything out.
        print( sys, gyro, accel, mag))

    def getHeading():

    def getAltitude():

class SerialDevice:
    """ A class to manage serial devices """

    def __init__(self, port, baud, timeout):
        servo = maestro.Controller()
        servo.setAccel(0,4)

    def getPort(self):
        return self.port

    def getBaud(self):
        return self.baud

    def getTimeout(self):
        return self.timeout

    def getDevice(self):
        return self.device


class Unbuffered:
    """ A class to eliminate the serial buffer """

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def flush(self):
        self.stream.flush()

    def close(self):
        self.stream.close()


class tracker():
    def __init__(self, parent=None):
        
        # Determine Serial Connections
        self.searchComPorts()


    def setAutotrack(self):
        """ Toggles autotracking """

       # toggle autotracking...

    def updateBalloonLocation(self, update):
        """ Updates the tracker with the latest balloon location """

        # Log the balloon location no matter what
        self.logData("balloonLocation", update.getTrackingMethod() + ',' + str(update.getTime()) + ',' + str(update.getLat()) + ',' + str(
            update.getLon()) + ',' + str(update.getAlt()) + ',' + str(update.getBear()) + ',' + str(update.getEle()) + ',' + str(update.getLOS()))

        if update.getTrackingMethod() == 'Iridium':
            if not self.useIridium:
                return

        # Make sure it's a good location
        # Don't consider updates with bad info to be new updates
        if ((update.getLat() == 0.0) or (update.getLon() == 0.0) or (update.getAlt() == 0.0)):
            return

        # Makes sure it's the newest location
        if update.getSeconds() < self.currentBalloon.getSeconds():
            return
            # Confirm that update matches a selected tracking method
            # if self.currentBalloon.getTrackingMethod() == 'RFD':
            # if (not self.useIridium or not self.useAPRS) and self.useRFD:
            # return

            # if self.currentBalloon.getTrackingMethod() == 'Iridium':
            # if (not self.useRFD or not self.useAPRS) and self.useIridium:
            # return

            # if self.currentBalloon.getTrackingMethod() == 'APRS':
            # if (not self.useIridium or not self.useRFD) and self.useAPRS:
            # return

        # If you haven't returned by now, update the graphing arrays
        
        self.antennaOnline(update)		# Move the tracker if tracking
        self.refresh(update)			# Update the tables
        self.currentBalloon = update
        

    def antennaOnline(self, update):
        """ Reaim the antennae while in autotrack mode """

        if self.autotrackOnline:
                if self.servosAttached:
                # Move Antenna to correct position
                self.moveToTarget(update.getBear(), update.getEle())

        else:
            #indicate offline


    def searchComPorts(self):
        """ Sets the Connections based on the Com Ports in use """

        serCheck = False

        ports = list(serial.tools.list_ports.comports())

        # Go through each port, and determine if it matches a known device
        for each in ports:
            print(each)
            eachLst = str(each).split('-')


            try:		# Mini Maestro shows up as Pololu Micro Maestro 6, but with 2 ports. We want the command port
                if eachLst[1].find("Pololu Micro Maestro 6") and eachLst[2].find("Servo Controller Command Port") != -1:
                    servoCOM = eachLst[0].strip()
                    self.servoCOM.setText(servoCOM)
                    self.servoAttached.setChecked(True)
                    serCheck = True

            except:		# Because not every port has 2 '-' characters, the split function may not work
                if (each.vid == 8187 and each.pid == 137) and each.location is None:
                    servoCOM = eachLst[0].strip()
                    self.servoCOM.setText(servoCOM)
                    self.servoAttached.setChecked(True)
                    serCheck = True

        # After checking all of the ports, you can see if a device has been
        # disconnected
         if not serCheck:
            # Indicate that servo is not attached
            print('No servo attached')
            self.servoAttached.setChecked(False)
        

    def calibrateIMU(self):
        """ Display the calibration values for the IMU in a visible window,
        and allow the user to select when the calibration is ready
        """

        if self.imuAttached:

            try:
                # connect to BNO055 via i2c
            except:
                print("Error connecting to IMU")
                return

            try:
                # Display the Calibration Status in the web browser
            except:
                print("Error creating the calibration window")
                return

            self.calibrationReady = False
            while not self.calibrationReady:		# Continuously loop until the IMU is calibrated to satisfaction
                # Display the Calibration Status in the web browser
        else:
            print("No IMU Attached")

    def getCenterBearing(self, s2):
        """ Acquire a center bearing and a GPS location from the calibration arduino """

        
        
        s2.flushInput()		# Clear the buffer so it can read new info
        
        # Read from GPS module and populate temp_gps[]

        tempLat = temp_gps[1]		# Get ground station latitude
        tempLon = temp_gps[2]		# Get ground station longitude
        tempAlt = temp_gps[3]		# Get ground station altitude
        # Get the offset for the center bearing
        tempoffsetDegrees = temp_arduino[4]
        tempLat = tempLat.split(".")
        # Convert the lat to decimal degrees as a float
        self.groundLat = float(tempLat[0]) + float(tempLat[1]) / 10000000
        tempLon = tempLon.split(".")
        # Convert the lon to decimal degrees as a float
        self.groundLon = float(tempLon[0]) - float(tempLon[1]) / 10000000
        tempAlt = tempAlt.split(".")
        # Get the altitude to the floor(foot)
        self.groundAlt = int(tempAlt[0])
        self.centerBear = float(tempoffsetDegrees)
        declination = float(geomag.declination(
            dlat=self.groundLat, dlon=self.groundLon, h=self.groundAlt))
        self.centerBear = (self.centerBear + declination)
        if self.centerBear > 360:
            self.centerBear -= 360
        elif self.centerBear < 0:
            self.centerBear += 360
        print ("Local Latitude: \t", self.groundLat)
        print ("Local Longitude:\t", self.groundLon)
        print ("Local Altitude: \t", self.groundAlt)
        print ("Offset Degrees: \t", self.centerBear)
        print ("Declination:	\t", declination)
        print ("Offset + Dec:   \t", self.centerBear)
        print ("-------------------------------------------------------")

        self.antennaBear = self.centerBear
        # Lets the program know that the center bearing has been set before
        self.centerBearSet = True

    
    def logData(self, type, msg):
        """ Logs the message in the correct file designated in the type argument """
        if self.saveData:
            try:
                if type == "balloonLocation":
                    f = open(self.balloonLocationLog, 'a')
                elif type == "pointing":
                    f = open(self.pointingLog, 'a')
                f.write(str(datetime.today().strftime(
                    "%m/%d/%Y %H:%M:%S")) + ',' + msg + '\n')
                f.close()
            except:
                print("Error logging data: " + type + ',' + msg)

        else:
            return

    def pointToMostRecentBalloon(self):
        """ Aims the tracker at the balloon, even if the antenna tracker is offline """

        if self.servosAttached:
            self.moveToTarget(self.currentBalloon.getBear(),
                              self.currentBalloon.getEle())
            print("Tracker aimed at most recent balloon location")
        else:
            print "Error: Settings set to no Servo Connection"

    def moveToCenterPos(self):
        """ Send servos to their center pos (should be horizontal and straight ahead if zeroed) """

        if self.servosAttached:
            try:
                self.servoController.moveTiltServo(6002)
                self.servoController.movePanServo(6002)
            except:
                print("Error moving servos to center position")

            # Set the antenna bearing and elevation to the center position
            self.antennaBear = self.centerBear
            self.antennaEle = 0
            self.manualRefresh()

        else:
            print "Error: Settings set to no Servo Connection"

    def moveToTarget(self, bearing, elevation):
        """ Moves servos based on a bearing and elevation angle """
        # Account for manual offset
        bearing = bearing
        #elevation += self.tiltOffset

        temp = 0
        # Uses the center bearing, and makes sure you don't do unnecessary
        # spinning when you're close to 0/360
        if (bearing > 180) and (self.centerBear == 0):
            self.centerBear = 360
        elif ((self.centerBear - bearing) > 180) and (self.centerBear >= 270):
            bearing += 360
        elif ((self.centerBear - bearing) > 180) and (self.centerBear <= 180):
            temp = self.centerBear
            self.centerBear = 360 + temp

        print ("\tBearing: %.0f" % (bearing))
        print ("\tElevation Angle: %.0f" % (elevation))

        # Pan Mapping
        # Mapping is designed for 45 degree increments
        # If
        panTo = (bearing - self.centerBear)
        # print "PanTo Value\n"
        # print panTo

        if panTo > -1 and panTo < 91:
            panTo = 180 - panTo
            if panTo < 0:
                panTo = panTo + 360
            panTo = int((panTo * 2.6 + 1020) * 4)

        elif panTo < 0 and panTo > -91:
            panTo = 180 - panTo
            if panTo < 0:
                panTo = panTo + 360
            panTo = int((panTo * 2.72 + 1010) * 4)

        else:
            panTo = 180 - panTo
            if panTo < 0:
                panTo = panTo + 360
            print "Default Mapping"
            panTo = int((panTo * 2.639 + 1025) * 4)

        if panTo > 7600:
            panTo = 7600
        if panTo < 4300:
            panTo = 4300
        # print panTo
        print "\tServo Degrees:"
        if self.servosAttached:
            self.servo.setTarget(0,panTo)  #set servo to move to center position

        # Tilt Mapping
        tiltTo = elevation
        tiltTo = 180 - tiltTo
        if tiltTo < 0:
            tiltTo = tiltTo + 360

        # Update the tilt mapping values here#
        tiltTo = int((tiltTo * 2.639 + 1025) * 4)

        if tiltTo > 6000:
            tiltTo = 6000		# Don't go over the max
        if tiltTo < 4348:
            tiltTo = 4348			# Don't go under the min
        # print tiltTo
        if self.servosAttached:		# Move the servos to the new locations if they're attacheed
            self.servo.setTarget(1,tiltTo)
        if temp != 0:
            self.centerBear = temp

        # Write the new pointing location to the log file
        self.logData("pointing", str(bearing) + ',' + str(elevation))

        # Update pointing values
        self.antennaBear = bearing
        self.antennaEle = elevation
        self.manualRefresh()

    


if __name__ == "__main__":
    
  