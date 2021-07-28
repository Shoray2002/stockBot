import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler,  CallbackContext
from datetime import  date,timedelta
from nsetools import Nse
nse=Nse()
from jugaad_data.nse import stock_csv, stock_df

TOKEN ='1944457344:AAFVfCOhzvs2_qEwu_cxsnYu28gQ8VL57zQ'
PORT = int(os.environ.get('PORT', '5000'))
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text('Hi! This bots helps you in everything related to Stocks of NSE')



def check(update: Update, context: CallbackContext) -> bool:
  t = str(context.args[0]).upper()
  s=nse.is_valid_code(t)
  update.message.reply_text(f'{t} is valid' if s else f'{t} is invalid')



def get_quote(update: Update, context: CallbackContext) -> None:
    """Get a quote"""
    # chat_id = update.message.chat_id
    try:
        t = str(context.args[0])
        # print(t)
        
        if nse.is_valid_code(t)==True:
            df = stock_df(symbol=t, from_date=date.today()-timedelta(days=1),to_date=date.today(), series="EQ")
            update.message.reply_text(f'Date: {df.DATE.to_string(index=False)}\nOpen: {df.OPEN.to_string(index=False)}\nClose: {df.CLOSE.to_string(index=False)}\nHIGH: {df.HIGH.to_string(index=False)}\nLOW: {df.LOW.to_string(index=False)} ')
        else :
            update.message.reply_text(f"INVALID stock code: {t.upper()}")


    except (IndexError, ValueError):
        update.message.reply_text('IMPROVE THE CODE')


def main() -> None:
    """Run bot."""
    print("started")
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("check", check))
    dispatcher.add_handler(CommandHandler("get", get_quote))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()