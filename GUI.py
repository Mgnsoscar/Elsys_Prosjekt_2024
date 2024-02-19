from    customwidgets   import  *
from    PyQt5           import  QtGui as Qg, QtCore as Qc, QtWidgets as Qw
from Functions import Functions


class GUI(Qw.QMainWindow):

    def __init__(self) -> None:

        # initialize the main window
        Qw.QMainWindow.__init__(self)
        self.resize(1500 // 2, 1000 // 2)

        #### Init a centralwidget, add to main, init central frame, add to central widget
        self.cw = mywidget(self, "v", radius=10)
        self.cf = myframe(self.cw, "v", "cf", add=True,  color=(0, 0, 0, 200))
        self.setCentralWidget(self.cw)  # ,  self.cf.addstyle("image", "border-image: url(:/images/Background3.jpg);")

        GUI._initMainframe(self)
        GUI.initStatusbar(self)
        GUI._initGameFrame(self)

    def _initMainframe(self) -> None:

        # Create 4 main frames
        mainframe = {}

        for i in range(1, 4):
            mainframe[str(i)] = myframe(self.cf, "h", f"mainframe{i}", add=True)

        mainframe["1"].margins(0, 0, 0, 0),     mainframe["1"].setMinimumHeight(30),    mainframe["1"].setMaximumHeight(30)
        mainframe["1"].addstyle("background-color", "background-color: rgba(200, 200, 200, 255)")
        mainframe["2"].margins(10, 10, 10, 10),     mainframe["2"].setMinimumHeight(150)
        mainframe["3"].customradius(0, 0, 10, 10),  mainframe["3"].setFixedHeight(10)

        self.mainframe = mainframe

    def initStatusbar(self):

        # Create a combo box
        self.combo_box = Qw.QComboBox()
        self.combo_box.addItem("No port selected...")
        self.combo_box.setStyleSheet("color: black; background-color: white; radius:0;")
        self.combo_box.activated[str].connect(self.on_combo_box_activated)
        #framm = myframe(self.mainframe["1"], "h", color=(0, 100, 0, 100))

        # Add the combo box to mainframe["1"]
        self.mainframe["1"].lay.addWidget(self.combo_box)

    def on_combo_box_activated(self, text) -> None:
        Functions.on_combo_box_activated(self, text)

    def _initGameFrame(self) -> None:

        temp = mystack(self.mainframe["2"], objectName="stacken", add=True)

        valg = myframe(temp, "h", objectName="forste")
        but = mybutton(valg, objectName="knappen", hover=(100, 100, 100, 100), add=True, text="Bytt")
        but.clicked.connect(lambda: Functions.bytt(self))
        volg = myframe(temp, "h", objectName="andre")

        temp.addstack(valg, "forste")
        temp.addstack(volg, "andre")

        contentFrames = {}

        for i in range(1, 4):
            contentFrames[i] = myframe(volg, "h", f"mainframe{i}", add=True)

        def initMidleContentFrame():

            image = mylabel(contentFrames[2], objectName="Image", add=True)
            image.addImage("Resources/fly.png")

            self.image = image

        initMidleContentFrame()
        self.temp = temp
