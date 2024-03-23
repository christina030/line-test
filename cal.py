# -*- coding: utf-8 -*-

# 月曆

# import pickle
# import os
# import datetime
# from datetime import datetime as dt
# import cv2
# import numpy as np
from linebot.models import TextSendMessage    # 載入 TextSendMessage 和 ImageSendMessage 模組

# from rep import modify_val, read_data
from imgur import glucose_graph


def handle_calendar(tk, userID, line_bot_api, folder):
        reply_msgs = []
        
        reply_msgs.append(TextSendMessage(text='我們為你量身定做了小月子月曆~\n除了照顧每天的心情，也要好好照顧自己的身體。\n在這裡，可以查看小月子週期中，各階段可能的狀況及注意事項。\n小月子月曆連結：https://faith-ministry.my.canva.site/calender'))
        
        imgSavePath = os.path.join(folder, 'cal.png')
        img_url = glucose_graph(imgSavePath)
        reply_msgs.append(ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
        
        line_bot_api.reply_message(tk, reply_msgs)
  
