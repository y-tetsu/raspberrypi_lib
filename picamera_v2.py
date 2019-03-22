#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Control of PiCamera V2
"""

import time
import picamera


class PiCameraV2():
    """
    capture photo and record video
    """
    def __init__(self):
        self.camera = None
        self.setup()

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.cleanup()

    def setup(self):
        """
        camera setup
        """
        try:
            self.camera = picamera.PiCamera()
            self.camera.hflip = True  # horizontal flip
            self.camera.vflip = True  # vertical flip

        except:
            self.cleanup()

    def cleanup(self):
        """
        camera cleanup
        """
        if self.camera:
            self.camera.close()
            self.camera = None

    def capture_photo(self, width, height, filename):
        """
        capture photo
        """
        self.camera.resolution = width, height  # size
        self.camera.capture(filename)           # capture photo

    def start_video(self, width, height, filename):
        """
        start video recording
        """
        self.camera.resolution = width, height  # size
        self.camera.start_recording(filename)   # start video recording
        time.sleep(1)                           # wait for startup camera

    def stop_video(self):
        """
        stop video recording
        """
        if self.camera:
            time.sleep(1)
            self.camera.stop_recording()


if __name__ == '__main__':
    with PiCameraV2() as c:
        c.capture_photo(720, 960, './photo1.jpg')
        c.start_video(240, 320, './video1.h264')
        time.sleep(5)
        c.stop_video()

        c.capture_photo(720, 960, './photo2.jpg')
        c.start_video(240, 320, './video2.h264')
        time.sleep(5)
        c.stop_video()
