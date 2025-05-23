"""
Used for control identification and extraction of screenshots
"""
import time
import cv2


def extract_widgets(image, color=(0, 0, 255)):
    # cv2.namedWindow('shape Detection', cv2.WINDOW_NORMAL)
    imgContour = image.copy()
    checkContour = image.copy()

    imgGray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 5, 50)
    img_, contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    contours_list = []

    rectangle_list = []

    for obj in contours:
        obj = cv2.convexHull(obj)
        perimeter = cv2.arcLength(obj, True)
        approx = cv2.approxPolyDP(obj, 0.01 * perimeter, True)
        x, y, w, h = cv2.boundingRect(approx)
        if w < 0.5 * h or w > 1.5 * h:
            continue

        flag = False
        for rectangle in rectangle_list:
            x_target = rectangle[0]
            y_target = rectangle[1]
            w_target = rectangle[2]
            h_target = rectangle[3]
            if x >= x_target and x + w <= x_target + w_target and y >= y_target and y + h <= y_target + h_target:
                flag = True
            if x_target >= x and x_target + w_target <= x + w and y_target >= y and y_target + h_target <= y + h:
                rectangle_list.remove(rectangle)
        if flag:
            # print('!!!!!!!!!!!!!!!!!!')
            continue
        rectangle_list.append([x, y, w, h])
        # print(rectangle_list)

        # area = cv2.contourArea(obj)
        # if area < 20000 or area > 420000:
        #     continue
        contours_list.append(obj)
        # cv2.rectangle(imgContour, (x, y), (x + w, y + h), color, 2)
        # print("area: ", area)

    clean_rectangle_list = []
    exclude_index = []
    for i in range(len(rectangle_list)):
        for j in range(i + 1, len(rectangle_list)):
            if rectangle_list[i][0] < rectangle_list[j][0] \
                and rectangle_list[i][0] + rectangle_list[i][2] > rectangle_list[j][0] + rectangle_list[j][2] \
                    and rectangle_list[i][1] < rectangle_list[j][1] and rectangle_list[i][1] + rectangle_list[i][3] > rectangle_list[j][1] + rectangle_list[j][3]:
                if j not in exclude_index:
                    exclude_index.append(j)
            if rectangle_list[i][0] > rectangle_list[j][0] \
                and rectangle_list[i][0] + rectangle_list[i][2] < rectangle_list[j][0] + rectangle_list[j][2] \
                    and rectangle_list[i][1] > rectangle_list[j][1] and rectangle_list[i][1] + rectangle_list[i][3] < rectangle_list[j][1] + rectangle_list[j][3]:
                exclude_index.append(i)
    for i in range(len(rectangle_list)):
        if i not in exclude_index:
            clean_rectangle_list.append(rectangle_list[i])
    rectangle_list = clean_rectangle_list

    for rectangle in rectangle_list:
        if rectangle[2] < 10 or rectangle[3] < 10 or rectangle[2] > 100 or rectangle[3] > 100:
            continue
        checkContour = cv2.rectangle(checkContour, (rectangle[0], rectangle[1]), (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3]), color, 2)

    # cv2.imshow("Original img", image)
    # cv2.imshow("shape Detection", imgContour)
    # cv2.waitKey(0)

    timeStamp = int(time.time())
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d-%H-%M-%S", timeArray)
    temp_widget_extraction_res_path = 'D:\\iSE\\2022_Summer\\AutoArm\\RoboTest\\opensource_code\\image\\temp\\' + otherStyleTime + '.jpg'
    cv2.imwrite(temp_widget_extraction_res_path, checkContour)
    return rectangle_list
