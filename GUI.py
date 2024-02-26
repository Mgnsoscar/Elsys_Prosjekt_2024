from    customwidgets   import  *
from    PyQt5           import  QtGui as Qg, QtCore as Qc, QtWidgets as Qw
from Functions import Functions
import pickle
import numpy as np


class GUI(Qw.QMainWindow):

    def __init__(self) -> None:

        # initialize the main window
        Qw.QMainWindow.__init__(self)
        self.resize(1500 // 2, 1000 // 2)

        #### Init a centralwidget, add to main, init central frame, add to central widget
        self.cw = mywidget(self, "v")
        self.cf = myframe(self.cw, "v", "cf", add=True,  color=(255, 255, 255, 255))
        self.setCentralWidget(self.cw)  ,  self.cf.addstyle("image", "border-image: url(Resources/skies.jpg);")

        GUI._initMainframe(self)
        GUI.initStatusbar(self)
        GUI._initGameFrame(self)

    def _initMainframe(self) -> None:

        # Create 4 main frames
        mainframe = {}

        for i in range(1, 4):
            mainframe[str(i)] = myframe(self.cf, "h", f"mainframe{i}", add=True)

        mainframe["1"].margins(0, 0, 0, 0),    mainframe["1"].setMaximumHeight(30)
        mainframe["1"].addstyle("background-color", "background-color: rgba(200, 200, 200, 255)")
        mainframe["2"].margins(0, 0, 0, 0),     mainframe["2"].setMinimumHeight(150)
        mainframe["3"].customradius(0, 0, 0, 0),  mainframe["3"].setFixedHeight(10)

        self.mainframe = mainframe

    def initStatusbar(self):

        # Create a combo box
        self.combo_box = Qw.QComboBox()
        self.combo_box.addItem("No port selected...")
        
        with open("Resources/Stylesheets/comboboxStyle.pkl", "rb") as file:
            style = str(pickle.load(file))
        
        print(style)

        self.combo_box.setStyleSheet(style)
        self.combo_box.activated[str].connect(self.on_combo_box_activated)
        #framm = myframe(self.mainframe["1"], "h", color=(0, 100, 0, 100))

        # Add the combo box to mainframe["1"]
        self.mainframe["1"].lay.addWidget(self.combo_box)

    def on_combo_box_activated(self, text: str) -> None:
        Functions.on_combo_box_activated(self, text)

    def _initGameFrame(self) -> None:

        temp = mystack(self.mainframe["2"], objectName="stacken", add=True)

        valg = myframe(temp, "h", objectName="forste")
        but = mybutton(valg, objectName="knappen", hover=(100, 100, 100, 100), add=True, text="Bytt")
        style = """
QPushButton {
    background-color: #4CAF50; /* Green */
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    transition-duration: 0.4s;
    cursor: pointer;
    border-radius: 8px;
}
QPushButton:hover {
    background-color: #45a049; /* Darker Green */
    color: white;
}
"""     
        but.setStyleSheet(style)
        but.clicked.connect(lambda: self.bytt())
        volg = myframe(temp, "h", objectName="andre")

        temp.addstack(valg, "forste")
        temp.addstack(volg, "andre")


        contentFrame = myframe(volg, "h", f"contentFrame", add=True)

        def initMidleContentFrame():
            
            # Create a stacked layout to stack widgets on top of each other
            stackedLayout = qw.QStackedLayout()

            image = mylabel(contentFrame, objectName="Image")
            image.addImage("Resources/fly.png")
            image.setAlignment(qc.Qt.AlignCenter)
            stackedLayout.addWidget(image)

            # Create the rectangular box
            rect = mylabel(contentFrame, objectName="box")
            rect.addImage("Resources/greenbox.png")
            rect.setAlignment(qc.Qt.AlignCenter)
            stackedLayout.addWidget(rect)
                
            stackedLayout.setStackingMode(stackedLayout.StackAll)

            contentFrame.lay.addLayout(stackedLayout)
            
            Functions._rotateTargetbox(rect)
            
            self.image = image

        initMidleContentFrame()
        self.temp = temp

    def _initSensorReadings(self) -> None:
        """
        Initialize the QTimer objects that schedules sensor readings.
        """
        
        # Create a QTimer object
        self.sensorReader  =   qc.QTimer(self)

        # Connect the timeout signal of the sensorReader to the function that rotates the plane
        self.sensorReader.timeout.connect(lambda: self._rotatePlane())

    def startSensorReadings(self, rate: int = 10) -> None:
        """
        Starts reading sensor values from the serial device.
        :param rate: How many readings pr. second.
        """

        self.sensorReader.start(1000//rate)

    def _rotatePlane(self):

        sensorValues = self.serialDevice.readSerial(printToConsole = True, sensors=[" Sensor3"])

        if sensorValues is not None:

            ja = (sensorValues["Sensor1"] / 500)*(np.pi*0.5)
            self.planeRotation = np.sin(ja) * 100

            # Rotate the label
            rotatedPixmap = qg.QPixmap("Resources/fly.png").transformed(qg.QTransform().rotate(self.planeRotation))
            self.image.setPixmap(rotatedPixmap)
            #obj.image.move(0, 10)

    def bytt(self) -> None:
        """
        Toggles the frame of the stack object in the GUI.
        """
        if self.temp.currentIndex() == 0:
            self.temp.setCurrentIndex(1)
        else:
            self.temp.setCurrentIndex(0)

        self.startSensorReadings(10)