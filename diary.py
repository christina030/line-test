# -*- coding: utf-8 -*-

from linebot.models import TextSendMessage, ImageSendMessage    # 載入 TextSendMessage 和 ImageSendMessage 模組
import os
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import datetime

from imgur import glucose_graph
from rep import modify_val, read_data


# 回覆圖片或影片訊息
# 建立回覆圖片的函式
def reply_img(tk, text, mood, folder, fontsize=72, color=(255,255,255), margin=20, linewidth=5, fontPath='used/CHENYULUOYAN-THIN-MONOSPACED.TTF'):
    # 文字對應圖片網址的字典
    img = [
        'img1.jpg',
        'img2.jpg',
        'img3.jpg',
        'img4.jpg',
        'img5.jpg',
        'img6.jpg'
    ]

    bg = cv2.imread(os.path.join(folder, img[mood]))

    text = text[15:]
    text = text.split('\n')
    today = datetime.date.today()
    date = f'{today.year} . {today.month} . {today.day}'

    font = ImageFont.truetype(fontPath, fontsize)
    imgPil = Image.fromarray(bg)
    draw = ImageDraw.Draw(imgPil)
    h, w, _ = bg.shape
    # x = w // 2 - (fontsize * len(text) // 2)
    for i, line in enumerate(text):
        x = w - margin - (i+1) * (fontsize + linewidth)
        y = margin + linewidth

        for c in line:
            draw.text((x, y), c, font=font, fill=color)
            y += fontsize

    # draw.text((x, 120), text, font=font, fill=color)
    draw.text((margin, h-fontsize-10),  date, font=font, fill=(52, 75, 91))

    imgCv2 = np.array(imgPil)

    imgSavePath = os.path.join(folder, tk + '_diary.jpg')
    cv2.imwrite(imgSavePath, imgCv2)

    img_url = glucose_graph(client_id, imgSavePath)

    if mood < len(img):
      return (img_url, imgSavePath)
    else:
      # 如果找不到對應的圖片，回傳 False
      return False


def handle_diary(tk, userID, text, mood, line_bot_api, folder):
    print('Text: ', text)
    if "---\n想記錄的話：\n---\n" in text:
        save_mood(userID, mood, folder)
        # img_url = reply_img(tk, text, mood, folder)   # 取得對應的圖片，如果沒有取得，會是 False
        # print(img_url)
        # if img_url:
        #     # 如果有圖片網址，回傳圖片
        #     img_message = ImageSendMessage(original_content_url=img_url[0], preview_image_url=img_url[0])
        #     line_bot_api.reply_message(tk, img_message)
        #     os.system(f'rm {img_url[1]}')

        #     save_mood(userID, mood, folder)
        # else:
        #     # 如果是 False，回傳文字
        #     text_message = TextSendMessage(text='找不到相關日記圖片')
        #     line_bot_api.reply_message(tk, text_message)
    else:
        text_message = TextSendMessage(text='請保留\n---\n想記錄的話：\n---\n')
        line_bot_api.reply_message(tk, text_message)

def save_mood(userID, mood, folder):#, mood_filename='mood_scores.pkl', action_filename='action_done.pkl'):
    # check if action done
    action_done = read_data('actions', 'done_date', userID)
    print('"""\nactions:')
    print(action_done)
    print(type(action_done))
    print('"""')
    # action_done = None
    # with open(os.path.join(folder, action_filename), 'rb') as f:
    #     action_done = pickle.load(f)

    today = datetime.date.today()
    # if action_done[userID] == today:
    #     return
    # else:
    if len(action_done) > 0 and action_done[0] != today:
        print('""" today not done """')
        # action_done[userID] = today
        # with open(os.path.join(folder, action_filename), 'wb') as f:
        #     pickle.dump(action_done, f)
        modify_val('actions', ['done_date'], [today], userID)

        # change mood score
        mood_scores = read_data('scores', 'score1, score2, score3, score4, score5', userID)
        print('"""\nscores:')
        print(mood_scores)
        print(type(mood_scores))
        print('"""')
        # mood_scores = None
        # with open(os.path.join(folder, mood_filename), 'rb') as f:
        #     mood_scores = pickle.load(f)

        # mood_scores[userID][-1] += (mood + 1)
        # print(userID, '分數：', mood_scores[userID][-1])

        # with open(os.path.join(folder, mood_filename), 'wb') as f:
        #     pickle.dump(mood_scores, f)
