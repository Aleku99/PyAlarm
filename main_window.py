from tkinter import messagebox


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QComboBox, QLabel, QCheckBox, QMessageBox
import tkinter as tk
import sys
import os
import alarm_entry
import json
from functools import partial
import datetime
from pygame import mixer
import time
import threading


root = tk.Tk()

class MainWindow():

    def __init__(self):
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.title = "PyAlarm"
        self.hours_list = self.list_of_strings(range(25))
        self.minutes_list = self.list_of_strings(range(61))
        self.day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.sounds_list = os.listdir("Sounds")
        self.init = 1
        self.new_entry = 0
        self.hour = "0"
        self.minute = "0"
        self.day = "Monday"
        self.repetitive = False
        self.sound = "default.mp3"
        self.app = QApplication(sys.argv)
        self.alarm_started = 0
        self.stop = False

        self.initUI()

    def initUI(self):

        self.win = QMainWindow()
        self.win.setGeometry(self.screen_width / 2, self.screen_height / 3, self.screen_width / 2, self.screen_height / 2)
        self.win.setWindowTitle(self.title)
        self.show_entries()

        self.reminder_field = QLineEdit(self.win)
        self.reminder_field.setPlaceholderText("Reminder")
        self.reminder_field.move(20, 20)
        self.reminder_field.resize(160, 40)


        self.hour_label = QLabel(self.win)
        self.hour_label.setText("Hour")
        self.hour_label.move(20, 80)

        self.hour_dropdown = QComboBox(self.win)
        self.hour_dropdown.move(80,80)
        self.hour_dropdown.addItems(self.hours_list)
        self.hour_dropdown.activated.connect(self.hour_handle_activated)

        self.minute_label = QLabel(self.win)
        self.minute_label.setText("Minute")
        self.minute_label.move(20, 140)

        self.minute_dropdown = QComboBox(self.win)
        self.minute_dropdown.move(80, 140)
        self.minute_dropdown.addItems(self.minutes_list)
        self.minute_dropdown.activated.connect(self.minute_handle_activated)

        self.day_label = QLabel(self.win)
        self.day_label.setText("Day")
        self.day_label.move(20, 200)

        self.day_dropdown = QComboBox(self.win)
        self.day_dropdown.move(80, 200)
        self.day_dropdown.addItems(self.day_list)
        self.day_dropdown.activated.connect(self.day_handle_activated)

        self.repetitive_label = QLabel(self.win)
        self.repetitive_label.setText("Daily")
        self.repetitive_label.move(20, 260)

        self.repetitive_checkbox = QCheckBox(self.win)
        self.repetitive_checkbox.move(80, 260)


        self.sound_label = QLabel(self.win)
        self.sound_label.setText("Sound")
        self.sound_label.move(20, 320)

        self.sound_dropdown = QComboBox(self.win)
        self.sound_dropdown.move(80, 320)
        self.sound_dropdown.resize(400,30)
        self.sound_dropdown.addItems(self.sounds_list)
        self.sound_dropdown.activated.connect(self.sound_handle_activated)


        self.button = QPushButton('Add alarm', self.win)
        self.button.move(20, 380)
        self.button.clicked.connect(self.onclick)

        self.sound_label = QLabel(self.win)
        self.sound_label.setText("Alarms:")
        self.sound_label.move(700, 20)

        self.run_background_task()

        if self.init == 1:
            self.win.show()
            self.init = 0
            ret = self.app.exec_()
            self.stop = True #stop is used to stop worker thread
            sys.exit(ret)
        else:
            self.win.show()

    def list_of_strings(self, my_list):
        my_list2 = []
        for element in my_list:
            my_list2.append(str(element))
        return my_list2

    def onclick(self):
        new_entry = alarm_entry.AlarmEntry(self.minute, self.hour, self.day, self.reminder_field.text(), self.repetitive_checkbox.isChecked(), self.sound)
        new_entry_list = new_entry.get_data()
        jsonStr = json.dumps(new_entry_list)
        alarm_entry_file = open("AlarmEntries","a")
        alarm_entry_file.write(jsonStr+"\n")
        alarm_entry_file.close()
        self.updateUI()

    def draw_entry(self, element, win, y_pos):
        minutes = str(element.split()[1])[1:-2]
        hour = str(element.split()[2])[1:-2]
        day = str(element.split()[3])[1:-2]
        reminder = str(element.split(",")[4])[2:-1]
        repetitive = str(element.split(",")[5])[0:]

        entry_hour_label = QLabel(win)
        entry_hour_label.setText(hour)
        entry_hour_label.move(600, y_pos)

        entry_minutes_label = QLabel(win)
        entry_minutes_label.setText(minutes)
        entry_minutes_label.move(625, y_pos)

        entry_day_label = QLabel(win)
        entry_day_label.setText(day)
        entry_day_label.move(650, y_pos)

        entry_reminder_label = QLabel(win)
        entry_reminder_label.setText(reminder)
        entry_reminder_label.move(700, y_pos)

        entry_repetitive_label = QLabel(win)
        entry_repetitive_label.setText(f"Repetitive: {repetitive}")
        entry_repetitive_label.move(800, y_pos)

        button = QPushButton('Delete alarm', win)
        button.move(910, y_pos)

        return button

    def delete_entry(self,element):
        entry_to_delete = str(element.split()[0])[1:-1]
        with open("AlarmEntries", "r+") as f:
            d = f.readlines()
            f.seek(0)
            for temp_element in d:
                if entry_to_delete != str(temp_element.split()[0])[1:-1]:
                    f.write(temp_element)
            f.truncate()
        self.updateUI()

    def show_entries(self):
        delete_entry_buttons = []
        try:
            alarm_entries_file = open("AlarmEntries","r")
            entries_list = alarm_entries_file.readlines()
            for index, element in enumerate(entries_list):
                delete_entry_buttons.append(self.draw_entry(element, self.win, index * 40 + 50))
                delete_entry_buttons[-1].clicked.connect(partial(self.delete_entry,element))
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(str(Exception))
            msg.setWindowTitle("Alert")

    def updateUI(self):
        self.win.hide()
        del self.win
        self.initUI()

    def day_handle_activated(self):
        self.day = self.day_dropdown.currentText()
    def hour_handle_activated(self):
        self.hour = self.hour_dropdown.currentText()
    def minute_handle_activated(self):
        self.minute = self.minute_dropdown.currentText()
    def sound_handle_activated(self):
        self.sound = self.sound_dropdown.currentText()

    def sound_alarm(self):
        while self.stop == False:
            now = datetime.datetime.now()
            minutes = str(now.minute)
            hour = str(now.hour)
            day = now.today().strftime("%A")
            try:
                alarm_entries_file = open("AlarmEntries","r")
                entries_list = alarm_entries_file.readlines()
                for index, element in enumerate(entries_list):
                    self.sound = str(element.split(",")[6])[2:-3]
                    if self.alarm_started == 0:
                        if str(element.split()[2])[1:-2] == hour and str(element.split()[1])[1:-2] == minutes and str(element.split()[3])[1:-2] == day:
                            sound_string = "Sounds/" + self.sound
                            print(sound_string)
                            try:
                                mixer.init()
                                mixer.music.load(sound_string)
                                mixer.music.play()
                                time.sleep(60)
                                mixer.music.stop()
                                mixer.quit()
                                self.alarm_started = 1
                            except RuntimeError:
                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Critical)
                                msg.setText(str(RuntimeError))
                                msg.setWindowTitle("Alert")
                        else:
                            print("Not the right time")
                            print(str(element.split()[1])[1:-2] + str(element.split()[2])[1:-2] + str(element.split()[3])[1:-2])
                            print(hour+minutes+day)
            except Exception:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(str(Exception))
                msg.setWindowTitle("Alert")
            self.alarm_started = 0
            time.sleep(1)
        print("stopping")


    def run_background_task(self):
        th = threading.Thread(target=self.sound_alarm)
        th.start()



