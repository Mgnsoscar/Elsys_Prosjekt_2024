from __future__ import annotations
from typing import *
import serial.tools.list_ports

class serialDevice(serial.Serial):

    def __init__(self, baudrate: int, port: Optional[str] = None, timeout: Optional[int] = None ) -> None:
        """
        Initialize a serial device. Open said device if the port is found and available.
        :param baudrate:
        :param port:
        :param timeout:
        """

        # Init self as a serial.Serial object
        super().__init__(port = port, baudrate = baudrate, timeout = timeout)

        # Try to open the serial device. If no ports have been found, leave it unopened.
        try:

            self.open()

        except:

            pass

    def readSerial(self, sensors: Optional[list[str]] = None, printToConsole: bool = False) -> dict:
        """
        Reads the serial stream and fetches the most recently measured values. The serial format must be "NameOfSensor1:value, NameOfSensor2:value,... "
        :param sensors: If not None, a list with the names of sensor to be read from. Default is None, meaning all values are read.
        :param printToConsole: True if fetched sensor values are to be printed to console. False by default.
        :return: Dictionary of values from the serial stream. Keys are the sensor names. If no sensor data is found, the dictionary is empty.
        """

        # Fetch the entire serial stream as a string
        packet  =   str( self.read_all() )
        #print(packet)

        # Sometimes it takes a few seconds before the serial stream starts to spit out actual values. The try/except loop returns a list of
        # None-values if no sensor values are found.

        try:

            # Split the serial stream into values, using "\n" as the divider. Sometimes the last value is not printed in it's entirety,
            # so fetch the one before. This introduces a slight lag, but the baudrate should be so fast that it doesn't really matter.
            stream  =   packet.split("\\n")[-2].rstrip("\\r")


            # Check if the string starts with b', in that case remove it
            if stream.startswith("b'"):

                stream  =   stream[2:]

            # Separate string into the sensor/value-pairs using "," as the divider.
            if "," in stream:
                pairs  =   stream.split(",")
            else:
                pairs   =   [stream]

            # Add the pairs to the dictionary

            sensorData  =   {}
            for pair in pairs:

                split   =   pair.split(":")

                # If no specific sensors are specified, add all values
                if sensors is None:

                    sensorData[split[0]]    =   int(split[1])

                else:

                    if split[0] in sensors:

                        sensorData[split[0]]    =   int(split[1])


            if len(sensorData) == 0:

                sensorData  =   None

        except:

            sensorData =  None

        # Print the values to console
        if printToConsole:

            print(sensorData)

        return sensorData

    def newBaudrate(self, newBaudrate: int) -> None:
        """
        Defines a new baudrate
        :param newBaudrate: The new baudrate.
        """

        self.baudrate = newBaudrate

    def newPort(self, newPort: str) -> None:
        """
        Chooses a new port as input.
        :param newPort: Thw name of the new port.
        """
        self.port = newPort
        self.open()

    @staticmethod
    def fetchPorts() -> list[str]|None:
        """
        Retrieve a list with names of available ports.
        :return: List of available port names. None if no ports are available.
        """

        # Fetch available ports
        ports       =   serial.tools.list_ports.comports()
        portsList   =   []

        for port in ports:

            portsList.append( str( port ) )

        return portsList
