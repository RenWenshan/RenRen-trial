import urllib, threading
from Queue import Queue

class FileGetter(threading.thread):

    def __init__(self, url):
        self.url = url
        self.result = None
        threading.Thread.__init__(self)

    def get_result(self):
        return self.result

    def run(self):
        try:
            f = urllib.urlopen(url)
            contents = f.read()
            f.close()
            self.result = contents
        except IOError:
            print 'can not'

def get_files(files):
    def producer(q, files):
        for file in files:
            thread = FileGetter(file)
