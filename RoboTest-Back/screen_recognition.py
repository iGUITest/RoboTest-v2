"""
Used for screen recognition of the device under test
"""
import cv2


def PhoneDet(img_path, image, info=[0, 0, 0, 0]):
    # cv2.namedWindow('Phone Detection', cv2.WINDOW_NORMAL)
    imgContour = image.copy()

    # TODO
    if info != [0, 0, 0, 0]:
        x = info[0]
        y = info[1]
        w = info[2]
        h = info[3]
        jietu_image = imgContour[y:y + h, x:x + w]
        cv2.imwrite(img_path, jietu_image)
        return info

    imgGray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 5, 50)
    img, contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    phone_contour = imgContour
    cv2.imwrite(img_path, phone_contour)

    final_x = 0
    final_y = 0
    final_w = 0
    final_h = 0
    final_area = 0

    for obj in contours:
        obj = cv2.convexHull(obj)
        perimeter = cv2.arcLength(obj, True)
        approx = cv2.approxPolyDP(obj, 0.01 * perimeter, True)
        x, y, w, h = cv2.boundingRect(approx)
        if w < 0.2 * h or w > 5 * h:
            continue
        area = cv2.contourArea(obj)
        if area < 42000 or area > 4200000:
            continue
        print('PhoneDet', y, y+h, x, x+w)
        if w < final_w and h < final_h:
            continue
        if w * h > final_area:
            jietu_image = imgContour[y:y+h, x:x+w]
            cv2.imwrite(img_path, jietu_image)
            final_area = w * h
        # cv2.rectangle(imgContour, (x, y), (x + w, y + h), color, 10)
        phone_contour = obj
        final_x = x
        final_y = y
        final_w = w
        final_h = h

    # cv2.imshow("Original img", image)
    # cv2.imshow("Phone Detection", imgContour)
    # cv2.waitKey(0)

    return [final_x, final_y, final_w, final_h]


# PhoneDet(r'D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\image\1.jpg', [20, 115, 578, 270])
# PhoneDet(r'D:\iSE\2022_Summer\AutoArm\RoboTest\opensource_code\image\1.jpg')
