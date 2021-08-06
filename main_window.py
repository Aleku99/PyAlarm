from tkinter import messagebox

from infi.systray import SysTrayIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QComboBox, QLabel, QCheckBox, QMessageBox
import tkinter as tk
import sys
import os
import alarm_entry
import json
from functools import partial
root = tk.Tk()
app = QApplication(sys.argv)

class MainWindow():

    def __init__(self):
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.title = "PyAlarm"
        self.hours_list = self.list_of_strings(range(25))
        self.minutes_list = self.list_of_strings(range(61))
        self.day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturnday", "Sunday"]
        self.sounds_list = os.listdir("Sounds")
        self.init = 1
        self.new_entry = 0
        self.initUI()

    def initUI(self):

        win = QMainWindow()
        win.setGeometry(self.screen_width / 2, self.screen_height / 3, self.screen_width / 2, self.screen_height / 2)
        win.setWindowTitle(self.title)
        self.show_entries(win)

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
        sound_dropdown.resize(400,30)
        sound_dropdown.addItems(self.sounds_list)


        button = QPushButton('Add alarm', win)
        button.move(20, 380)
        button.clicked.connect(partial(self.onclick, minute_dropdown.currentText(), hour_dropdown.currentText(), day_dropdown.currentText(),reminder.text(), repetitive_checkbox.isChecked()))

        sound_label = QLabel(win)
        sound_label.setText("Alarms:")
        sound_label.move(700, 20)

        if self.init == 1:
            win.show()
            self.init = 0
            sys.exit(app.exec_())
        else:
            win.show()


    def list_of_strings(self, my_list):
        my_list2 = []
        for element in my_list:
            my_list2.append(str(element))
        return my_list2

    def onclick(self, minutes, hour, day, reminder, repetitive):
        new_entry = alarm_entry.AlarmEntry(minutes, hour, day, reminder, repetitive)
        new_entry_list = new_entry.get_data()
        jsonStr = json.dumps(new_entry_list)
        alarm_entry_file = open("AlarmEntries","a")
        alarm_entry_file.write(jsonStr+"\n")
        alarm_entry_file.close()

    def draw_entry(self, element, win, y_pos):

        minutes = str(element.split()[1])[1:-2]
        hour = str(element.split()[2])[1:-2]
        day = str(element.split()[3])[1:-1]
        reminder = str(element.split()[4])[1:-1]
        repetitive = str(element.split()[5])[0:-1]

        entry_minutes_label = QLabel(win)
        entry_minutes_label.setText(minutes)
        entry_minutes_label.move(600, y_pos)

        entry_hour_label = QLabel(win)
        entry_hour_label.setText(hour)
        entry_hour_label.move(650, y_pos)

        entry_day_label = QLabel(win)
        entry_day_label.setText(day)
        entry_day_label.move(700, y_pos)

        entry_reminder_label = QLabel(win)
        entry_reminder_label.setText(reminder)
        entry_reminder_label.move(750, y_pos)

        entry_repetitive_label = QLabel(win)
        entry_repetitive_label.setText(repetitive)
        entry_repetitive_label.move(800, y_pos)

        button = QPushButton('Delete alarm', win)
        button.move(850, y_pos)

        return button

    def delete_entry(self,element,win):
        entry_to_delete = str(element.split()[0])[1:-1]
        with open("AlarmEntries", "r+") as f:
            d = f.readlines()
            f.seek(0)
            for temp_element in d:
                if entry_to_delete != str(temp_element.split()[0])[1:-1]:
                    f.write(temp_element)
            f.truncate()
        self.updateUI(win)

    def show_entries(self,win):
        delete_entry_buttons = []
        try:
            alarm_entries_file = open("AlarmEntries","r")
            entries_list = alarm_entries_file.readlines()
            for index, element in enumerate(entries_list):
                delete_entry_buttons.append(self.draw_entry(element, win, index * 40 + 50))
                delete_entry_buttons[-1].clicked.connect(partial(self.delete_entry,element,win))
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(Exception))
            msg.setWindowTitle("Alert")

    def updateUI(self,win):
        win.hide()
        del win
        self.initUI()




