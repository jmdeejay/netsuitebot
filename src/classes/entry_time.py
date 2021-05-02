# Standard library imports
import re

# Third party imports
import tkinter as tk


class EntryTime(tk.Entry):
    def __init__(self, master=None, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)
        self.bind("<FocusOut>", self.foc_out)

    def format_time(self, time):
        clean_time = re.sub(r"[^0-9:.]", "", time)
        if clean_time == "":
            return ""

        if re.match(r"^-?\d+(?:\.\d+)$", clean_time):  # 7.5
            pos = clean_time.find(".")
            hours = int(clean_time[0:pos])
            minutes = 0
            if pos != -1:
                float_minutes = int(clean_time[pos+1:len(clean_time)].ljust(2, "0"))
                if float_minutes > 99:
                    float_minutes = 99
                minutes = int(float_minutes / 100 * 60)
        elif re.match(r"^([0-9]|[0-9][0-9]):([0-9]|[0-9][0-9])$", clean_time):  # 7:30
            pos = clean_time.find(":")
            hours = int(clean_time[0:pos])
            minutes = int(clean_time[pos+1:len(clean_time)])
        elif re.match(r"^([0-9]|[0-9][0-9])$", clean_time):  # 7
            hours = int(clean_time)
            minutes = 0
        else:
            return ""

        if hours > 23:
            hours = 0
        if minutes > 59:
            minutes = 59

        return str(hours) + ":" + str(minutes).zfill(2)

    def foc_out(self, *args):
        time = self.format_time(self.get())
        self.delete("0", "end")
        self.insert(0, time)
