from    customwidgets   import  *
from    PyQt5           import  QtGui as Qg, QtCore as Qc, QtWidgets as Qw
from    serialIn        import  serialDevice
from    GUI             import  GUI
import  numpy           as      np
import  sys

class Program(GUI):

    def __init__(self):

        super().__init__()

        # Initialize a serial device with standard baudrate of 9600
        self.serialDevice = serialDevice(115200)

        self.fetchComs()

        # Initialize the rotational value of the plane
        self.planeRotation = 0

        self._initSensorReadings()

        #self.startSensorReadings(10)

    def fetchComs(self):

        ports = self.serialDevice.fetchPorts()
        for port in ports:
            self.combo_box.addItem(port)



    def _initSensorReadings(self) -> None:
        """
        Initialize the QTimer objects that schedules sensor readings.
        """

        # Create a QTimer object
        self.sensorReader  =   qc.QTimer(self)

        # Connect the timeout signal of the sensorReader to the function that rotates the plane
        self.sensorReader.timeout.connect(lambda: Functions._rotatePlane(self))

    def startSensorReadings(self, rate: int = 10) -> None:
        """
        Starts reading sensor values from the serial device.
        :param rate: How many readings pr. second.
        """
        self.sensorReader.start(1000//rate)

    def stopSensorReadings(self) -> None:
        """
        Makes the program stop fetching sensor values from the serial device.
        """
        self.sensorReader.stop()


class Functions(Program):

    def _rotatePlane(self):

        sensorValues = np.array( [self.serialDevice.readSerial(printToConsole = True)] )

        # = (serialVal / 500)*(np.pi*0.5)
        #self.rotation = np.sin(ja) * 100

        # Rotate the label
        #rotatedPixmap = Qg.QPixmap("fly.png").transformed(Qg.QTransform().rotate(self.rotation))
        #self.image.setPixmap(rotatedPixmap)

