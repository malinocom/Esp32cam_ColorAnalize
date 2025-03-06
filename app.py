from flask import Flask, request, jsonify
import cv2
import numpy as np
import requests


app = Flask(__name__)

@app.route('/')
def home():
    return "amirammmm"

@app.route('/detect', methods=['POST'])
def detect_colors():
    esp32_url = "http://amirrez.liara.run/capture"


    response = requests.get(esp32_url)
    image_array = np.array(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)


    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])


    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])


    mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)


    mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)


    mask = cv2.bitwise_or(mask_red, mask_yellow)


    if np.any(mask):
        color_detected = "Red or Yellow detected"
    else:
        color_detected = "No Red or Yellow detected"


    return jsonify({"result": color_detected})


if __name__ == '__main__':
    app.run(debug=True)
