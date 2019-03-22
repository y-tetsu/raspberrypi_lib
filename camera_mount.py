#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Control of Camera Mount using PiCamera V2 and two SG90(for pan and tilt)
"""

import time
from picamera_v2 import PiCameraV2
from sg90 import SG90, SG90HW

STEP_WAIT = 0.005
SWING_INTERVAL = 0.5


class CameraMount():
    """
    Control of Camera Mount
     --------------------------------------------
     gpiop : GPIO-PIN for pan
     gpiot : GPIO-PIN for tilt
     hwp   : True if using Hardware-PWM for gpiop
     hwt   : True if using Hardware-PWM for gpiot
     --------------------------------------------
    """
    def __init__(self, gpiop=18, gpiot=19, hwp=True, hwt=True):
        self.gpiop = gpiop
        self.gpiot = gpiot
        self.hwp = hwp
        self.hwt = hwt
        self.camera = None
        self.servop = None
        self.servot = None
        self.setup()

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.cleanup()

    def setup(self):
        """
        setup Camera Mount
        """
        try:
            self.camera = PiCameraV2()

            if self.hwp:
                self.servop = SG90HW(self.gpiop)
            else:
                self.servop = SG90(self.gpiop)

            if self.hwt:
                self.servot = SG90HW(self.gpiot)
            else:
                self.servot = SG90(self.gpiot)

        except:
            self.cleanup()

    def cleanup(self):
        """
        cleanup Camera Mount
        """
        if self.camera:
            self.camera.cleanup()
            self.camera = None

        if self.servop:
            self.servop.cleanup()
            self.servop = None

        if self.servot:
            self.servot.cleanup()
            self.servot = None

    def video_pan(self, width, height, filename):
        """
        recording video while panning
        """
        # set camera in center
        self.servop.center()
        self.servot.center()

        # start video recording
        self.camera.start_video(width, height, filename)

        # pan camera
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servop, self.servot, self.servop.center_angle, self.servop.max_angle)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servop, self.servot, self.servop.max_angle, self.servop.min_angle, -1)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servop, self.servot, self.servop.min_angle, self.servop.center_angle)
        time.sleep(SWING_INTERVAL)

        # stop video recording
        self.camera.stop_video()

    def video_tilt(self, width, height, filename):
        """
        recording video while tilting
        """
        # set camera in center
        self.servop.center()
        self.servot.center()

        # start video recording
        self.camera.start_video(width, height, filename)

        # tilt camera
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servot, self.servop, self.servot.center_angle, self.servot.min_angle, -1)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servot, self.servop, self.servot.min_angle, self.servot.max_angle)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servot, self.servop, self.servot.max_angle, self.servot.center_angle, -1)
        time.sleep(SWING_INTERVAL)

        # stop video recording
        self.camera.stop_video()

    def rotate(self, servo1, servo2, src_angle, dst_angle, step=1):
        """
        rotate servo1 and fix servo2
        """
        resolution = servo1.resolution
        fix_angle = servo2.center_angle

        start = int(src_angle / resolution)
        end = int(dst_angle / resolution) + 1

        for angle in range(start, end, step):
            servo1.move(angle * resolution)
            servo2.move(fix_angle)
            time.sleep(STEP_WAIT)


if __name__ == '__main__':
    with CameraMount() as camera:
        camera.video_pan(240, 320, './video_pan.h264')
        camera.video_tilt(240, 320, './video_tilt.h264')
