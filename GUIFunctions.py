from main import *
import datetime

GLOBAL_STATE = 0

class Ui_Functions(MainWindow):

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE

        if status == 0:

            self.showMaximized()

            GLOBAL_STATE = 1

            #self.drop_shadow_layout.setContentsMargins(0, 0, 0, 0)
            self.ui.centrawidget.setStyleSheet("border-radius: 0px;")


        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            #self.drop_shadow_layout.setContentsMargins(10, 10, 10, 10)
            #self.ui.centrawidget.setStyleSheet("border-radius: 15px;")
    def Ui_definitions(self):

        self.ui.maximize.clicked.connect(lambda: Ui_Functions.maximize_restore(self))

    def timer(self, work):

        #### Define what to do if the start button is pressed:

        if work == 'start':

            self.timer_running = True

            if self.timer_counter_num == 0:
                timer_time_str = '00:15:20'
                hours, minutes, seconds = timer_time_str.split(':')
                minutes = int(minutes) + (int(hours) * 60)
                seconds = int(seconds) + (minutes * 60)
                self.timer_counter_num = self.timer_counter_num + seconds
            # print('hei')
            timer_counter()

        # elif work == 'stop':
        #         self.timer_running = False
        #         self.start.configure(state='normal')
        #         self.stop.configure(state='disabled')
        #         self.reset.configure(state='normal')
        #
        # elif work == 'reset':
        #         self.timer_running = False
        #         self.timer_counter_num = 0

    def timer_counter(self):
        def count():

            if self.timer_running:

                if self.timer_counter_num == 0:

                    self.timer_running = False
                    self.timer('reset')
                    display = '00:00:00'

                else:
                    tt = datetime.timedelta(seconds=self.timer_counter_num)
                    display = tt
                    self.timer_counter_num -= 1

            self.lcdtime.display(f'{display}')
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(count)
            self.timer.setInterval(1000)  # 1000ms = 1s
            self.timer.start()

        count()