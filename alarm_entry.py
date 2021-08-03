from PyQt5.QtWidgets import QMessageBox
index = 0
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
