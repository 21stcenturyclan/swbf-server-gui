import subprocess


class Runner:
    def __init__(self):
        self._processes = []

    def add_process(self, exe, options):
        self._processes.append(subprocess.Popen(exe + ' ' + options))

    def stop_process(self):
        if len(self._processes):
            self._processes[0].kill()
