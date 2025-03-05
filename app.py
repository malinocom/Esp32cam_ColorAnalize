import cv2
import numpy as np
import requests


# آدرس IP ESP32-CAM
url = "http://<ESP32_IP>/capture" # آدرس IP خود را وارد کنید


# دریافت تصویر از ESP32-CAM
response = requests.get(url)
image_array = np.array(bytearray(response.content), dtype=np.uint8)
image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)


# تبدیل تصویر به فضای رنگ HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


# تعریف محدوده رنگ قرمز
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([180, 255, 255])


# تعریف محدوده رنگ زرد
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])


# ایجاد ماسک برای رنگ قرمز
mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
mask_red = cv2.bitwise_or(mask_red1, mask_red2)


# ایجاد ماسک برای رنگ زرد
mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)


# ترکیب ماسک‌ها
mask = cv2.bitwise_or(mask_red, mask_yellow)


# بررسی وجود رنگ‌ها
if np.any(mask):
    color_detected = "Red or Yellow detected"
else:
    color_detected = "No Red or Yellow detected"


# ارسال نتیجه به ESP32-CAM
response = requests.post("http://<ESP32_IP>/result", json={"result": color_detected})


# نمایش نتیجه در کنسول (اختیاری)
print(color_detected)