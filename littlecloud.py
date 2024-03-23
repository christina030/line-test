# -*- coding: utf-8 -*-

# 小雲朵

# import pickle
# import os
# import datetime
# from datetime import datetime as dt
# import cv2
# import numpy as np
from linebot.models import TextSendMessage    # 載入 TextSendMessage 和 ImageSendMessage 模組

# from rep import modify_val, read_data

help_str = '''嗨～我是小雲朵，歡迎來到屬於我們的空間。
這裡的各種功能，都是為了照護流產後女性的身心需求，量身打造的個人化服務。

【專屬月曆】詳列出了小月子所需的日程，協助您流產後的身體修復。
依照您所處的階段，我們將傳送訊息，提醒您如何在相應的時間段好好照顧自己。

【心情日記】以月亮圖案為選項，陪伴您記錄這段日子裡圓缺的心情。
透過覺察自己的狀態安頓心情，是幫助我們自我療癒的必經之路。

【月亮種子】需要您每日澆水，就像我們希望您每日都好好照料自己。經過時日，月亮種子將依照您每日記錄下的心情月亮，每階段生長成不同的模樣。

30天後，月亮種子將長成屬於您這段旅程的模樣，紀念你我相伴的這段時光。
我們的旅程也將告一段落，期望您帶著小雲朵的祝褔，去往下一段美好篇章。
'''

def handle_littlecloud(tk, userID, line_bot_api, folder):
        text_message = TextSendMessage(text=help_str)
        line_bot_api.reply_message(tk, text_message)
  
