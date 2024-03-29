import sys
from Program import Program
from PyQt5 import QtWidgets as Qw

if __name__ == "__main__":

    # Initialize a PyQt5 application
    application = Qw.QApplication( sys.argv )

    # Initialize the program
    Prog = Program()

    # Show the program
    Prog.gui.show()

    # Exit the program when the window is closed
    sys.exit( application.exec_() )

