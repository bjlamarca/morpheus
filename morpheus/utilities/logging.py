from pathlib import Path
import json, datetime, os
from datetime import datetime
from django.urls import reverse
from utilities.models import SystemLog
from django.contrib.contenttypes.models import ContentType

BASE_DIR = Path(__file__).resolve().parent.parent
         

LOG_LEVEL = (
        'VERBOSE',
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL',
    )

class SystemLogger():
    def __init__(self, content_type, module):
        self.logitem = {}
        self.logitem['content_type'] = content_type
        self.logitem['modeule'] = module
        self.logitem['method'] = ''
        self.logitem['message'] = ''
        self.logitem['details'] = ''
        self.logitem['level'] = ''

    def log(self, module, message, details, level):
        self.logitem['module'] = module
        self.logitem['message'] = message
        self.logitem['details'] = details
        self.logitem['level'] = level

        #write to file log and database
        #if DB write fails, log additional msg in file
        try:
            content_type = ContentType.objects.get(app_label=self.logitem['content_type'])
        except:
            content_type = None
        f = open('logs/systemlog.log', 'a')
        self.logitem['date_time'] = str(datetime.now())
        log_json = json.dumps(self.logitem, indent=2) 
        f.write(log_json + ',\n')
        f.close

        try:
            new_log = SystemLog()
            new_log.date_time = str(datetime.now())
            if content_type:
                new_log.content_type = content_type
            new_log.area = self.logitem['area']
            new_log.message = self.logitem['message']
            new_log.details = self.logitem['details']
            new_log.level = self.logitem['level']
            new_log.save()

        except Exception as error:
            f = open('systemlog.log', 'a')
            self.logitem['date_time'] = str(datetime.now())
            self.logitem['area'] = 'System Log'
            self.logitem['message'] = 'Unable to write error to DB'
            self.logitem['details'] = str(error)
            self.logitem['level'] = 'WARNING' 
            log_json = json.dumps(self.logitem, indent=2) 
            f.write(log_json + ',\n')
            f.close       




