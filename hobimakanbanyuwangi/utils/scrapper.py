from subprocess import Popen, PIPE
from config.settings.base import APPS_DIR
import os, re

venv_path = os.environ['VIRTUAL_ENV']
script_path = (str(APPS_DIR / "utils"))

class CollectData:
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
        os.system(f"rm -rf {script_path}/data/hobimakan.banyuwangi.json")
        print ("start scraper")
        p = Popen(self.cmd(),
                  stdin=PIPE,
                  stdout=PIPE,
                  stderr=PIPE)
        output, msg = p.communicate()
        match = re.search("posts: (\d+) m", msg.decode('utf-8'))
        if match:
           return True
        return False

class InstagramExtraction:
    def cmd(self):
        return [
            f'{venv_path}/bin/python',
            f'{script_path}/instagram-extraction.py',
        ]

    def send(self):
        print ("start extraction")
        p = Popen(self.cmd(),
                  stdin=PIPE,
                  stdout=PIPE,
                  stderr=PIPE)
        output, msg = p.communicate()
        return True
        
class UpdateLikeAndComment:
    def cmd(self):
        return [
            '/home/ubuntu/myproject/bin/python',
            '{script_path}/update_like_comment.py',
        ]

    def send(self):
        p = Popen(self.cmd(),
                  stdin=PIPE,
                  stdout=PIPE,
                  stderr=PIPE)
        output,msg = p.communicate()
        return True
