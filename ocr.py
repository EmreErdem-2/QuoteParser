import cv2
import pytesseract
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
import sys
from front import ImageApp

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Apply thresholding to get a binary image
    _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Remove horizontal lines (underlines)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    detected_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(binary_image, [c], -1, (0, 0, 0), 2)
    
    # Invert the image back
    processed_image = cv2.bitwise_not(binary_image)
    
    return processed_image

def perform_ocr(image_path):
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image)
    return text

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ImageApp()
    ex.show()
    
    # Assuming the image is saved as 'displayed_image.png'
    image_path = 'displayed_image.png'
    pixmap = ex.drop_label.pixmap()
    pixmap.save(image_path)
    
    ocr_text = perform_ocr(image_path)
    print("OCR Result:")
    print(ocr_text)
    
    sys.exit(app.exec_())