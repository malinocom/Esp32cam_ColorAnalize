from flask import Flask, request
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/color_detection')
def color_detection():
    # دریافت تصویر از ESP32-CAM
    image_data = request.data
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

    # تبدیل تصویر به فضای رنگ HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # تعریف محدوده رنگ زرد
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # تعریف محدوده رنگ سبز
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # ترکیب ماسک‌ها
    mask = cv2.bitwise_or(mask_yellow, mask_green)

    # بررسی وجود رنگ‌ها
    yellow_detected = np.any(mask_yellow)
    green_detected = np.any(mask_green)

    if yellow_detected and green_detected:
        return "Both Yellow and Green detected"
    elif yellow_detected:
        return "Yellow detected"
    elif green_detected:
        return "Green detected"
    else:
        return "No color detected"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # آدرس IP و پورت سرور
