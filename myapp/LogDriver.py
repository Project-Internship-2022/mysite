
import logging as log
from datetime import date
from socket import gethostbyname, gethostname
from mysite.settings import STATIC_ROOT 
import os

class LogDriver:

    def __init__(self, *args, **kwargs):
        self.consoleFormatter: log.Formatter = None
        self.consoleHandler: log.StreamHandler = None
        self.report: log.Logger = None
        self.record: log.Logger = None

    def set_record_handler(self):
        try:
            os.mkdir(STATIC_ROOT + "\logs")
        except:
            pass
        self.LogFileHandler = log.FileHandler(filename = STATIC_ROOT +  f"/logs/{str(date.today())}-{str(gethostbyname(gethostname()))}.txt")
        self.LogFileHandler.setLevel(log.DEBUG)
        self.LogFileFormatter = log.Formatter(f"#Timestamp :  %(asctime)s \n %(message)s \n{'-'*200}",datefmt='%d-%m-%Y  %H:%M')
        self.LogFileHandler.setFormatter(self.LogFileFormatter)
        self.record = log.getLogger('record')
        self.record.setLevel(log.DEBUG)
        self.record.addHandler(self.LogFileHandler)
        self.record.info("Handler Launched successfully...")
       
    def set_console_handler(self):
        self.consoleHandler = log.StreamHandler()
        self.consoleHandler.setLevel(self.REPORT_LEVEL)
        self.consoleFormatter = log.Formatter(f"{self.command_prompt} : %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.consoleHandler.setFormatter(self.consoleFormatter)
        self.report.addHandler(self.consoleHandler)




