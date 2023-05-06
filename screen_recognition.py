"""
用于对被测设备进行屏幕识别
"""
import cv2


def PhoneDet(img_path, info=[0, 0, 0, 0]):
    # cv2.namedWindow('Phone Detection', cv2.WINDOW_NORMAL)
    image = cv2.imread(img_path)
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

    imgGray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # 转灰度图
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # 高斯模糊
    imgCanny = cv2.Canny(imgBlur, 5, 50)  # Canny算子边缘检测
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
        perimeter = cv2.arcLength(obj, True)  # 计算轮廓周长
        approx = cv2.approxPolyDP(obj, 0.01 * perimeter, True)  # 获取轮廓角点坐标
        x, y, w, h = cv2.boundingRect(approx)  # 获取矩形左上角坐标值和宽度、高度
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
        # cv2.rectangle(imgContour, (x, y), (x + w, y + h), color, 10)  # 绘制边界框
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
