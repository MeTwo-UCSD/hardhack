"""
use ffmepg to take care of video and audio input
encode as it runs

require python > 3.3
"""

from __future__ import print_function
import subprocess
import sys
import os
import shutil
import platform
import shlex


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
        self.bin_path = shutil.which('ffmpeg')

        if self.bin_path is None:
            self.bin_path = shutil.which('avconv')
            if self.bin_path is None:
                print("cannot find excutable")
                sys.exit(1)

        # input module based on system
        self._command = [self.bin_path, '-y']
        # if platform.system() == 'Windows':
        #    self._command.extend(['-f', 'dshow'])

    def run(self):
        # ffmpeg -list_devices true -f dshow -i dummy
        # ffmpeg -f dshow -list_options true -i video="Integrated Camera"
        # ffmpeg -f dshow -video_size 1920x1080 -framerate 30 -pixel_format
        # video4linux2
        """
        todo: add configuration and device selection
        """

        VP9_LIVE_PARAMS = shlex.split(
            "-speed 6 -tile-columns 4 -frame-parallel 1 -threads 8 -static-thresh 0 -max-intra-rate 300 -deadline realtime -lag-in-frames 0 -error-resilient 1")

        # input video device
        self._command.extend(['-f', 'dshow', '-vcodec', 'h264', '-video_size',
                              '1920x1080', '-framerate', '30', '-i', 'video=HD Pro Webcam C920'])
        # input audio device
        self._command.extend(['-f', 'dshow', '-sample_size', '16', '-sample_rate',
                              '44100', '-channels', '1', '-i', 'audio=Microphone (HD Pro Webcam C920)'])
        # map input
        self._command.extend(['-map', '0:0', '-pix_fmt', 'yuv420p',
                              '-c:v', 'libvpx-vp9', '-s', '1280x720', '-keyint_min', '60', '-g', '60', '-b:v', '3000k'])

        self._command.extend(VP9_LIVE_PARAMS)

        self._command.extend(['-f', 'webm_chunk', '-header', '/live/glass_360.hdr',
                              '-chunk_start_index', '1', '/live/glass_360_%d.chk'])

        # , '-map', '1:0'])
        # # output video & audio format
        # self._command.extend(['-vcodec', 'libx264'])
        # self._command.extend(['-acodec', 'aac', '-ab', '128k', '-ar', '44100'])
        # self._command.extend(
        #     ['-maxrate', '750k', '-bufsize', '4000k', 'out.mp4'])
        try:
            self._process = subprocess.Popen(
                self._command, stdin=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            out_bytes = e.output

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
    time.sleep(30)
    test_cam.terminate()
