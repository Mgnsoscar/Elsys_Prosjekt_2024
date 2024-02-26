from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Program import Program
    from GUI     import GUI

from PyQt5      import QtGui as qg, QtWidgets as qw, QtCore as qc
import numpy as np


class Functions:

    @staticmethod
    def bytt(obj: GUI) -> None:
        """
        Toggles the frame of the stack object in the GUI.
        """
        if obj.temp.currentIndex() == 0:
            obj.temp.setCurrentIndex(1)
        else:
            obj.temp.setCurrentIndex(0)

        #Functions.startSensorReadings(obj, 10)

    @staticmethod
    def on_combo_box_activated(obj: GUI|Program, text: str) -> None:
        """
        When something is clicked in a combo box, the text is fed into the function of the serialDevice that
        defines a new port.
        :param text: The text clicked on in the combo box. Is automatically sent as a parameter.
        """
        text = text.split("-")
        text = str(text[0])
        text = text.strip()
        print(text)
        obj.serialDevice.newPort(text)

    @staticmethod
    def fetchComs(obj: Program) -> None:
        """
        Fetches a list of available ports and adds these to a combo box in the graphical user interface.
        """

        ports = obj.serialDevice.fetchPorts()
        for port in ports:
            obj.combo_box.addItem(port)

    @staticmethod
    def _initSensorReadings(obj: Program) -> None:
        """
        Initialize the QTimer objects that schedules sensor readings.
        """

        # Create a QTimer object
        obj.sensorReader  =   qc.QTimer(obj)

        # Connect the timeout signal of the sensorReader to the function that rotates the plane
        obj.sensorReader.timeout.connect(lambda: Functions._rotatePlane(obj))

    @staticmethod
    def startSensorReadings(obj: Program|GUI, rate: int = 10) -> None:
        """
        Starts reading sensor values from the serial device.
        :param rate: How many readings pr. second.
        """
        obj.sensorReader.start(1000//rate)

    @staticmethod
    def stopSensorReadings(obj: Program) -> None:
        """
        Makes the program stop fetching sensor values from the serial device.
        """
        obj.sensorReader.stop()

    @staticmethod
    def startGame(obj: Program) -> None:

        pass

    @staticmethod
    def _rotatePlane(obj: Program):

        sensorValues = obj.serialDevice.readSerial(printToConsole = False)

        if sensorValues is not None:

            ja = (sensorValues["Sensor1"] / 500)*(np.pi*0.5)
            obj.planeRotation = np.sin(ja) * 100


            # Rotate the label
            rotatedPixmap = qg.QPixmap("Resources/fly.png").transformed(qg.QTransform().rotate(obj.planeRotation))
            obj.image.setPixmap(rotatedPixmap)
            obj.image.move(0, 10)
