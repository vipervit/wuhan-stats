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
                worldometer.email.send()
                prev = worldometer.last_updated
            if not __debug__:
                logger.debug('Exiting due to debug mode.')
                sys.exit()

    def __set_interval__(self):
        self._interval = int(self.pollinterval.get()) * 3600000

    def run(self):
        if self.Start["text"] == "Stop":
            self.__set_interval__()
            self.execute()
            self.master.after(self._interval, self.run)

    def startstop_change_title(self):
        if self.Start["text"] == "Start":
            self.Start["text"] = "Stop"
        else:
            self.Start["text"] = "Start"
        self.run()

    def createWidgets(self):

        self.text = Label(self, text="Polling interval (hrs):")
        self.text.pack(side=LEFT)

        self.pollinterval = Spinbox(self, from_=1, to=24, increment=1, width=5)
        self.pollinterval.pack(side=LEFT)

        self.Start = Button(self, text="Start", command=self.startstop_change_title)
        self.Start.pack(side=LEFT)

        self.QUIT = Button(text="QUIT", command=self.quit, fg="red")
        self.QUIT.pack(side=RIGHT)



    def __init__(self, master=None):
        self._interval = None
        Frame.__init__(self, master)
        self.createWidgets()
        self.pack()
