import pyautogui
import cv2
import numpy as np
from datetime import datetime;


def capture_screen(save=False):
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    if save:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cv2.imwrite(f"data/screenshot_{timestamp}.png", frame)

    return frame

def shoe_screen(frame):
    cv2.imshow("Captured Screen", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()