import time
import  logging

from tkinter import *

from wuhan_stats.src.site import site as site
from wuhan_stats import logger

class Application(Frame):

    def execute(self):
        if not __debug__:
            logger.debug(self._elapsed)
        else:
            prev = ''
            with site('Worldometer') as worldometer:
                worldometer.get()
                if prev < worldometer.last_updated:
                    worldometer.desktop.send()
                    if self.__email_alert_enabled__():
                        worldometer.email.send()
                    prev = worldometer.last_updated

    def __email_alert_enabled__(self):
        if self._checkboxval.get() == 1:
            return True
        else:
            return False

    def __polling_period_read__(self):
        return int(self.PollingInterval.get())

    def __polling_period_seconds__(self, debug=__debug__):
        if not __debug__:
            n = 10000 # 10 sec
        else:
            n = 3600000 # 1 hour
        return self.__polling_period_read__() * n

    def __polling_period_reset__(self):
        if not self._running:
            self._period = self.__polling_period_seconds__()
            self.__counter_reset__()

    def __counter_start_value__(self, debug=__debug__):
        return int(self._period / 1000)

    def __counter_display_set__(self):
        self.Counter["text"] = self._elapsed

    def __counter_reset__(self):
        self._elapsed = self.__counter_start_value__()
        self.__counter_display_set__()

    def __counter_run__(self):
        if self._running:
            if self._elapsed-1 > 0:
                self._elapsed -= 1
            else:
                self.__counter_reset__()
            self.Counter["text"] = self._elapsed
            self.master.after(1000, self.__counter_run__) # 1000 = update every second

    def run(self):
        if self._running:
            self.execute()
            self.master.after(self._period, self.run)

    def startstop_change_title(self):
        if not self._running:
            self._running = True
            self.Start["text"] = "Stop"
            self.run()
            self.__counter_run__()
        else:
            self._running = False
            self.Start["text"] = "Start"
            self.__counter_reset__()
            self.__polling_period_reset__()

    def createWidgets(self):

        self.SendEmail = Checkbutton(text='Email    ', variable=self._checkboxval).pack(side=LEFT)
        Label(text="Polling(hrs):").pack(side=LEFT)
        self.PollingInterval = Spinbox(from_=1, to=24, increment=1, width=5, command=self.__polling_period_reset__)
        self.PollingInterval.pack(side=LEFT)
        Label(text="Next in sec:").pack(side=LEFT)
        self.Counter = Button(text="0", width=4)
        self.Counter.pack(side=LEFT)
        self.Start = Button(text="Start", command=self.startstop_change_title)
        self.Start.pack(side=LEFT)
        self.QUIT = Button(text="QUIT", command=self.quit, fg="red").pack(side=RIGHT)
        self.__polling_period_reset__()
        self.__counter_reset__()

    def __init__(self, master=None):
        self._elapsed = 0
        self._period = None
        self._running = False
        self._checkboxval = IntVar()
        Frame.__init__(self, master)
        self.createWidgets()
        self.pack()
