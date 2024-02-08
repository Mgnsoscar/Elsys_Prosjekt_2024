from customwidgets import *
from PyQt5.QtGui import QGuiApplication, QCursor, QPixmap, QTransform
from PyQt5 import QtCore as qc
from PyQt5.QtCore import QTimer
import serial.tools.list_ports

from datetime import *
import numpy as np
import sys

class Main(qw.QMainWindow):

    def __init__(self):

        self.ser = serialDevice()


        # Bool to know if the window is maximized or normal
        self.maximized = False

        # initialize the main window, remove frames, make translucent, set size
        qw.QMainWindow.__init__(self)
        #self.setWindowFlags(qc.Qt.FramelessWindowHint)
        #self.setAttribute(qc.Qt.WA_TranslucentBackground)
        self.resize(1500 // 2, 1000 // 2)

        self.rotation = 0

        # Run the gui init
        GUI.init(self)

        # Create a QTimer object
        self.timer = QTimer(self)
        # Connect the timeout signal of the timer to a function
        self.timer.timeout.connect(lambda: self.myFunction())
        # Set the interval to trigger the timeout signal every 100 milliseconds (10 times a second)
        self.timer.start(100)


    def myFunction(self):
        serialVal = self.ser.readSerial()
        ja = (serialVal/500)*(np.pi*0.5)
        self.rotation = np.sin(ja) * 100

        GUI.rotatePlane(self)

    def keyPressEvent(self, event):
        # Override the keyPressEvent method
        # This method is called every time a key is pressed
        #self.ser.readSerial()
        pass


# The main frame containing the sub-elements of the gui
class GUI(Main):

    def init(self):

        #### Init a centralwidget, add to main, init central frame, add to central widget
        self.cw = mywidget(self, "v", radius=10)
        self.cf = myframe(self.cw, "v", "cf", add=True, radius=10, color=(0, 0, 0, 200))
        self.setCentralWidget(self.cw)  # ,  self.cf.addstyle("image", "border-image: url(:/images/Background3.jpg);")

        GUI.initMainframe(self)
        GUI.initGameFrame(self)

    def initMainframe(self):

        # Create 4 main frames
        mainframe = {}

        for i in range(1, 3):
            mainframe[str(i)] = myframe(self.cf, "h", f"mainframe{i}", add=True)

        mainframe["1"].margins(10, 10, 10, 10),     mainframe["1"].setMinimumHeight(150),   mainframe["1"].setMinimumHeight(350)
        mainframe["2"].customradius(0, 0, 10, 10),  mainframe["2"].setFixedHeight(10)

        #mainframe["1"].addstyle("border-image", "border-image: url(elmic.jpg);")

        self.mainframe = mainframe

    def initGameFrame(self):

        contentFrames = {}

        for i in range(1, 4):
            contentFrames[i] = myframe(self.mainframe["1"], "h", f"mainframe{i}", add=True)

        def initMidleContentFrame():

            image = mylabel(contentFrames[2], objectName="Image", add=True)
            image.addImage("fly.png")

            self.image = image

        initMidleContentFrame()

    def rotatePlane(self):

        # Rotate the label
        rotated_pixmap = QPixmap("fly.png").transformed(QTransform().rotate(self.rotation))
        self.image.setPixmap(rotated_pixmap)



# Some functions that eases use
class functions(Main):

    def max_restore(self):

        if self.maximized == False:
            self.cw.radius(0), self.cf.radius(0), self.mainframe["1"].customradius(0, 0, 0, 0), self.showMaximized()
            self.maximized = True

        else:
            self.cw.radius(10), self.cf.radius(10), self.mainframe["1"].customradius(10, 10, 0, 0), self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.maximized = False

    def buttonconfig(self):
        # close/maximize/minimize buttons:
        self.button["1"].clicked.connect(self.showMinimized), self.button["2"].clicked.connect(
            lambda: functions.max_restore(self))
        self.button["3"].clicked.connect(self.close)





class serialDevice:


    def __init__(self):

        #Definerer portene
        ports = serial.tools.list_ports.comports()
        self.device = serial.Serial()
        portsList = []

        for onePort in ports:
            portsList.append(str(onePort))

        self.device.baudrate = 9600
        self.device.port = "COM4"
        self.device.timeout = 1
        self.device.open()
        self.device.flushInput()

    def readSerial(self):


        packet = str(self.device.read_all())

        try:
            val = packet.split("\\n")[-2].rstrip("\\r")
            if val.startswith("b'"):
                val = val[2:]
            val=int(val)
        except:
            val = 0

        print(val)
        return val

# Initialize a PyQt5 application
application = qw.QApplication(  sys.argv  )

# Initialize the program
Main = Main()

# Show the program
Main.show()

# Exit the program when the window is closed
sys.exit(  application.exec_()  )

