from pymongo import MongoClient
import datetime
from config import mongodb

cluster = MongoClient(mongodb)
db = cluster['telegram']


def new_user(user_id):
    db.users.insert(
        {
            'uid': user_id,
            'state': 'onboarding',
            'summaries': [],
            'timestamp': datetime.datetime.utcnow()
        }
    )


def is_user_new(user_id):
    search = db.users.find_one(
        {
            'uid': user_id,
        }
    )
    if search is None:
        new_user(user_id=user_id)
        return True
    else:
        return False


def set_state(user_id, state):
    db.users.update(
        {'uid': user_id},
        {
            '$set': {
                'state': state
            }
        }
    )


def new_summary(user_id, message_id, summary_text, url, summary_type):
    sid = summaries_amount() + 1
    db.summaries.insert(
        {
            'sid': sid,
            'uid': user_id,
            'type': summary_type,
            'message_id': message_id,
            'summary_text': summary_text,
            'url': url,
            'timestamp': datetime.datetime.utcnow()
        }
    )
    return sid


def summaries_amount():
    return len(list(db.summaries.find()))


def get_state(user_id):
    return db.users.find_one({'uid': user_id})['state']
