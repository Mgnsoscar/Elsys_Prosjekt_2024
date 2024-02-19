from    PyQt5           import  QtGui as Qg, QtCore as Qc, QtWidgets as Qw
from    serialIn        import  serialDevice
from    GUI             import  GUI
from    Functions       import  Functions

class Program(GUI):

    __slots__ = ("serialDevice", "planeRotation", "sensorReader")

    serialDevice:       serialDevice
    planeRotation:      int
    sensorReader:       Qc.QTimer

    def __init__(self):

        super().__init__()

        # Initialize a serial device with standard baudrate of 9600
        self.serialDevice = serialDevice(115200)

        Functions.fetchComs(self)

        # Initialize the rotational value of the plane
        self.planeRotation = 0

        Functions._initSensorReadings(self)

        #Functions.startSensorReadings(self, 10)

