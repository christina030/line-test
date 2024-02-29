# -*- coding: utf-8 -*-

# 使用者

import pickle
import os
import datetime


def check_and_save_user(userID, folder, user_filename='users.pkl', mood_filename='mood_scores.pkl', action_filename='action_done.pkl'):
    # user file
    users = None
    with open(os.path.join(folder, user_filename), 'rb') as f:
        users = pickle.load(f)

    if userID in users.keys():
        return

    users[userID] = datetime.date.today()

    with open(os.path.join(folder, user_filename), 'wb') as f:
        pickle.dump(users, f)

    # mood score file
    mood_scores = None
    with open(os.path.join(folder, mood_filename), 'rb') as f:
        mood_scores = pickle.load(f)

    mood_scores[userID] = [0]

    with open(os.path.join(folder, mood_filename), 'wb') as f:
        pickle.dump(mood_scores, f)

    # action done file
    action_done = None
    with open(os.path.join(folder, action_filename), 'rb') as f:
        action_done = pickle.load(f)

    action_done[userID] = None

    with open(os.path.join(folder, action_filename), 'wb') as f:
        pickle.dump(action_done, f)
