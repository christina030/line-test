# -*- coding: utf-8 -*-

# 小雲朵

# import pickle
# import os
# import datetime
# from datetime import datetime as dt
# import cv2
# import numpy as np
import random
from linebot.models import TextSendMessage    # 載入 TextSendMessage 和 ImageSendMessage 模組
from linebot.models import MessageAction, TemplateSendMessage, ConfirmTemplate

# from rep import modify_val, read_data

help_str = '''嗨～我是小雲朵，歡迎來到屬於我們的空間。
這裡的各種功能，都是為了照護流產後女性的身心需求，量身打造的個人化服務。

【專屬月曆】詳列出了小月子所需的日程，協助您流產後的身體修復。
依照您所處的階段，我們將傳送訊息，提醒您如何在相應的時間段好好照顧自己。

【心情日記】以月亮圖案為選項，陪伴您記錄這段日子裡圓缺的心情。
透過覺察自己的狀態安頓心情，是幫助我們自我療癒的必經之路。

【月亮種子】需要您每日澆水，就像我們希望您每日都好好照料自己。經過時日，月亮種子將依照您每日記錄下的心情月亮，每階段生長成不同的模樣。

30天後，月亮種子將長成屬於您這段旅程的模樣，紀念你我相伴的這段時光。
我們的旅程也將告一段落，期望您帶著小雲朵的祝褔，去往下一段美好篇章。'''

chat_list = [
        '注意休息，好好照顧自己唷！',
        '不論今天過得如何，都要記得留一些時間給自己。',
        '親愛的你，希望你今天一切都好～',
        '記得吃飽睡好～幫我好好照顧自己。',
        '有空的話，就做一些讓自己放鬆的事情吧♬',
        '親愛的你，記得給自己多一點溫柔和呵護，讓每一天都有個有個美好的開始～',
        '記得保持輕鬆心情，讓自己的心靈得到療癒。吃飯時可以選擇一些有助於身體調理的食材哦！',
        '如果你感到疲倦，不要勉強自己，多休息一會兒吧～保護好自己的身心健康是最重要的。',
        '不論今天過得如何，記得給自己一個機會去哀悼、去釋放心中的情緒。',
        '親愛的你，入夜之時，可以用香氛精油和舒緩的聲音，幫助你進入安穩的睡眠。'
]


def handle_littlecloud(userID, line_bot_api):
        line_bot_api.push_message(userID, TemplateSendMessage(
            alt_text='ConfirmTemplate',
            template=ConfirmTemplate(
                    text='哈囉～你要跟我聊天嗎？還是需要幫助呢？',
                    actions=[
                        MessageAction(
                            label='聊天',
                            text='來聊一聊吧～'
                        ),
                        MessageAction(
                            label='幫助',
                            text='我需要幫助～'
                        )
                    ]
                )
        ))

def handle_help(tk, userID, line_bot_api):
        text_message = TextSendMessage(text=help_str)
        line_bot_api.reply_message(tk, text_message)
  
def handle_chat(tk, userID, line_bot_api):
        chat_str = random.choice(chat_list)
        text_message = TextSendMessage(text=chat_str)
        line_bot_api.reply_message(tk, text_message)
  
