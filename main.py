import os

import numpy as np
import pandas as pd
import cv2
import pytesseract as pt


def showimg(t, img):
    cv2.imshow(t, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def image_ocr(cropped_image):
    kernel = np.ones((1, 1), np.uint8)
    # ret, cropped_image = cv2.threshold(cropped_image, 200, 255, cv2.THRESH_BINARY)
    # showimg('Threshold', cropped_image)
    dilate_cropped_image = cv2.dilate(cropped_image, kernel, iterations=10)
    # dilate_cropped_image = cv2.dilate(dilate_cropped_image, kernel, iterations=10)
    # cv2.imshow('cropped image', cropped_image)
    # cv2.imshow('dilate cropped image', dilate_cropped_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return pt.image_to_string(dilate_cropped_image)


img_path = './prod20000/transfer/'
raw_path = './prod20000/raw/'

files = sorted(os.listdir(img_path))
if '.DS_Store' in files:
    files.remove('.DS_Store')
title = ['PA_UIKey', 'ORS', 'QT', 'QTcBaz', 'PR', 'P', 'RR', 'PP', 'P', 'QRS', 'T', 'comment', 'bpm']
result = []
err = []

for file in files:

    info = [file.replace('.png', '')]
    print(f'\n\nImage: {file}')
    img = cv2.imread(img_path + file)
    # if debug:
    #     cv2.imshow('1 org image', img)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = gray_img.shape
    print(f'image height: {height}, width: {width}')
    # if debug:
    #     cv2.imshow('2 gray image', gray_img)

    # details part
    cropped_image = gray_img[100:int(height / 3) - 25, 195:365]
    content = image_ocr(cropped_image)
    content = content.replace('ms', '/').replace('i', '1').replace('A', '4').replace('~', '-').replace('.', '').replace(
        '|', '/')
    parts = content.split('/')
    for idx, part in enumerate(parts):
        parts[idx] = parts[idx].replace('\n', '').replace(' ', '').replace('\x0c', '').replace('degrees', '').replace('degree', '').replace('&6s','').replace(']', '1').replace('{', '')
    # print(parts)

    # comments part
    cropped_image = gray_img[100:int(height / 3) - 25, 365:int(width)]
    comment = image_ocr(cropped_image)
    comment = comment.strip()
    comment = comment.replace('$T', 'ST').replace('*#*', '***').replace('Ist', '1st').replace('\n\n', '\n')
    # print(comment)

    # heart rate part
    cropped_image = gray_img[0:60, int(width) - 150:int(width) - 80]
    # cv2.imshow('title', cropped_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    bpm = image_ocr(cropped_image)
    bpm = bpm.replace('\n\x0c', '')
    # print(bpm)

    # crop the raw image part
    cropped_image = gray_img[int(height / 3) - 22:height - 93, 58:int(width) - 52]
    cv2.imwrite(raw_path + info[0] + '_raw.png', cropped_image)

    info.extend(parts)
    info.append(comment)
    info.append(bpm)
    print(info)
    print(len(info))
    if (len(info) == 13):
        result.append(info)
    else:
        info.append(len(info))
        err.append(info)
#
df = pd.DataFrame(result, columns=title)
df.to_csv('out.csv', index=False, encoding='utf-8')

df_err = pd.DataFrame(err)
df_err.to_csv('err.csv', index=False, encoding='utf-8')
# with open('./prod300/errlist.txt', 'w') as f:
#     for i in err:
#         f.write(i)


# cv2.waitKey(0)
# cv2.destroyAllWindows()
