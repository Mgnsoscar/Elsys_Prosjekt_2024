from __future__ import annotations
from    PyQt5           import  QtGui as qg, QtCore as qc, QtWidgets as qw
from    PyQt5.QtCore    import  QTimer
from    serialIn        import  SerialDevice
import numpy as np
from GUI import GUI

class Program():

    __slots__ = (
        "gui",
        "serial_device", 
        "plane_rotation", 
        "sensor_reader",
        "target_box_rotation"
        )

    gui: GUI
    serial_device: SerialDevice
    plane_rotation: int
    sensor_reader: qc.QTimer
    target_box_rotation: int
    
    def __init__(self) -> None:
        
        # Initialize the graphical user interface
        self.gui = GUI(top_level = self)
        
        # Initialize a serial device with standard baudrate of 9600
        self.serial_device = SerialDevice(115200)
        
        # Initialize the sensor_readers
        self.initialize_sensor_readings()

        # Initialize the rotational value of the plane as 0
        self.plane_rotation = 0
        
        # Initialize the target box rotation as 0
        self.target_box_rotation = 0
        
        # Fetch and display available ports in the user interface
        self.fetch_available_ports()
  
    def port_selected(self, text: str) -> None:
        """
        When something is clicked in the combo box displaying available ports, 
        the text is fed into the function of the serialDevice that defines a new port.
        
        :param text: The text clicked on in the combo box. Is automatically sent as a parameter.
        """
        if text == "No port selected...":
            print("Works")
            return
        text = str(text.split("-")[0]).strip()
        try:
            self.serial_device.newPort(text)
        except:
            pass  

    def fetch_available_ports(self) -> None:
        
        self.gui.display_available_ports(
            self.serial_device.fetchPorts()
        )

    def compute_plane_rotation(self) -> None:

        try:
            sensorValues = self.serialDevice.readSerial(printToConsole = True, sensors=[" Sensor3"])

            if sensorValues is not None:

                ja = (sensorValues["Sensor1"] / 500)*(np.pi*0.5)
                self.plane_rotation = np.sin(ja) * 100
                
                self.gui.rotate_plane(self.plane_rotation)
      
        except:
            
            pass  
      
    def game_ready_for_start(self) -> bool:
        
        # TODO 
        # Make a function that checks if the program recieves sensor readings and make
        pass

    def get_stability(self) -> float:
        
        # TODO
        # Make a function that calculates the stability of the plane in the game
        pass  

    def start_game(self) -> None:
        
        # TODO
        # Make a function that starts the game
        pass
        
    def initialize_sensor_readings(self) -> None:
        """Initialize the QTimer objects that schedules sensor readings, and 
        link the QTimer to the rotate_plane function of GUI_functions.
        """
        
        # Create a QTimer object
        self.sensor_reader  =   QTimer(self.gui)

        # Connect the timeout signal of the sensorReader to the function that rotates the plane
        self.sensor_reader.timeout.connect(lambda: self.rotate_plane())

    @staticmethod
    def start_readings(reader: QTimer, rate: int = 10) -> None:
        """Starts a sensor reading with a specified rate.

        Args:
            sensor_reader (qc.QTimer): The QTimer instance related to a specific sensor reading.
            rate (int, optional): How many times a second the sensor reading should be excecuted. Defaults to 10.
        """

        reader.start(1000//rate)

    @staticmethod
    def stop_readings(reader: QTimer) -> None:
        """Makes the program stop fetching sensor values from the serial device.

        Args:
            sensor_reader (QTimer): The sensor reader that should be stopped.
        """
        reader.stop()
