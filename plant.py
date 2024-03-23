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
    user_date = read_data('users', 'first_date', userID)[0]
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
    # days = (today - user_date).days
    days = 30

    # if days in grow_days:
        # mood_scores[userID].append(0)

        # with open(os.path.join(folder, mood_filename), 'wb') as f:
        #     pickle.dump(mood_scores, f)
        # modify_val('scores', [f'score{mood_scores.index(None)+1}'], [0], userID)
    stage = 0
    if days >= grow_days[2]:
        stage = 3
        modify_val('scores', ['stage'], [stage], userID)
    elif days >= grow_days[1]:
        stage = 2
        modify_val('scores', ['stage'], [stage], userID)
    elif days >= grow_days[0]:
        stage = 1
        modify_val('scores', ['stage'], [stage], userID)

    print(f'""" 第{days}天 """', userID)
    ############################################################
    img_url = grow_plant(tk, mood_scores, stage, folder)   # 取得對應的圖片，如果沒有取得，會是 False
    print(img_url)
    if img_url:
        reply_msgs = []

        if days >= 30:
            reply_msgs.append(ImageSendMessage(original_content_url=img_url[0], preview_image_url=img_url[0]))
            # os.system(f'rm {img_url[1]}')
            
            plant_name = read_data('users', 'plant_name', userID)[0]
            reply_msgs.append(TextSendMessage(text=f'我們的旅程已經走到了第 30 天，謝謝你的悉心照料。［{plant_name}］生長完成了！\n能在你的呵護裡，陪你一起走過一段，［{plant_name}］覺得很幸福❤️。'))
            
            imgSavePath = os.path.join(folder, 'star.png')
            img_url = glucose_graph(imgSavePath)
            reply_msgs.append(ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
        
            reply_msgs.append(TextSendMessage(text=f'完成旅程的［{plant_name}］，化作一顆溫柔的星，住進夜空裡守護你。\n謝謝你，是你的堅強和柔軟，讓我們一起走過。'))
            reply_msgs.append(TextSendMessage(text='這段旅程告一段落，我深深地祝福你，一切願望都能成真。\n你可以帶上回憶，離開這裡去往你的人生新篇。\n也可以繼續留下來和我們一起，種下一顆新種子，再度守護種子成長，種成一片屬於你的秘密花園。\n無論你在哪裡，這裡永遠歡迎你。\n\n（如果你想要再一起種下一顆新種子，請輸入：種下新的種子！）'))

        else:
            first_time = read_data('users', 'first_time', userID)[0]
            if first_time:
                reply_msgs.append(TextSendMessage(text='月亮種子的成長，需要我們細緻的照料。\n充足的水分的第一步，讓我們來幫種子澆水吧！\n每天都可以來找我一起澆水，我最擅長澆水了，畢竟我是小雲朵嘛～'))
                # line_bot_api.reply_message(tk, text_message)
            else:
                action_done = read_data('actions', 'plant_done_date', userID)[0]
                plant_name = read_data('users', 'plant_name', userID)[0]
                
                today = datetime.date.today()
            
                if action_done != today: 
                    print('""" today not plant done """')
                    modify_val('actions', ['plant_done_date'], [today.strftime('%Y-%m-%d')], userID)
            
                    reply_msgs.append(TextSendMessage(text=f'🌧️💦💦🌱澆水啦～再等等［{plant_name}］長大吧！'))
                else:
                    reply_msgs.append(TextSendMessage(text=f'今日份澆水已完成！明天再來幫［{plant_name}］澆水吧～☺️'))
                
            # 如果有圖片網址，回傳圖片
            reply_msgs.append(ImageSendMessage(original_content_url=img_url[0], preview_image_url=img_url[0]))
            # line_bot_api.reply_message(tk, img_message)
            # os.system(f'rm {img_url[1]}')
    
            if first_time:
                reply_msgs.append(TextSendMessage(text='哇！發芽了～\n種子的成長，會隨著每天記錄的心情月亮，產生不同變化，長成屬於你獨一而二的樣貌。\n讓我們一起期待，為你的小生命取個名字吧～'))
                reply_msgs.append(TextSendMessage(text='請輸入：我想取名為［］\n（［］中為你想取的名字，若之後想再更換名字，可以同樣輸入此訊息喔～）'))
        
        line_bot_api.reply_message(tk, reply_msgs)
        os.system(f'rm {img_url[1]}')
        
    else:
        # 如果是 False，回傳文字
        text_message = TextSendMessage(text='非常抱歉，月亮種子功能目前出現異常，如遇到問題請回報，我們會盡快修復！')
        line_bot_api.reply_message(tk, text_message)
    ############################################################


def grow_plant(tk, mood_scores, stage, folder):
    img_name = [
        '0.PNG',
        ['1-1.PNG',
         '2-1.PNG',
         '3-1.PNG',
         '4-1.PNG'],
        ['1-2.PNG',
         '2-2.PNG',
         '3-2.PNG',
         '4-2.PNG'],
        ['1-3.PNG',
         '2-3.PNG',
         '3-3.PNG',
         '4-3.PNG']
    ]
    
    img = cv2.imread(os.path.join(folder, img_name[0]), cv2.IMREAD_UNCHANGED)

    for i, mood in enumerate(mood_scores[:stage]):
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

def handle_plant_name(tk, userID, name, line_bot_api, folder):
    modify_val('users', ['plant_name'], [name], userID)

    reply_msgs = []
    
    reply_msgs.append(TextSendMessage(text=f'種子已被命名成［{name}］囉！'))
    # line_bot_api.reply_message(tk, text_message)
    
    first_time = read_data('users', 'first_time', userID)[0]
    print('"""\nusers first:')
    print(first_time)
    print(type(first_time))
    print('"""')
    if first_time:
        reply_msgs.append(TextSendMessage(text='接下來，讓我們共同度過這段值得珍惜的日子。好好照顧自己，我會在這裡陪伴你❤️'))
        # line_bot_api.reply_message(tk, text_message)

        imgSavePath = os.path.join(folder, '2.png')
        img_url = glucose_graph(imgSavePath)
        reply_msgs.append(ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
        
        modify_val('users', ['first_time'], [False], userID)
        
    line_bot_api.reply_message(tk, reply_msgs)

def handle_plant_new(tk, userID, line_bot_api, folder):
    modify_val('users', ['first_date'], [datetime.date.today().strftime('%Y-%m-%d')], userID)

    reply_msgs = []
    
    imgSavePath = os.path.join(folder, 'seed.png')
    img_url = glucose_graph(imgSavePath)
    reply_msgs.append(ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
        
    reply_msgs.append(TextSendMessage(text='已種下新的種子囉！'))

    line_bot_api.reply_message(tk, reply_msgs)
