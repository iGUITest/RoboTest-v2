"""
Used to calculate image similarity
"""
import cv2
import numpy as np
from matplotlib import pyplot as plt


def extract_sift_feature(img):
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(img, None)
    return keypoints, descriptors


def show_img_sift_dot(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    keypoints, descriptors = extract_sift_feature(img)
    img1 = cv2.drawKeypoints(rgb_img, keypoints, img)
    plt.imshow(img1)
    plt.show()


def draw_match_image(img1, img2):
    rgb_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    keypoints1, descriptors1 = extract_sift_feature(img1)
    keypoints2, descriptors2 = extract_sift_feature(img2)

    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)

    img3 = cv2.drawMatches(rgb_img1, keypoints1, rgb_img2, keypoints2, matches[:50], rgb_img2, flags=2)
    plt.imshow(img3)
    plt.show()


def cal_SIFT_sim(img1, img2):
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    keypoints1, descriptors1 = extract_sift_feature(img1)
    keypoints2, descriptors2 = extract_sift_feature(img2)

    bf = cv2.BFMatcher()
    matches1 = bf.knnMatch(descriptors1, descriptors2, k=2)
    top_results1 = []
    for m, n in matches1:
        if m.distance < 0.7 * n.distance:
            top_results1.append(m)
    matches2 = bf.knnMatch(descriptors2, descriptors1, k=2)
    top_results2 = []
    for m, n in matches2:
        if m.distance < 0.7 * n.distance:
            top_results2.append(m)
    top_results = []
    for m1 in top_results1:
        m1_query_idx = m1.queryIdx
        m1_train_idx = m1.trainIdx

        for m2 in top_results2:
            m2_query_idx = m2.queryIdx
            m2_train_idx = m2.trainIdx

            if m1_query_idx == m2_train_idx and m1_train_idx == m2_query_idx:
                top_results.append(m1)

    image_sim = len(top_results) / min(len(keypoints1), len(keypoints2))
    return image_sim


def extract_SIFT_vector(img, vector_size):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints = sift.detect(gray_img, None)
    keypoints = sorted(keypoints, key=lambda x: -x.response)
    img_kps = keypoints[:vector_size]
    kps, des = sift.compute(gray_img, img_kps)
    vector = des.flatten()
    vector_len = vector_size * 128
    if vector.size < vector_len:
        vector = np.concatenate(vector, np.zeros(vector_len - vector.size))
    return vector


import scipy.spatial as T


def cal_similarity(img_path1, img_path2):
    print('img_path1:', img_path1)
    print('img_path2:', img_path2)
    vector_size = 100
    img1 = cv2.imread(img_path1)
    img2 = cv2.imread(img_path2)
    img1_vector = extract_SIFT_vector(img1, vector_size).reshape(-1, 128 * vector_size)
    img2_vector = extract_SIFT_vector(img2, vector_size).reshape(-1, 128 * vector_size)
    sim = T.distance.cdist(img1_vector, img2_vector, 'cosine')
    print(sim)
    return sim

# img1 = cv2.imread(r"D:\iSE\2022_Summer\AutoArm\RoboTest\image\test\picture1.jpg")
# img2 = cv2.imread(r"D:\iSE\2022_Summer\AutoArm\RoboTest\image\test\picture3.jpg")
# draw_match_image(img1, img2)
