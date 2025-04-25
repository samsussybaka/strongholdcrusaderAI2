# perception/minimap.py

import cv2

# Define minimap region (you may need to adjust these values)
# Format: (left, top, width, height)
MINIMAP_REGION = (1700, 850, 200, 200)  # Example: bottom right corner

def extract_minimap(frame):
    x, y, w, h = MINIMAP_REGION
    minimap = frame[y:y+h, x:x+w]
    return minimap

def show_minimap(minimap):
    cv2.imshow("Minimap", minimap)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
