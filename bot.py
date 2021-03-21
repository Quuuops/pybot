from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randrange
import db
from datetime import datetime,timedelta
print("Бот запущен. Нажмите Ctrl+C для завершения")


def palma(update, context):
    chat = update.effective_chat
    rand = randrange(-5, 15)
    curent_growth = db.database.select(update.message.from_user['id'])

    if curent_growth == None :
        print(update.message.from_user['username'], 'Добавлен')
        db.database.add(name=update.message.from_user['username'], first_name=update.message.from_user['first_name'],
                        user_id=
                        update.message.from_user['id'], count=0,)
        db.database.update(user_id=update.message.from_user['id'],date=datetime.now()+ timedelta(days=1), palma=rand)
        curent_growth_now = db.database.select(update.message.from_user['id'])


        if rand < 0:

            context.bot.send_message(chat_id=chat.id, text="Ваша бутылка сократилась на {} \n"
                                                           "Ваша бутылка {} сантиметров".format(rand,
                                                                                                curent_growth_now['growth']))
        else:
            context.bot.send_message(chat_id=chat.id, text="Ваша бутылка выросла на {} \n"
                                                           "Ваша бутылка {} сантиметров".format(rand,

                                                                                                curent_growth_now['growth']))
    else:
        curent_user =db.database.select(update.message.from_user['id'])
        if curent_user['date'] < datetime.now() :
            db.database.update(user_id=update.message.from_user['id'], date=datetime.now()+ timedelta(days=1), palma=rand)
            curent_growth_now = db.database.select(update.message.from_user['id'])

            if rand < 0:

                context.bot.send_message(chat_id=chat.id, text="Ваша бутылка сократилась на {} \n"
                                                               "Ваша бутылка {} сантиметров".format(rand,
                                                                                                    curent_growth_now['growth']))
            else:
                context.bot.send_message(chat_id=chat.id, text="Ваша бутылка выросла на {} \n"
                                                               "Ваша бутылка {} сантиметров".format(rand,
                                                                                                    curent_growth_now['growth']))
        else:
            curent_growth_user = db.database.select(update.message.from_user['id'])
            date_user_db = curent_growth_user['date']
            date_now = datetime.now()
            time = date_user_db-date_now
            minute = (time.seconds // 60) % 60
            hours = (time.seconds / 60) // 60
            context.bot.send_message(chat_id=chat.id, text="Попробуй через {} ч {} м  ".format(int(hours),minute))


updater = Updater('', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("bottle", palma))

updater.start_polling()
updater.idle()
