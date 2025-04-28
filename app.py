import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Set the Tesseract path (update this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.title("Stronghold 2 Strat")
st.write("upload a game screenshot to get started")

uploaded_file = st.file_uploader("choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.subheader("Red Circle Detection")

    image = Image.open(uploaded_file)
    st.image(image, caption="uploaded image", use_container_width=True)

    # Convert the image to a numpy array
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Define bottom left region (adjust these values based on your screen)
    height, width = image_cv.shape[:2]
    bottom_left = image_cv[int(height*0.7):height, 0:int(width*0.3)]
    
    # Convert to HSV for better color detection
    image_hsv = cv2.cvtColor(bottom_left, cv2.COLOR_BGR2HSV)
    
    # Red color range
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Create masks
    mask_red1 = cv2.inRange(image_hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(image_hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(mask_red, (5, 5), 0)
    
    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 20,
                             param1=50, param2=30, minRadius=5, maxRadius=50)

    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw the outer circle
            cv2.circle(bottom_left, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw the center of the circle
            cv2.circle(bottom_left, (i[0], i[1]), 2, (0, 0, 255), 3)

    # Show result
    st.image(cv2.cvtColor(bottom_left, cv2.COLOR_BGR2RGB), caption='Detected Red Circles', use_column_width=True)
    st.write(f"Number of circles detected: {len(circles[0]) if circles is not None else 0}")

    cv2.imwrite("detected_circles.jpg", bottom_left)
    st.success("image saved")

    st.subheader("Number Detection")

    # Define top right region (adjust these values based on your screen)
    top_right = image_cv[0:int(height*0.2), int(width*0.8):width]
    
    # Convert to grayscale
    gray = cv2.cvtColor(top_right, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to make text more visible
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Perform OCR on the thresholded image
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    numbers = pytesseract.image_to_string(thresh, config=custom_config)
    
    # Clean up the detected numbers
    numbers = ''.join(filter(str.isdigit, numbers))
    
    # Show the processed region and detected numbers
    st.image(cv2.cvtColor(top_right, cv2.COLOR_BGR2RGB), caption='Top Right Region', use_column_width=True)
    st.image(thresh, caption='Processed for OCR', use_column_width=True)
    st.write(f"Detected Numbers: {numbers}")

    cv2.imwrite("top_right_numbers.jpg", top_right)
    st.success("image saved")
    
