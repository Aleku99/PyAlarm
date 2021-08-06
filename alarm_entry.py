import os

from PyQt5.QtWidgets import QMessageBox


if(os.stat("AlarmEntries").st_size == 0):
    index = 0
else:
    with open("AlarmEntries", "r+") as f:
        lines = f.readlines()
        index = int(str(lines[-1].split()[0])[1:-1])

class AlarmEntry:

        def __init__(self, minutes, hour, day, reminder, repetitive):
            global index
            self.minutes = minutes
            self.hour = hour
            self.day = day
            self.reminder = reminder
            self.repetitive = repetitive
            index = index + 1

        def get_data(self):
            global index
            return_list = []
            return_list.append(index)
            return_list.append(self.minutes)
            return_list.append(self.hour)
            return_list.append(self.day)
            return_list.append(self.reminder)
            return_list.append(self.repetitive)
            return return_list
