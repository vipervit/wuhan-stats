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

    def __set_interval__(self):
        reading = int(self.PollingInterval.get())
        self._interval = reading * 3600000

    def __run_counter__(self):
        if self.Start["text"] == "Stop":
            self.Counter["text"] = str(self._elapsed)
            self._elapsed -= 1
            self.master.after(1000, self.__run_counter__)

    def run(self):
        if self.Start["text"] == "Stop":
            self._elapsed = int(self.PollingInterval.get()) * 3600
            self.__run_counter__()
            self.execute()
            self.master.after(self._interval, self.run)

    def startstop_change_title(self):
        if self.Start["text"] == "Start":
            self.Start["text"] = "Stop"
        else:
            self.Start["text"] = "Start"
            self.Counter["text"] = "0"
        self.__set_interval__()
        self.run()

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
