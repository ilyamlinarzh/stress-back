from schedule import every, repeat, run_pending
import time
# from ..db.models import User, Word, BotAttach
from consts import community_token
from helpers import randomWord, getUsersToSend, addBotAttach, getAllStresses, chunks_generators, sendTask
from threading import Thread


@repeat(every(90).seconds)
def handler():
    users = getUsersToSend()
    if len(users) == 0:
        return

    word = randomWord()
    users_groups = chunks_generators(users, 100)
    for group in users_groups:
        Thread(target=sendTask, args=(group, word)).start()


if __name__ == '__main__':
    handler()
    while True:
        try:
            run_pending()
            time.sleep(1)
        except:
            pass