# -*- coding: utf-8 -*-

# 種子

import pickle
import os
import datetime
from datetime import datetime as dt
import cv2
import numpy as np
from linebot.models import TextSendMessage, ImageSendMessage    # 載入 TextSendMessage 和 ImageSendMessage 模組

from imgur import glucose_graph
from rep import modify_val, read_data


grow_days = [5, 10, 20]#, 30]
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
        modify_val('scores', [f'score{mood_scores.index(None)+1}'], [0], userID)

    print(f'""" 第{days}天 """', userID)
    ############################################################
    img_url = grow_plant(tk, mood_scores, folder)   # 取得對應的圖片，如果沒有取得，會是 False
    print(img_url)
    if img_url:
        # 如果有圖片網址，回傳圖片
        img_message = ImageSendMessage(original_content_url=img_url[0], preview_image_url=img_url[0])
        line_bot_api.reply_message(tk, img_message)
        os.system(f'rm {img_url[1]}')

        # first_time = read_data('users', 'first_time', userID)
        # if first_time:
        #     text_message = TextSendMessage(text='月亮種子的成長，需要我們細緻的照料。\n充足的水分的第一步，讓我們來幫種子澆水吧！\n每天都可以來找我一起澆水，我最擅長澆水了，畢竟我是小雲朵嘛～')
        #     line_bot_api.reply_message(tk, text_message)
            
    else:
        # 如果是 False，回傳文字
        text_message = TextSendMessage(text='找不到相關植栽圖片')
        line_bot_api.reply_message(tk, text_message)
    ############################################################


def grow_plant(tk, mood_score, folder):
    img_name = [
        '0.png',
        ['1-1.png',
         '2-1.png',
         '3-1.png',
         '4-1.png'],
        ['1-2.png',
         '2-2.png',
         '3-2.png',
         '4-2.png'],
        ['1-3.png',
         '2-3.png',
         '3-3.png',
         '4-3.png']
    ]
    
    img = cv2.imread(os.path.join(folder, img_name[0]), cv2.IMREAD_UNCHANGED)

    for i, mood in enumerate(mood_score[:mood_score.index(None)-1]):
        ############################################################
        # img2 = cv2.imread(os.path.join(folder, img_name[1][i]), cv2.IMREAD_UNCHANGED)
        # if mood is None:
        #     break
        if mood < mood_ranges[i][0]:
            img2 = cv2.imread(os.path.join(folder, img_name[1][i]), cv2.IMREAD_UNCHANGED)
        elif mood < mood_ranges[i][1]:
            img2 = cv2.imread(os.path.join(folder, img_name[2][i]), cv2.IMREAD_UNCHANGED)
        else:
            img2 = cv2.imread(os.path.join(folder, img_name[3][i]), cv2.IMREAD_UNCHANGED)
        ############################################################

        # img[img2 != [0, 0, 0]] = img2[img2 != [0, 0, 0]]
        alpha = np.transpose(np.tile(img2[:, :, -1], (3, 1, 1)), (1, 2, 0)) / 255.
        img[:, :, :-1] = img[:, :, :-1] * (1 - alpha) + img2[:, :, :-1] * alpha

    imgSavePath = os.path.join(folder, tk + '_plant.jpg')
    cv2.imwrite(imgSavePath, img)

    img_url = glucose_graph(imgSavePath)

    if img is not None:
      return (img_url, imgSavePath)
    else:
      # 如果找不到對應的圖片，回傳 False
      return False
