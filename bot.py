import logging
import os
PORT = int(os.environ.get('PORT', 5000))
from telegram import Update
from telegram.ext import Updater, CommandHandler,  CallbackContext
from datetime import  date,timedelta
from nsetools import Nse
nse=Nse()
from jugaad_data.nse import stock_csv, stock_df


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text('Hi! This bots helps you in everything related to Stocks of NSE')



def check(update: Update, context: CallbackContext) -> bool:
  t = str(context.args[0])
  s=nse.is_valid_code(t)
  update.message.reply_text(f'{t.upper()} is valid' if s else f'{t.lower()} is invalid')



def get_quote(update: Update, context: CallbackContext) -> None:
    """Get a quote"""
    # chat_id = update.message.chat_id
    try:
        t = str(context.args[0])
        print(t)
        df = stock_df(symbol=t, from_date=date.today()-timedelta(days=1),to_date=date.today(), series="EQ")
        df=df.drop(['VWAP'  , '52W H' , '52W L'  ,  'VOLUME'  ,'VALUE' , 'NO OF TRADES' ],axis=1)
        update.message.reply_text(df.head(1).to_string())

    except (IndexError, ValueError):
        update.message.reply_text('IMPROVE THE CODE')



def main() -> None:
    """Run bot."""
    TOKEN=os.getenv('TOKEN')
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("check", check))
    dispatcher.add_handler(CommandHandler("get", get_quote))
    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
    updater.bot.setWebhook('https://stockbot-28.herokuapp.com/' + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()