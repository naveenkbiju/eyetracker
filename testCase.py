import unittest
import cv2
class TestStringMethods(unittest.TestCase):

    def test_isCameraOn(self):
        video = cv2.VideoCapture(0)
        check , v = video.read()
        self.assertTrue(check)
if __name__ == '__main__':
    unittest.main()