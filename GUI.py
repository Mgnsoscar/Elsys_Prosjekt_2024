from __future__ import annotations
from    GUI_subclasses  import  menu_frame, main_frame
from    PyQt5.QtWidgets import  QMainWindow
from    PyQt5.QtGui     import  QPixmap, QTransform
from    customwidgets   import  myframe, mywidget
from    typing          import  List, TYPE_CHECKING

if TYPE_CHECKING:
    from Program import Program

class GUI(QMainWindow):

    def __init__(self, top_level: Program) -> None:

        # initialize the main window and resize
        QMainWindow.__init__(self)
        self.resize(
            1500 // 2, 
            1000 // 2
            )

        #### Initialize a centralwidget, add to main, init central frame, add to central widget
        self.central_widget = mywidget(
            Master = self, 
            layoutType = "v"
            )
        self.setCentralWidget(self.central_widget)
        
        # Create the central frame where all subsequent frames are supposed to be.
        self.central_frame = myframe(
            Master = self.central_widget, 
            layoutType = "v", 
            objectName = "central_frame", 
            add = True,  
            color=(255, 255, 255, 255)
            )
        self.central_frame.addstyle("image", "border-image: url(Resources/skies.jpg);")
        

        # Initialize the menu section
        self.menu_frame = menu_frame(
            parent = self.central_frame,
            top_level = top_level
        )

        # Initialize the main frame where most of the content will be
        self.main_frame = main_frame(
            parent = self.central_frame,
            top_level = top_level
        )
        
    def rotate_plane(self, rotation: int) -> None:

        # Rotate the label
        rotated_pixmap = QPixmap("Resources/fly.png").transformed(QTransform().rotate(rotation))
        self.main_frame.main_stack_frame_2.plane.setPixmap(rotated_pixmap)
            
    def rotate_targetbox(self, rotation: int) -> None:
        # TODO
        # Make a function that after som time interval reorients the target box.
        pass

    def display_available_ports(self, list_of_ports: List[str]) -> None:
        """Fetches a list of available ports and adds these to a combo box in the graphical user interface.

        Args:
            instance (Program): An instance of the program.
        """
        
        items = []
        # Remove all items previously in the box
        for item_index in range(self.menu_frame.ports_box.count()):
            self.menu_frame.ports_box.removeItem(
                item_index
            )
        
        if len(list_of_ports) > 0:
            self.menu_frame.ports_box.addItems(
                list_of_ports
            )
        else:
            self.menu_frame.ports_box.addItem("No ports avaliable...")
    
        
