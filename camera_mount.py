#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Control of Camera Mount using PiCamera V2 and two SG90(for pan and tilt)
"""

import time
import math

STEP_WAIT = 0.005
SWING_INTERVAL = 0.5


class CameraMount():
    """
    Control of Camera Mount
     --------------------------------------------
     camera : Camera Object
     servop : Servo Object for pan
     servot : Servo Object for tilt
     --------------------------------------------
    """
    def __init__(self, camera, servop, servot):
        self.camera = camera
        self.servop = servop
        self.servot = servot

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.cleanup()

    def cleanup(self):
        """
        cleanup Camera Mount
        """
        if self.camera:
            self.camera = None

        if self.servop:
            self.servop = None

        if self.servot:
            self.servot = None

    def start_video(self, width, height, filename):
        """
        start video recording
        """
        self.camera.start_video(width, height, filename)

    def stop_video(self):
        """
        stop video recording
        """
        self.camera.stop_video()

    def center(self):
        """
        set camera in center
        """
        self.servop.center()
        self.servot.center()

    def position(self, x_angle, y_angle):
        """
        set camera at x,y position
        """
        self.servop.move(-x_angle)
        self.servot.move(-y_angle)

    def video_pan(self, width, height, filename):
        """
        recording video while panning
        """
        self.center()
        self.start_video(width, height, filename)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servop, self.servot, self.servop.center_angle, self.servop.max_angle)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servop, self.servot, self.servop.max_angle, self.servop.min_angle, -1)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servop, self.servot, self.servop.min_angle, self.servop.center_angle)
        time.sleep(SWING_INTERVAL)
        self.stop_video()

    def video_tilt(self, width, height, filename):
        """
        recording video while tilting
        """
        self.center()
        self.start_video(width, height, filename)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servot, self.servop, self.servot.center_angle, self.servot.min_angle, -1)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servot, self.servop, self.servot.min_angle, self.servot.max_angle)
        time.sleep(SWING_INTERVAL)
        self.rotate(self.servot, self.servop, self.servot.max_angle, self.servot.center_angle, -1)
        time.sleep(SWING_INTERVAL)
        self.stop_video()

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
    from picamera_v2 import PiCameraV2
    from sg90 import SG90, SG90HW

    with PiCameraV2() as c, SG90HW(18) as sp, SG90HW(19) as st:
        with CameraMount(c, sp, st) as cm:
            cm.video_pan(240, 320, './video_pan.h264')
            cm.video_tilt(240, 320, './video_tilt.h264')

            cm.center()
            cm.start_video(240, 320, './video_clockwize.h264')

            for degree in range(360*2, 0, -1):
                x = math.cos(math.radians(degree)) * 80
                y = math.sin(math.radians(degree)) * 80
                cm.position(x, y)
                time.sleep(STEP_WAIT * 2)

            cm.center()
            cm.stop_video()
