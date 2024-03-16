# -*- coding: utf-8 -*-

import pickle
import os

from diary import handle_diary
from plant import handle_grow
from user import check_and_save_user
from rep import add_row, modify_val, read_data, delete_row


diary_mood = ['action=diary&mood=1', 'action=diary&mood=2', 'action=diary&mood=3', 'action=diary&mood=4', 'action=diary&mood=5', 'action=diary&mood=6']

def check_handle_message(event, line_bot_api, folder):#, msg_filename='msgs.pkl'):
    tk = event.reply_token
    if event.type == 'postback':
        text = event.postback.data
    elif event.type == 'message':
        text = event.message.text
    userID = event.source.user_id
    print('""" receive """', event)
    print(text, tk, userID)

    # check_and_save_user
    check_and_save_user(userID, folder)

    # msgs file
    msgs = read_data('msgs', 'token, mood', userID)
    print('"""\nmsgs:')
    print(msgs)
    print(type(msgs))
    print('"""')
    # msgs = None
    # with open(os.path.join(folder, msg_filename), 'rb') as f:
    #     msgs = pickle.load(f)


    # if userID in msgs.keys():
    if msgs is not None:
        print('""" have chosen mood """')
        if tk != msgs[0]:
            print('Start handle diary!')
            handle_diary(tk, userID, text, msgs[1], line_bot_api, folder)
            print('End handle diary!')
            delete_row('msgs', userID)
        # if msgs[userID][0][1] == 'diary':
        #     if tk != msgs[userID][0][0]:
        #         print('Start handle diary!')
        #         handle_diary(tk, userID, text, msgs[userID][0][2], line_bot_api, folder)
        #         print('End handle diary!')
        #         del msgs[userID]

        #         with open(os.path.join(folder, msg_filename), 'wb') as f:
        #             pickle.dump(msgs, f)

    elif text in diary_mood:
        add_row('msgs', '(user_id, token, mood)', (userID, tk, diary_mood.index(text)))
        # msgs[userID] = [[tk, 'diary', diary_mood.index(text)]]

        # with open(os.path.join(folder, msg_filename), 'wb') as f:
        #     pickle.dump(msgs, f)

    # elif text == 'change-to-plant':
    elif text == 'change-to-plant' or text == '植栽':
        handle_grow(tk, userID, line_bot_api, folder)
