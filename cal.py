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


def handle_calendar(tk, userID, line_bot_api, folder):
        text_message = TextSendMessage(text='我們為你量身定做了小月子月曆~\n除了照顧每天的心情，也要好好照顧自己的身體。\n在這裡，可以查看小月子週期中，各階段可能的狀況及注意事項。\n小月子月曆連結：https://reurl.cc/97mWlv')
        line_bot_api.reply_message(tk, text_message)
  
