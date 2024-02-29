import os

from diary import handle_diary
from plant import handle_grow
from user import check_and_save_user


def check_handle_message(event, line_bot_api, msg_filename='msgs.pkl'):
    tk = event.reply_token
    if event.type == 'postback':
        text = event.postback.data
    elif event.type == 'message':
        text = event.message.text
    userID = event.source.user_id

    # check_and_save_user
    check_and_save_user(userID)

    # msgs file
    msgs = None
    with open(os.path.join(folder, msg_filename), 'rb') as f:
        msgs = pickle.load(f)


    if userID in msgs.keys():
        if msgs[userID][0][1] == 'diary':
            if tk != msgs[userID][0][0]:
                print('Start handle diary!')
                handle_diary(tk, userID, text, msgs[userID][0][2], line_bot_api)
                print('End handle diary!')
                del msgs[userID]

                with open(os.path.join(folder, msg_filename), 'wb') as f:
                    pickle.dump(msgs, f)

    elif text in diary_mood:
        msgs[userID] = [[tk, 'diary', diary_mood.index(text)]]

        with open(os.path.join(folder, msg_filename), 'wb') as f:
            pickle.dump(msgs, f)

    elif text == 'change-to-plant':
        handle_grow(tk, userID, line_bot_api)
