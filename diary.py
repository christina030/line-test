# -*- coding: utf-8 -*-

import pyimgur
from linebot.models import TextSendMessage, ImageSendMessage    # 載入 TextSendMessage 和 ImageSendMessage 模組
import os
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import datetime

# 回覆圖片或影片訊息

"""
[圖片URL](https://medium.com/@fidhaley/line-bot-python-%E5%BB%BA%E7%AB%8B%E6%88%91%E7%9A%84%E7%AC%AC%E4%B8%80%E5%80%8Bapp-3-linebot%E6%96%87%E5%AD%97%E6%8C%87%E4%BB%A4-%E5%AD%98%E5%8F%96%E5%9C%96%E7%89%87-%E6%9B%B4%E6%8F%9B%E6%A9%9F%E5%99%A8%E4%BA%BA%E5%A4%A7%E9%A0%AD%E8%B2%BC%E6%95%88%E6%9E%9C-1cbb61647d60)
"""

client_id = 'bde19e3500c4e17'
def glucose_graph(client_id, imgpath):
    im = pyimgur.Imgur(client_id)
    upload_image = im.upload_image(imgpath, title='Uploaded with PyImgur')
    return upload_image.link

"""
[自動回覆圖片](https://steam.oxxostudio.tw/category/python/example/line-reply-message.html)
[編輯圖片](https://blog.gtwang.org/programming/opencv-drawing-functions-tutorial/)
"""

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


def handle_diary(tk, userID, text, mood, line_bot_api):
    print('Text: ', text)
    if "---\n想記錄的話：\n---\n" in text:
        img_url = reply_img(tk, text, mood)   # 取得對應的圖片，如果沒有取得，會是 False
        print(img_url)
        if img_url:
            # 如果有圖片網址，回傳圖片
            img_message = ImageSendMessage(original_content_url=img_url[0], preview_image_url=img_url[0])
            line_bot_api.reply_message(tk, img_message)
            os.system(f'rm {img_url[1]}')

            save_mood(userID, mood)
        else:
            # 如果是 False，回傳文字
            text_message = TextSendMessage(text='找不到相關日記圖片')
            line_bot_api.reply_message(tk, text_message)
    else:
        text_message = TextSendMessage(text='請保留\n---\n想記錄的話：\n---\n')
        line_bot_api.reply_message(tk, text_message)
