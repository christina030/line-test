# -*- coding: utf-8 -*-

# 種子

import pickle
import os
import datetime
from datetime import datetime as dt
import cv2
from linebot.models import TextSendMessage, ImageSendMessage    # 載入 TextSendMessage 和 ImageSendMessage 模組

from imgur import glucose_graph
from rep import modify_val, read_data


grow_days = [5, 10, 20, 30]
mood_ranges = [[8, 16], [10, 20], [20, 40], [20, 40]]

def handle_grow(tk, userID, line_bot_api, folder):#, user_filename='users.pkl', mood_filename='mood_scores.pkl'):
    user_date = read_data('users', 'first_date', userID)
    print('"""\nusers date:')
    print(user_date)
    print(type(user_date))
    print('"""')
    mood_scores = read_data('scores', 'score1, score2, score3, score4, score5', userID)
    print('"""\nscores:')
    print(mood_scores)
    print(type(mood_scores))
    print('"""')
    # users = None
    # mood_scores = None
    # with open(os.path.join(folder, user_filename), 'rb') as f:
    #     users = pickle.load(f)
    # with open(os.path.join(folder, mood_filename), 'rb') as f:
    #     mood_scores = pickle.load(f)

    today = datetime.date.today()
    # days = (today - users[userID]).days
    days = (today - user_date[0]).days
    # days = (today - dt.strptime(user_date[0], '%Y-%m-%d')).days

    if days in grow_days:
        # mood_scores[userID].append(0)

        # with open(os.path.join(folder, mood_filename), 'wb') as f:
        #     pickle.dump(mood_scores, f)
        modify_val('scores', [f'score{len(mood_scores)+1}'], [0], userID)

    print(f'""" 第{days}天 """', userID)
    ############################################################
    img_url = grow_plant(tk, mood_scores[userID], folder)   # 取得對應的圖片，如果沒有取得，會是 False
    print(img_url)
    if img_url:
        # 如果有圖片網址，回傳圖片
        img_message = ImageSendMessage(original_content_url=img_url[0], preview_image_url=img_url[0])
        line_bot_api.reply_message(tk, img_message)
        os.system(f'rm {img_url[1]}')
    else:
        # 如果是 False，回傳文字
        text_message = TextSendMessage(text='找不到相關植栽圖片')
        line_bot_api.reply_message(tk, text_message)
    ############################################################


def grow_plant(tk, mood_score, folder):
    img = [
        'plant1.png',
        ['plant2.png',
         'plant3.png',
         'plant4.png',
         'plant5.png'],
        ['plant2_2.png',
         'plant2_3.png',
         'plant2_4.png',
         'plant2_5.png'],
        ['plant3_2.png',
         'plant3_3.png',
         'plant3_4.png',
         'plant3_5.png']
    ]

    img = cv2.imread(os.path.join('shared', img[0]), cv2.IMREAD_UNCHANGED)

    for i, mood in enumerate(mood_score[:-1]):
        if mood < mood_ranges[i][0]:
            img2 = cv2.imread(os.path.join('shared', img[1][i]), cv2.IMREAD_UNCHANGED)
        elif mood < mood_ranges[i][1]:
            img2 = cv2.imread(os.path.join('shared', img[2][i]), cv2.IMREAD_UNCHANGED)
        else:
            img2 = cv2.imread(os.path.join('shared', img[3][i]), cv2.IMREAD_UNCHANGED)

        # img[img2 != [0, 0, 0]] = img2[img2 != [0, 0, 0]]
        img = img * (1 - img2[:, :, -1]) + img2 * img2[:, :, -1]

    imgSavePath = os.path.join('shared', tk + '_plant.jpg')
    cv2.imwrite(imgSavePath, img)

    img_url = glucose_graph(client_id, imgSavePath)

    if img:
      return (img_url, imgSavePath)
    else:
      # 如果找不到對應的圖片，回傳 False
      return False
