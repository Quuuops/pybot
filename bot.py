from datetime import datetime, timedelta, date, time
from random import randrange

from telegram.ext import Updater, CommandHandler

import db

print("Бот запущен. Нажмите Ctrl+C для завершения")


def show_top(update, context):
    chat = update.effective_chat
    growth_users = db.database.select_top(chat.id)
    msg = 'Топ бутылок \n'
    for i in range(len(growth_users)):
        msg += '{}. @{} : {} см\n'.format(i+1,growth_users[i]['user'], growth_users[i]['growth'])
    context.bot.send_message(chat.id, text=msg)

def now_time():
    return time(00)


def palma(update, context):
    chat = update.effective_chat
    rand = randrange(-5, 15)
    curent_growth = db.database.select(update.message.from_user['id'],chat_id=chat.id)
    if curent_growth == None:
        print(update.message.from_user['username'], 'Добавлен')
        db.database.add(name=update.message.from_user['username'], first_name=update.message.from_user['first_name'],
                        user_id=
                        update.message.from_user['id'], count=0, chat_id=chat.id)
        db.database.update(user_id=update.message.from_user['id'],
                           date=datetime.combine(date.today() + timedelta(1), now_time()), palma=rand)
        curent_growth_now = db.database.select(update.message.from_user['id'],chat_id=chat.id)

        if rand < 0:

            context.bot.send_message(chat_id=chat.id, text="Ваша бутылка сократилась на {} \n"
                                                           "Ваша бутылка {} сантиметров".format(rand,
                                                                                                curent_growth_now[
                                                                                                    'growth']))
        else:
            context.bot.send_message(chat_id=chat.id, text="Ваша бутылка выросла на {} \n"
                                                           "Ваша бутылка {} сантиметров".format(rand,

                                                                                                curent_growth_now[
                                                                                                    'growth']))
    else:
        curent_user = db.database.select(update.message.from_user['id'],chat.id)
        if curent_user['date'] < datetime.now():
            db.database.update(user_id=update.message.from_user['id'],
                               date=datetime.combine(date.today() + timedelta(1), now_time()),
                               palma=rand)
            curent_growth_now = db.database.select(update.message.from_user['id'])

            if rand < 0:

                context.bot.send_message(chat_id=chat.id, text="Ваша бутылка сократилась на {} \n"
                                                               "Ваша бутылка {} сантиметров".format(rand,
                                                                                                    curent_growth_now[
                                                                                                        'growth']))
            else:
                context.bot.send_message(chat_id=chat.id, text="Ваша бутылка выросла на {} \n"
                                                               "Ваша бутылка {} сантиметров".format(rand,
                                                                                                    curent_growth_now[
                                                                                                        'growth']))
        else:
            curent_growth_user = db.database.select(update.message.from_user['id'],chat_id=chat.id)
            date_user_db = curent_growth_user['date']
            date_now = datetime.now()
            time = date_user_db - date_now
            minute = (time.seconds // 60) % 60
            hours = (time.seconds / 60) // 60
            print(chat.id)
            context.bot.send_message(chat_id=chat.id, text="Попробуй через {} ч {} м  ".format(int(hours), minute))


updater = Updater('', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("bottle", palma))
dispatcher.add_handler(CommandHandler("top10", show_top))

updater.start_polling()
updater.idle()
