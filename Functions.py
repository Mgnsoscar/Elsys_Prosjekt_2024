from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Program import Program
    from GUI     import GUI

from PyQt5      import QtGui as qg, QtWidgets as qw, QtCore as qc
import numpy as np
import random


class Functions:

    @staticmethod
    def on_combo_box_activated(obj: GUI|Program, text: str) -> None:
        """
        When something is clicked in a combo box, the text is fed into the function of the serialDevice that
        defines a new port.
        :param text: The text clicked on in the combo box. Is automatically sent as a parameter.
        """
        if text == "No port selected...":
            return
        text = text.split("-")
        text = str(text[0])
        text = text.strip()
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

        sensorValues = obj.serialDevice.readSerial(printToConsole = True)

        if sensorValues is not None:

            ja = (sensorValues["Sensor1"] / 500)*(np.pi*0.5)
            obj.planeRotation = np.sin(ja) * 100


            # Rotate the label
            rotatedPixmap = qg.QPixmap("Resources/fly.png").transformed(qg.QTransform().rotate(obj.planeRotation))
            obj.image.setPixmap(rotatedPixmap)
            #obj.image.move(0, 10)

    @staticmethod
    def _rotateTargetbox(boxObj: Program):

        random_integer = random.randint(-60, 60)
            
            # Rotate the label
        rotatedPixmap = qg.QPixmap("Resources/greenbox.png").transformed(qg.QTransform().rotate(random_integer))
        boxObj.setPixmap(rotatedPixmap)

