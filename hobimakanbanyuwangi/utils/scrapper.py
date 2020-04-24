from subprocess import Popen, PIPE
from django.core.mail import EmailMessage as Email
from config.settings.base import APPS_DIR
import os, re

venv_path = os.environ['VIRTUAL_ENV']
script_path = (str(APPS_DIR / "utils"))

class InstagramAll:
    def cmd(self):
        return [
            f'{venv_path}/bin/instagram-scraper',
            'hobimakan.banyuwangi',
            '--media-metadata',
            '--media-types', 
            'none',
            '-d',
            f'{script_path}/data',
        ]

    def send(self):
        os.system(f"rm -rf {script_path}data/hobimakan.banyuwangi.json")
        p = Popen(self.cmd(),
                  stdin=PIPE,
                  stdout=PIPE,
                  stderr=PIPE)
        output, msg = p.communicate()
        match = re.match("posts: (\d+) m", msg.decode('utf-8'))
        if match:
           return False
        return True

class ExtractorDB:
    def cmd(self):
        return [
            f'{venv_path}/bin/python',
            f'{script_path}/ig-extraction.py',
        ]

    def send(self):
        p = Popen(self.cmd(),
                  stdin=PIPE,
                  stdout=PIPE,
                  stderr=PIPE)
        output,msg = p.communicate()
        return True
        
class RatingExtract:
    def cmd(self):
        return [
            '/home/ubuntu/myproject/bin/python',
            '{script_path}/ig-rating.py',
        ]

    def send(self):
        p = Popen(self.cmd(),
                  stdin=PIPE,
                  stdout=PIPE,
                  stderr=PIPE)
        output,msg = p.communicate()
        return True
