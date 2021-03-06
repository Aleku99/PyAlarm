import os



if(not os.path.exists("AlarmEntries")):
    index = 0
    f = open("AlarmEntries", "w")
    f.close()

elif os.stat("AlarmEntries").st_size == 0:
    index = 0

else:
    with open("AlarmEntries", "r+") as f:
        lines = f.readlines()
        index = int(str(lines[-1].split()[0])[1:-1])


class AlarmEntry:

        def __init__(self, minutes, hour, day, reminder="No reminder", repetitive="false", sound="theresnomusicfilesinthesoundfolderhahaha"):
            global index
            self.minutes = minutes
            self.hour = hour
            self.day = day
            self.reminder = reminder
            self.repetitive = repetitive
            self.sound = sound
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
            return_list.append(self.sound)
            return return_list
