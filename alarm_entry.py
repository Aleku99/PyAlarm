from PyQt5.QtWidgets import QMessageBox

class AlarmEntry:
        def __init__(self, minutes, hour, day, reminder, repetitive):
            self.minutes = minutes
            self.hour = hour
            self.day = day
            self.reminder = reminder
            self.repetitive = repetitive

        def get_data(self):
            return "" + self.minutes + self.hour + self.day + self.reminder + self.repetitive
