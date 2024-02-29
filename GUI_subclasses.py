from __future__ import annotations
from typing import TYPE_CHECKING
from    customwidgets   import  myframe, mylabel, mybutton, mystack
from    PyQt5           import  QtCore
from    PyQt5.QtWidgets import  QStackedLayout, QComboBox
from    functools       import  partial
if TYPE_CHECKING:
    from    GUI             import  GUI
    from    Program         import Program
import  pickle

class menu_frame(myframe):
    
    __slots__ = ["ports_box"]
    
    ports_box: QComboBox
    
    def __init__(self, parent: myframe, top_level: Program) -> None:
        
        super().__init__(
            Master = parent,
            layoutType = "v",
            objectName = "menu_frame",
            add = True
        )
        self.margins(0, 0, 0, 0) 
        self.setMaximumHeight(30)
        self.addstyle(
            commandKey = "background-color", 
            command = "background-color: rgba(200, 200, 200, 255)"
            )
        
        # Create a combo box where available ports should be displayed and add it to 
        # the layout of the menu frame
        self.ports_box = QComboBox()
        self.lay.addWidget(self.ports_box)
        self.ports_box.addItem("No ports available...")
        
        # Import style sheet for the combo box
        with open("Resources/Stylesheets/comboboxStyle.pkl", "rb") as file:
            ports_box_style = str(pickle.load(file))
        self.ports_box.setStyleSheet(ports_box_style)
        
        # When the text of the box is changed, run the function that assigns a new port
        self.ports_box.currentTextChanged.connect(
            partial(top_level.port_selected)
        )
 
class Main_stack_frame_1(myframe):
    
    __slots__ = ["button_1"]
    
    button_1: mybutton
    
    def __init__(self, parent: mystack, top_level: GUI) -> None:
        
        # Create the first slide of the stack
        super().__init__(
            Master = parent, 
            layoutType = "h", 
            objectName="stack_frame_1"
            )
        
        # Create a button and define it's style
        self.button_1 = mybutton(
            Master = self, 
            objectName = "button_1", 
            hover = (100, 100, 100, 100), 
            add=True, 
            text = "Start Game"
            )
        button_1_style = """
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
        self.button_1.setStyleSheet(button_1_style)
        
        # Link the button press to a function that changes the stack slide
        self.button_1.clicked.connect(
            lambda: top_level.gui.main_frame.change_stack_slide(2)
            )
        
        # Add the frame to the parents layout
        parent.addstack(self, "main_stack_stack_frame_1")
         
class Main_stack_frame_2(myframe):
    
    __slots__ = ["stacked_layout", "plane", "target_box"]
    
    stacked_layout: QStackedLayout
    plane: mylabel
    target_box: mylabel
        
    def __init__(self, parent: mystack, top_level: GUI) -> None:
        
        # Initialise the frame
        super().__init__(
            Master = parent, 
            layoutType = "h", 
            objectName = "main_stack_frame_2"
            )
        
        # Create a stacked layout and set stacking mode to stack widgets on top of each other
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.setStackingMode(self.stacked_layout.StackAll)

        # Create the label containing the image of the plane
        self.plane = mylabel(
            Master = self, 
            objectName="plane"
            )
        self.plane.addImage("Resources/fly.png")
        self.plane.setAlignment(QtCore.Qt.AlignCenter)
        self.stacked_layout.addWidget(self.plane)

        # Create the target box, add image of the plane and center.
        self.target_box = mylabel(
            Master = self, 
            objectName = "target_box",
            add = True
            )
        self.target_box.addImage("Resources/greenbox.png")
        self.target_box.setAlignment(QtCore.Qt.AlignCenter)
        self.stacked_layout.addWidget(self.target_box)
        
        # Add the stacked layout to the layout of the frame
        self.lay.addLayout(self.stacked_layout)
                
        # Add the stacked layout to the parent frame
        parent.addstack(self, "main_stack_frame_2")
 
class main_frame(myframe):
    
    __slots__ = ["main_stack", "main_stack_frame_1", "main_stack_frame_2"]
    
    main_stack: mystack
    main_stack_frame_1: Main_stack_frame_1
    main_stack_frame_2: Main_stack_frame_2
    
    def __init__(self, parent: myframe, top_level: GUI) -> None:
        
        # Initialize the main fram and customize appearance
        super().__init__(
            Master = parent,
            layoutType = "h",
            objectName = "main_frame",
            add = True
            )
        self.margins(0, 0, 0, 0)
        self.setMinimumHeight(150)  
        
        # Create a stackable widget
        self.main_stack = mystack(
            Master = self, 
            objectName = "main_stack", 
            add=True
            )
        
        # Initialize the first frame of the main stack
        self.main_stack_frame_1 = Main_stack_frame_1(
            parent = self.main_stack,
            top_level = top_level
            )
        
        # Initialize the second frame of the main stack
        self.main_stack_frame_2 = Main_stack_frame_2(
            parent = self.main_stack,
            top_level = top_level
            )
    
    def change_stack_slide(self, stack_frame: int) -> None:
        """Changes which slide is displayed in the main frame.

        Args:
            stack_frame (int): The frame to be displayed.
        """
        
        self.main_stack.setCurrentIndex(stack_frame - 1)       
   
