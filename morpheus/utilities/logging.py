from pathlib import Path
import json, datetime, os
from datetime import datetime
from django.urls import reverse
from utilities.models import SystemLog

BASE_DIR = Path(__file__).resolve().parent.parent
print(type(BASE_DIR), BASE_DIR)            

LOG_LEVEL = (
        'VERBOSE',
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL',
    )

class SystemLogger():
    def __init__(self, area, message, details, level='INFO'):
        self.logitem = {}
        print("Type", type(self.logitem))
        self.logitem['area'] = area
        self.logitem['message'] = message
        self.logitem['details'] = details
        self.logitem['level'] = level

    def log(self):
        #write to file log and database
        #if DB write fails, log additional msg in file

        f = open('systemlog.json', 'a')
        self.logitem['date_time'] = str(datetime.now())
        log_json = json.dumps(self.logitem, indent=2) 
        f.write(log_json + ',\n')
        f.close

        try:
            new_log = SystemLog(
            date_time = str(datetime.now()),
            area = self.logitem['area'],
            message = self.logitem['message'],
            details = self.logitem['details'],
            level = self.logitem['level'],
            )
            new_log.save()
        except Exception as error:
            f = open('systemlog.json', 'a')
            self.logitem['date_time'] = str(datetime.now())
            self.logitem['area'] = 'System Log'
            self.logitem['message'] = 'Unable to write error to DB'
            self.logitem['details'] = str(error)
            self.logitem['level'] = 'WARNING' 
            log_json = json.dumps(self.logitem, indent=2) 
            f.write(log_json + ',\n')
            f.close       




