from infi.systray import SysTrayIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QComboBox, QLabel, QCheckBox
import tkinter as tk
import sys
import os
import alarm_entry
root = tk.Tk()

class MainWindow():

    def __init__(self):
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.title = "PyAlarm"
        self.hours_list = self.list_of_strings(range(25))
        self.minutes_list = self.list_of_strings(range(61))
        self.day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturnday", "Sunday"]
        self.sounds_list = os.listdir("Sounds")
        self.initUI()

    def initUI(self):
        app = QApplication(sys.argv)
        win = QMainWindow()
        win.setGeometry(self.screen_width / 2, self.screen_height / 3, self.screen_width / 2, self.screen_height / 2)
        win.setWindowTitle(self.title)


        reminder = QLineEdit(win)
        reminder.setPlaceholderText("Reminder")
        reminder.move(20, 20)
        reminder.resize(160, 40)

        hour_label = QLabel(win)
        hour_label.setText("Hour")
        hour_label.move(20, 80)

        hour_dropdown = QComboBox(win)
        hour_dropdown.move(80,80)
        hour_dropdown.addItems(self.hours_list)

        minute_label = QLabel(win)
        minute_label.setText("Minute")
        minute_label.move(20, 140)

        minute_dropdown = QComboBox(win)
        minute_dropdown.move(80, 140)
        minute_dropdown.addItems(self.minutes_list)

        day_label = QLabel(win)
        day_label.setText("Day")
        day_label.move(20, 200)

        day_dropdown = QComboBox(win)
        day_dropdown.move(80, 200)
        day_dropdown.addItems(self.day_list)

        repetitive_label = QLabel(win)
        repetitive_label.setText("Daily")
        repetitive_label.move(20, 260)

        repetitive_checkbox = QCheckBox(win)
        repetitive_checkbox.move(80, 260)

        sound_label = QLabel(win)
        sound_label.setText("Sound")
        sound_label.move(20, 320)

        sound_dropdown = QComboBox(win)
        sound_dropdown.move(80, 320)
        sound_dropdown.resize(500,30)
        sound_dropdown.addItems(self.sounds_list)


        button = QPushButton('Add alarm', win)
        button.move(20, 380)
        button.clicked.connect(self.onclick(minute_dropdown.currentText(),hour_dropdown.currentText(),day_dropdown.currentText(),reminder.text(),repetitive_checkbox.isChecked())) #TODO: partial function



        win.show()
        sys.exit(app.exec_())

    def list_of_strings(self, my_list):
        my_list2 = []
        for element in my_list:
            my_list2.append(str(element))
        return my_list2

    def onclick(self, minutes, hour, day, reminder, repetitive):
        new_entry = alarm_entry.AlarmEntry()
        new_entry_list = new_entry.get_data()
        alarm_entry_file = open("AlarmEntries","a")
        alarm_entry_file.write("\n"+new_entry_list)
        alarm_entry_file.close()



