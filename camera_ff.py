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
import shlex
import json

class Camera:
    """
    capture video through ffmepg command line
    """


    def __init__(self):
        # require python > 3.3
        try:
            assert sys.version_info >= (3, 3)
        except AssertionError:
            print("Require Python > 3.3")

        # include ffmpeg or fall back to avconv
        os.environ["PATH"] += os.pathsep + os.path.abspath('./bin')
        self.ffmpeg_path = shutil.which('ffmpeg')

        if self.ffmpeg_path is None:
            self.ffmpeg_path = shutil.which('avconv')
            if self.ffmpeg_path is None:
                print("cannot find excutable")
                sys.exit(1)

        # input module based on system

        # if platform.system() == 'Windows':
        #    self._command.extend(['-f', 'dshow'])

        with open('command.json') as file:
            self._command = json.load(file)

    def run(self):
        # ffmpeg -list_devices true -f dshow -i dummy
        # ffmpeg -f dshow -list_options true -i video="Integrated Camera"
        # ffmpeg -f dshow -video_size 1920x1080 -framerate 30 -pixel_format
        # video4linux2
        self._generate_live()
        self._generate_mpd()


    def _generate_live(self):
        """
        todo: add configuration and device selection
        """
        live_command = [self.ffmpeg_path, '-y']

        live_command.extend(shlex.split(self._command['win']['input_video']))
        live_command.extend(shlex.split(self._command['generate_live']))

        self._process = subprocess.Popen(live_command, stdin=subprocess.PIPE, cwd='live')

    def _generate_mpd(self):
        mpd_command = [self.ffmpeg_path]

        mpd_command.extend(shlex.split(self._command['generate_mpd']))

        subprocess.Popen(mpd_command, cwd='live')


    def terminate(self):
        """
        end current process
        """
        self._process.communicate(b'q', timeout=5)


if __name__ == "__main__":
    from threading import Thread
    import time
    test_cam = Camera()
    t = Thread(target=test_cam.run, daemon=True)
    t.start()
    time.sleep(60)
    test_cam.terminate()
