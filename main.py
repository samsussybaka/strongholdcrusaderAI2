from perception.screen_capture import capture_screen, show_screen
from perception.minimap import extract_minimap, show_minimap

if __name__ == "__main__":
    frame = capture_screen(save=True)

    minimap = extract_minimap(frame)
    show_screen(frame)
    show_minimap(minimap)