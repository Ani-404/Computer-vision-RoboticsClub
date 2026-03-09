import cv2
import os

# image insertion
folder_path = r"C:\Projects\Computer-vision-RoboticsClub\data"

# Expected left-to-right colors for each test image.
expected = {
    "test1.jpeg": ["blue", "blue", "blue"],
    "test2.jpeg": ["red", "blue", "blue"],
    "test3.jpeg": ["red", "blue", "blue"],
    "test4.jpeg": ["blue", "red", "blue"],
    "test5.jpeg": ["blue", "red", "blue"],
    "test6.jpeg": ["red", "red", "red"],
    "test7.jpeg": ["blue", "blue", "red"],
    "test8.jpeg": ["red", "blue", "blue"],
    "test9.jpeg": ["red", "blue", "red"],
    "test10.jpeg": ["red", "red", "blue"],
    "test11.jpeg": ["blue", "red", "red"],
    "test12.jpeg": ["red", "blue", "blue"],
    "test13.jpeg": ["blue", "red", "blue"],
}

correct_cases = 0
wrong_cases = 0
skipped_cases = 0

for filename in sorted(os.listdir(folder_path)):
    file_path = os.path.join(folder_path, filename)
    img = cv2.imread(file_path)

    if img is None:
        print(f"{filename}: skipped (image read failed)")
        skipped_cases += 1
        continue

    img = cv2.resize(img, (500, 500))

    # making of the contour
    image_copy = img.copy()
    gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) < 4:
        print(f"{filename}: skipped (not enough contours)")
        skipped_cases += 1
        continue

    # finding centre points of the circles (contours)
    try:
        m1 = cv2.moments(contours[1])
        m2 = cv2.moments(contours[2])
        m3 = cv2.moments(contours[3])

        cx1 = int(m1["m10"] / m1["m00"])
        cx2 = int(m2["m10"] / m2["m00"])
        cx3 = int(m3["m10"] / m3["m00"])
        cy1 = int(m1["m01"] / m1["m00"])
        cy2 = int(m2["m01"] / m2["m00"])
        cy3 = int(m3["m01"] / m3["m00"])
    except ZeroDivisionError:
        print(f"{filename}: skipped (invalid contour moments)")
        skipped_cases += 1
        continue

    # ordering centre points left to right
    points = sorted([[cx1, cy1], [cx2, cy2], [cx3, cy3]], key=lambda k: k[0])
    cx1, cy1 = points[0]
    cx2, cy2 = points[1]
    cx3, cy3 = points[2]

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue_value1 = int(hsv_img[cy1, cx1][0])
    hue_value2 = int(hsv_img[cy2, cx2][0])
    hue_value3 = int(hsv_img[cy3, cx3][0])

    # assigning colors based on hue values
    if hue_value1 < 20:
        color1 = "red"
    elif 40 < hue_value1 < 140:
        color1 = "blue"
    else:
        color1 = "red"

    if hue_value2 < 20:
        color2 = "red"
    elif 40 < hue_value2 < 140:
        color2 = "blue"
    else:
        color2 = "red"

    if hue_value3 < 20:
        color3 = "red"
    elif 40 < hue_value3 < 140:
        color3 = "blue"
    else:
        color3 = "red"

    predicted = [color1, color2, color3]
    expected_colors = expected.get(filename)

    if expected_colors is None:
        result = "no-label"
        skipped_cases += 1
    elif predicted == expected_colors:
        result = "correct"
        correct_cases += 1
    else:
        result = "wrong"
        wrong_cases += 1

    print(f"{filename}: {predicted} -> {result}")

print("\nSummary")
print(f"Correct test cases: {correct_cases}")
print(f"Wrong test cases: {wrong_cases}")
print(f"Skipped test cases: {skipped_cases}")
