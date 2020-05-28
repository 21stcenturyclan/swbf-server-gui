import os
import sys
import subprocess
from threading import Thread


class Runner:
    def __init__(self):
        self._processes = []

    def add_process(self, exe, options):
        print(exe, options, sep='')
        sys.stdout.flush()

        proc = subprocess.Popen(exe + ' ' + options)
        proc.communicate()

        # t = Thread(target=run, args=[exe], daemon=True)
        # t.run()


def run(exe):
    subprocess.call([exe])
