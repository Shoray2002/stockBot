#!/usr/bin/env python3
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler,Filters
# from jugaad_data.nse import NSELive
from datetime import  date,timedelta
from jugaad_data.nse import stock_csv, stock_df
from nsetools import Nse
nse=Nse()
import logging

TOKEN = '1944457344:AAFVfCOhzvs2_qEwu_cxsnYu28gQ8VL57zQ'

def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def echo(update: Update, context: CallbackContext) -> None:
    t=update.message.text.upper()
    df = stock_df(symbol=t, from_date=date.today()-timedelta(days=1),to_date=date.today(), series="EQ")
    df=df.drop(['VWAP'  , '52W H' , '52W L'  ,  'VOLUME'  ,'VALUE' , 'NO OF TRADES' ],axis=1)
    update.message.reply_text(df.head(1).to_string())


def check(update: Update, context: CallbackContext) -> None:
    all_stock_codes = nse.get_stock_codes()
    update.message.reply_text(all_stock_codes)
    
updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(MessageHandler(Filters.text, check))
updater.dispatcher.add_handler(MessageHandler(Filters.text,echo))

updater.start_polling()

updater.idle()


