from    customwidgets   import  *
from    PyQt5           import  QtGui as Qg, QtCore as Qc, QtWidgets as Qw


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
        GUI._initGameFrame(self)

    def _initMainframe(self) -> None:

        # Create 4 main frames
        mainframe = {}

        for i in range(1, 3):
            mainframe[str(i)] = myframe(self.cf, "h", f"mainframe{i}", add=True)

        mainframe["1"].margins(10, 10, 10, 10),     mainframe["1"].setMinimumHeight(150),   mainframe["1"].setMinimumHeight(350)
        mainframe["2"].customradius(0, 0, 10, 10),  mainframe["2"].setFixedHeight(10)

        #mainframe["1"].addstyle("border-image", "border-image: url(elmic.jpg);")

        self.mainframe = mainframe

    def _initGameFrame(self) -> None:

        contentFrames = {}

        for i in range(1, 4):
            contentFrames[i] = myframe(self.mainframe["1"], "h", f"mainframe{i}", add=True)

        def initMidleContentFrame():

            image = mylabel(contentFrames[2], objectName="Image", add=True)
            image.addImage("fly.png")

            self.image = image

        initMidleContentFrame()
