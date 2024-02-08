import serial.tools.list_ports


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

    def readSerial(self):

        packet = str(self.device.read_all())
        print(packet)
        #val = int(packet.split("\\n")[-2].rstrip("\\r"))
        self.device.flushInput()
        #return val


ser = serialDevice()
