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

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.cleanup()

    def capture_photo(self, width, height, filename):
        """
        capture photo
        """
        with picamera.PiCamera() as camera:
            camera.resolution = width, height  # size
            camera.hflip = True                # horizontal flip
            camera.vflip = True                # vertical flip

            time.sleep(1)                      # wait for startup camera
            camera.capture(filename)           # capture photo

    def start_video(self, width, height, filename):
        """
        start video recording
        """
        try:
            self.camera = picamera.PiCamera()

            self.camera.resolution = width, height  # size
            self.camera.hflip = True                # horizontal flip
            self.camera.vflip = True                # vertical flip

            time.sleep(1)                           # wait for startup camera
            self.camera.start_recording(filename)   # start video recording

        except:
            self.camera.close()
            self.camera = None

    def stop_video(self):
        """
        stop video recording
        """
        self.camera.stop_recording()
        self.camera.close()
        self.camera = None

    def cleanup(self):
        """
        camera cleanup
        """
        if self.camera:
            self.camera.close()


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
