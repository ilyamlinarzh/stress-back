from background.consts import stress_symbols, a_letters, stress_symbols_for_all, community_token, keyboard_template, emoji, goodTemplates, badTemplates, goodEmoji, badEmoji
from db.models import User, Word, BotAttach
from peewee import fn
import datetime
import vk_api
import json
import random

session = vk_api.VkApi(token=community_token)

def initStringWord(word):
    w = ''
    bit_n = 0
    s = False
    for l in word:
        if l in a_letters:
            if not s:
                bit_n += 1

        if l in stress_symbols.keys():
            w+=stress_symbols[l]
            s=True
        else:
            w+=l

    return dict(word=w, bit_n=bit_n)

def getAllStresses(word):
    word = word.lower()
    writes = []
    for i in range(len(word)):
            l = word[i]
            if l in a_letters:
                thisWrite = list(word)
                thisWriteR = list(word)
                thisWrite[i] = stress_symbols_for_all[l]
                thisWriteR[i] = l.upper()
                writes.append([''.join(thisWrite), ''.join(thisWriteR)])
    return writes

def randomWord():
    word = Word.select().order_by(fn.Random()).limit(1)
    return word[0]

def getUsersToSend():
    users_time = User.select().where(User.notify == True and (User.last_bot_answer + User.period) <= int(datetime.datetime.now().timestamp()))
    users_attach = BotAttach.select()
    print(len(users_time), len(users_attach))
    users_time_ids = [u.userid for u in users_time]
    users_attach_ids = [u.user.userid for u in users_attach]
    print(users_time_ids, users_attach_ids)
    return list( set(users_time_ids) - set(users_attach_ids) )

def removeBotAttach(userids):
    users = User.select().where(User.userid.in_(userids))
    attaches = BotAttach.delete().where(BotAttach.user.in_(users))
    attaches.execute()

def addBotAttach(userids, word):
    users = User.select().where(User.userid.in_(userids))
    attaches = BotAttach.delete().where(BotAttach.user.in_(users))
    attaches.execute()
    data = [
        (user, word)
        for user in users
    ]
    BotAttach.insert_many(data, fields=[BotAttach.user, BotAttach.word]).execute()

def chunks_generators(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]

def button(word_var):
    payload = dict(
        action='answer',
        normal=word_var[1]
    )
    return [
         {
            "action":{
               "type":"text",
                "label":word_var[0],
               "payload":json.dumps(payload)
            }
         }
      ]

def sendTask(users, word):
    word_vars = getAllStresses(word.word)
    buttons = [button(v) for v in word_vars]
    keyboard = keyboard_template
    keyboard['buttons'] = buttons
    emoji_sym = emoji[random.randint(0, len(emoji)-1)]
    message = f'{emoji_sym} Укажите ударение в слове «{word.word.lower()}»'
    if len(word.description) > 0:
        message += f' ({word.description})'
    session.method('messages.send', dict(
        random_id=0,
        message=message,
        keyboard=json.dumps(keyboard),
        peer_ids=','.join([str(i) for i in users])
    ))
    addBotAttach(users, word)

def updateAnswerTime(userid):
    q = User.update(last_bot_answer=int(datetime.datetime.now().timestamp())).where(User.userid==userid)
    q.execute()

def messageTrue(userid, goodAnswer, interpretation=''):
    updateAnswerTime(userid)
    removeBotAttach([userid])
    word = initStringWord(goodAnswer)
    intro = goodTemplates[random.randint(0, len(goodTemplates)-1)]
    emoji_sym = goodEmoji[random.randint(0, len(goodEmoji)-1)]
    message = f'{emoji_sym} {intro}\n{word["word"]} — ударение на {word["bit_n"]} слог'
    if len(interpretation) > 0:
        int = initStringWord(interpretation)
        message += f' ({int["word"]})'
    session.method('messages.send', dict(
        random_id=0,
        peer_id = str(userid),
        message=message
    ))

def messageFalse(userid, goodAnswer, interpretation=''):
    updateAnswerTime(userid)
    removeBotAttach([userid])
    word = initStringWord(goodAnswer)
    intro = badTemplates[random.randint(0, len(badTemplates)-1)]
    emoji_sym = badEmoji[random.randint(0, len(badEmoji)-1)]
    message = f'{emoji_sym} {intro}\n{word["word"]} — ударение на {word["bit_n"]} слог'
    if len(interpretation) > 0:
        int = initStringWord(interpretation)
        message += f' ({int["word"]})'
    session.method('messages.send', dict(
        random_id=0,
        peer_id = str(userid),
        message=message
    ))