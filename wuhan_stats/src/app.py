import time
import  logging

from tkinter import *

from wuhan_stats.src.site import site as site

logger = logging.getLogger(__name__)

class Application(Frame):

    def execute(self):
        prev = ''
        with site('Worldometer') as worldometer:
            worldometer.get()
            if prev < worldometer.last_updated:
                worldometer.desktop.send()
                if self._checkboxval.get() == 1:
                    worldometer.email.send()
                prev = worldometer.last_updated
            if not __debug__:
                logger.debug('Exiting due to debug mode.')
                sys.exit()

    def __interval_set__(self):
        self._interval = int(self.PollingInterval.get()) * 3600000

    def __counter_set__(self):
        self._elapsed = int(self.PollingInterval.get()) * 3600

    def __counter_update__(self):
        reset = False
        if self._elapsed > 0 and self.Start["text"] != "Start":
            self._elapsed -= 1
        else:
            reset = True
        if reset:
            self._elapsed = 0
            return
        self.Counter["text"] = self._elapsed
        self.master.after(1000, self.__counter_update__)

    def run(self):
        self.__counter_update__()
        if self.Start["text"] == "Stop":
            self.execute()
            self.master.after(self._interval, self.run)

    def startstop_change_title(self):
        if self.Start["text"] == "Start":
            self.Start["text"] = "Stop"
            self.__interval_set__()
            self.__counter_set__()
            self.run()
        else:
            self.Start["text"] = "Start"
            self.Counter["text"] = "0"

    def createWidgets(self):

        self.SendEmail = Checkbutton(text='Email    ', variable=self._checkboxval).pack(side=LEFT)
        self.Text = Label(text="Polling(hrs):").pack(side=LEFT)
        self.PollingInterval = Spinbox(from_=1, to=24, increment=1, width=5)
        self.PollingInterval.pack(side=LEFT)
        self.Counter = Button(text="0", width=4)
        self.Counter.pack(side=LEFT)
        self.Start = Button(text="Start", command=self.startstop_change_title)
        self.Start.pack(side=LEFT)
        self.QUIT = Button(text="QUIT", command=self.quit, fg="red").pack(side=RIGHT)

    def __init__(self, master=None):
        self._interval = None
        self._elapsed = 0
        self._checkboxval = IntVar()
        Frame.__init__(self, master)
        self.createWidgets()
        self.pack()
