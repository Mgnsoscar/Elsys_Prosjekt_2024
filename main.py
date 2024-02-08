from    customwidgets   import  *
from    PyQt5           import  QtGui as Qg, QtCore as Qc, QtWidgets as Qw
from    serialIn        import  serialDevice
from    GUI             import  GUI
import  numpy           as      np
import  sys

class Main(GUI):

    def __init__(self):

        super().__init__()

        # Initialize a serial device with standard baudrate of 9600
        self.serialDevice = serialDevice(9600)

        # Initialize the rotational value of the plane
        self.planeRotation = 0

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
        self.timer.start(1000//rate)

    def stopSensorReadings(self) -> None:
        """
        Makes the program stop fetching sensor values from the serial device.
        """
        self.timer.stop()


class Functions(Main):

    def _rotatePlane(self):

        sensorValues = np.array( [self.serialDevice.readSerial(sensors = ["leftWing", "rightWing"], printToConsole = True)] )

        # = (serialVal / 500)*(np.pi*0.5)
        #self.rotation = np.sin(ja) * 100

        # Rotate the label
        #rotatedPixmap = Qg.QPixmap("fly.png").transformed(Qg.QTransform().rotate(self.rotation))
        #self.image.setPixmap(rotatedPixmap)

if __name__ == "__main__":

    # Initialize a PyQt5 application
    application = Qw.QApplication(  sys.argv  )

    # Initialize the program
    Main = Main()

    # Show the program
    Main.show()

    # Exit the program when the window is closed
    sys.exit(  application.exec_()  )

