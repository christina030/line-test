# -*- coding: utf-8 -*-

# 使用者

import pickle
import os
import datetime

from rep import add_row, read_data


def check_and_save_user(userID, folder):#, user_filename='users.pkl', mood_filename='mood_scores.pkl', action_filename='action_done.pkl'):
    # user file
    users = read_data('users', 'user_id', userID)
    print('"""\nusers:')
    print(users)
    print(type(users))
    print('"""')
    # users = None
    # with open(os.path.join(folder, user_filename), 'rb') as f:
    #     users = pickle.load(f)

    # if userID in users.keys():
    if users is not None:
        print('""" user already """')
        return

    # users[userID] = datetime.date.today()

    # with open(os.path.join(folder, user_filename), 'wb') as f:
    #     pickle.dump(users, f)
    add_row('users', '(user_id, first_date)', (userID, datetime.date.today().strftime('%Y-%m-%d')))

    # mood score file
    # mood_scores = None
    # with open(os.path.join(folder, mood_filename), 'rb') as f:
    #     mood_scores = pickle.load(f)

    # mood_scores[userID] = [0]

    # with open(os.path.join(folder, mood_filename), 'wb') as f:
    #     pickle.dump(mood_scores, f)
    add_row('scores', '(user_id, score1)', (userID, 0))

    # action done file
    # action_done = None
    # with open(os.path.join(folder, action_filename), 'rb') as f:
    #     action_done = pickle.load(f)

    # action_done[userID] = None

    # with open(os.path.join(folder, action_filename), 'wb') as f:
    #     pickle.dump(action_done, f)
    add_row('actions', '(user_id)', (userID))
