from perception.screen_capture import capture_screen, shoe_screen
from perception.minimap import extract_minimap, show_minimap

if __name__ == "__main__":
    frame = capture_screen(save=True)

    minimap = extract_minimap(frame)
    shoe_screen(frame)