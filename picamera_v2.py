#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Control of PiCamera V2
"""

import time
import threading
import picamera
import picamera.array
import cv2

VIDEO_WAIT = 1
STREAMING_WAIT = 1

class PiCameraV2():
    """
    capture photo, record video, and streaming for cv2
    """
    def __init__(self):
        self.camera = None
        self.array = None
        self.stream = None
        self.frame = None
        self.stop = None
        self.stream_thread = None
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
        if self.stream_thread:
            self.stop = True
            self.stream_thread.join()
            self.stream_thread = None

        if self.stop:
            self.stop = None

        if self.stream:
            self.stream.close()
            self.stream = None

        if self.array:
            self.array.close()
            self.array = None
            self.frame = None

        if self.camera:
            self.camera.close()
            self.camera = None

    def capture_photo(self, width, height, filename):
        """
        capture photo
        """
        self.camera.resolution = (width, height)  # size
        self.camera.capture(filename)             # capture photo

    def start_video(self, width, height, filename):
        """
        start video recording
        """
        self.camera.resolution = (width, height)  # size
        self.camera.start_recording(filename)     # start video recording
        time.sleep(VIDEO_WAIT)                    # wait for startup camera

    def stop_video(self):
        """
        stop video recording
        """
        if self.camera:
            time.sleep(VIDEO_WAIT)
            self.camera.stop_recording()

    def start_streaming(self, width, height):
        """
        start streaming
        """
        self.camera.resolution = (width, height)
        self.array = picamera.array.PiRGBArray(self.camera)
        self.stream = self.camera.capture_continuous(self.array, format="bgr", use_video_port=True)
        self.stop = False
        self.frame = None

        self.stream_thread = threading.Thread(target=self.update_streaming, args=())
        self.stream_thread.start()

        time.sleep(STREAMING_WAIT)

    def update_streaming(self):
        """
        update streaming
        """
        for frame in self.stream:
            self.frame = frame.array
            self.array.truncate(0)

            if self.stop:
                self.stream.close()
                self.array.close()

                return

    def stop_streaming(self):
        """
        stop streaming
        """
        self.stop = True


if __name__ == '__main__':
    with PiCameraV2() as c:
        print('photo1 start.')
        c.capture_photo(720, 960, './photo1.jpg')

        print('video1 start.')
        c.start_video(240, 320, './video1.h264')
        time.sleep(3)
        c.stop_video()

        print('photo2 start.')
        c.capture_photo(720, 960, './photo2.jpg')

        print('video2 start.')
        c.start_video(240, 320, './video2.h264')
        time.sleep(3)
        c.stop_video()

        print('streaming start. ESC key for quit.')
        c.start_streaming(640, 480)

        try:
            cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)

            while True:
                frame = c.frame
                cv2.imshow('Frame', frame)
                key = cv2.waitKey(1) & 0xFF

                if key == 27:
                    break

        finally:
            cv2.destroyAllWindows()
