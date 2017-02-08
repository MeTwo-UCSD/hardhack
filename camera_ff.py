"""
use ffmepg to take care of video and audio input
encode as it runs

require python > 3.3
by defualt, ffmpeg runs under live folder.
"""

from __future__ import print_function
import subprocess
import sys
import os
import shutil
import platform
import json
from shlex import split
from time import sleep

class Camera:
    """
    capture video through ffmepg command line
    """


    def __init__(self):
        # require python > 3.3
        try:
            assert sys.version_info >= (3, 3)
        except AssertionError:
            raise AssertionError("Require Python > 3.3")

        # include ffmpeg or fall back to avconv
        os.environ["PATH"] += os.pathsep + os.path.abspath('./bin')
        self.ffmpeg_path = shutil.which('ffmpeg')

        if self.ffmpeg_path is None:
            self.ffmpeg_path = shutil.which('avconv')
            if self.ffmpeg_path is None:
                print("cannot find excutable")
                sys.exit(1)

        # input module based on system
        if platform.system() == 'Windows':
            self._system = 'Windows'
        elif platform.system() == 'Linux':
            self._system = 'Linux'
        else:
            raise AssertionError("Not Supported platform")

        with open('command.json') as file:
            self._command = json.load(file)

    def run(self):
        # ffmpeg -list_devices true -f dshow -i dummy
        # ffmpeg -f dshow -list_options true -i video="Integrated Camera"
        # ffmpeg -f dshow -video_size 1920x1080 -framerate 30 -pixel_format
        # video4linux2
        os.makedirs('./live', exist_ok=True)
        self._generate_live()
        self._generate_mpd()
        if self._process.poll() is not None:
            raise ChildProcessError("cannot open process")

    def _generate_live(self):
        """
        todo: add configuration and device selection
        """
        live_command = [self.ffmpeg_path, '-y']

        live_command.extend(split(self._command[self._system]['input_video']))
        live_command.extend(split(self._command['generate_live']))

        self._process = subprocess.Popen(live_command, stdin=subprocess.PIPE, cwd='./live')

    def _generate_mpd(self):
        mpd_command = [self.ffmpeg_path]

        mpd_command.extend(split(self._command['generate_mpd']))

        subprocess.Popen(mpd_command, cwd='./live')

    def terminate(self, timeout=5):
        """
        end current process
        """
        self._process.terminate()
        sleep(timeout)
        if self._process.poll() is None:
            self._process.kill()
        sleep(timeout)
        if self._process.poll() is None:
            raise TimeoutError('Cannot kill subprocess')


if __name__ == "__main__":
    from threading import Thread
    test_cam = Camera()
    t = Thread(target=test_cam.run, daemon=True)
    t.start()
    sleep(60)
    test_cam.terminate()
