import os
import telegram
from telegram import Update

from telegram.ext import Updater, CommandHandler, CallbackContext

from db import insert, update_location, user_info
from app import *

from tokensec import *

PORT = int(os.environ.get('PORT',88))

manual = '/trends - get latest trends on your set location.\n'
'/location <city/country> - set location eg. (/location Kenya)\n'
'/set <seconds> - determine update frequency\n'
'/unset - remove automatic updates'

welcomeMessage = 'Hi, welcome to Twitter Trends.\n\
We will update you on latest trends on available locations of your choosing.\n\
/help to get manual'

def start(update: Update, context: CallbackContext):
    insert(update.message.chat_id)
    update.message.reply_text(welcomeMessage)
    
def help(update:Update, context: CallbackContext):
    update.message.reply_text(manual)
    
def location(update: Update, context: CallbackContext):
    try:
        loc = str(context.args[0])
        chat_id = update.message.chat_id
        update_location(chat_id,loc)
    except Exception as ex:

        update.message.reply_text('Usage: /location <city/country>')

def trends(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    update.message.reply_text(get_tweets(user_info(chat_id)[0][0]))

def alarm(context: CallbackContext):
    job = context.job
    context.bot.send_message(job.context,text=get_tweets(user_info(job.context)[0][0]))
    
def remove_job_if_exists(name: str, context: CallbackContext):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def set_timer(update:Update, context: CallbackContext):
    chat_id = update.message.chat_id
    
    try:
        due = int(context.args[0])
        
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(alarm,due,context=chat_id,name=str(chat_id))
        update.message.reply_text('Timer set successfully!')
        
    except (IndexError, KeyError):
        update.message.reply_text('Usage: /set <seconds>')
        
def unset(update:Update, context: CallbackContext):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def main():
    updater = Updater(TELEGRAM_TOKEN)
    
    dispatcher = updater.dispatcher

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("location",location))
    dispatcher.add_handler(CommandHandler("trends",trends))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CommandHandler("unset", unset))

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=int(PORT),url_path=TELEGRAM_TOKEN)
    updater.bot.set_webhook('https://ttrendbot.herouapp.com/' + TELEGRAM_TOKEN)

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()
    
if __name__ == '__main__':
    main()
