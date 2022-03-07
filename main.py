import sys
import os
from playsound import playsound
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer


class MyApp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.ui_file = os.path.dirname(__file__) + "resources/break-alarm.ui"
        uic.loadUi(self.ui_file, self)
        self.show()
        # global variable
        self.state = False
        self.clockVar = 0
        self.workState = True
        self.timeVar = [0, 0, 0]
        self.roundVar = 0
        # Triggers

        # Define Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.clock_func)
        self.timer.start(1000)  # in milli seconds
        self.pushButton.clicked.connect(self.start_stop)

    def start_stop(self):
        self.state = not self.state
        if self.state:
            try:
                self.timeVar[0] = int(self.plainTextWork.toPlainText()) * 60
                self.timeVar[1] = int(self.plainTextBreak.toPlainText()) * 60
                self.timeVar[2] = int(self.plainTextRepeat.toPlainText())
                self.pushButton.setText('خاموش')
                self.monitor.setText("وقت کاره")
            except:
                self.dlg_show()
                return
        else:
            self.plainTextWork.clear()
            self.plainTextBreak.clear()
            self.plainTextRepeat.clear()
            self.pushButton.setText('روشن')
            self.clockVar = 0
            self.roundVar = 0
            self.monitor.setText("برنامه خاموشه!")

        self.plainTextWork.setDisabled(self.state)
        self.plainTextBreak.setDisabled(self.state)
        self.plainTextRepeat.setDisabled(self.state)
        self.clock_func()

    def clock_func(self):
        if self.workState and self.state:
            if self.clockVar < self.timeVar[0]:
                self.clockVar += 1
            else:
                self.clockVar = 0
                self.workState = False
                self.monitor.setText("پاشو استراحت کن")
                audio_file = os.path.dirname(__file__) + "/resources/break.wav"
                playsound(audio_file)

        elif not self.workState and self.state:
            if self.clockVar < self.timeVar[1]:
                self.clockVar += 1
            else:
                self.clockVar = 0
                self.workState = True
                self.roundVar += 1
                if self.roundVar < self.timeVar[2]:
                    self.monitor.setText("وقت کاره")
                    audio_file = os.path.dirname(__file__) + "/resources/work.wav"
                    playsound(audio_file)
                else:
                    self.start_stop()

    def dlg_show(self):
        dlg = QMessageBox(self)
        # setting text to the dlg
        dlg.setText("توی کادر عدد وارد کنید.")
        # setting icon to it
        dlg.setIcon(QMessageBox.Critical)
        # showing it
        dlg.show()


def main():
    # creating PyQt5 application
    app = QApplication(sys.argv)

    # setting application name
    app.setApplicationName("Work-Break timer")

    # creating a main window object
    window = MyApp()

    # loop
    app.exec_()


if __name__ == '__main__':
    main()
