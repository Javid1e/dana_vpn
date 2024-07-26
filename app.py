from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher, Updater
import os
from dotenv import load_dotenv

load_dotenv()  # بارگذاری متغیرهای محیطی از فایل .env

app = Flask(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Updater(TOKEN, use_context=True).bot


def start(update: Update, context) -> None:
    keyboard = [
        [KeyboardButton('📦 خرید وی‌پی‌ان'), KeyboardButton('💬 پشتیبانی')],
        [KeyboardButton('ℹ️ درباره ما'), KeyboardButton('⚙️ تنظیمات')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('به ربات خوش آمدید! از منوی زیر استفاده کنید:', reply_markup=reply_markup)


def buy(update: Update, context) -> None:
    keyboard = [
        [InlineKeyboardButton("خرید 1 ماهه - 10,000 تومان", callback_data='buy_1_month')],
        [InlineKeyboardButton("خرید 3 ماهه - 25,000 تومان", callback_data='buy_3_months')],
        [InlineKeyboardButton("خرید 1 ساله - 80,000 تومان", callback_data='buy_1_year')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('لطفاً یکی از پلن‌ها را انتخاب کنید:', reply_markup=reply_markup)


def support(update: Update, context) -> None:
    update.message.reply_text('لطفاً سوال یا مشکل خود را ارسال کنید و تیم پشتیبانی ما به زودی با شما تماس خواهد گرفت.')


def about_us(update: Update, context) -> None:
    update.message.reply_text(
        'ما ارائه دهنده بهترین خدمات وی‌پی‌ان با کیفیت بالا هستیم. برای اطلاعات بیشتر به وبسایت ما مراجعه کنید.')


def settings(update: Update, context) -> None:
    keyboard = [
        [InlineKeyboardButton("تغییر زبان", callback_data='change_language')],
        [InlineKeyboardButton("مدیریت اشتراک‌ها", callback_data='manage_subscriptions')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('لطفاً یکی از گزینه‌های زیر را انتخاب کنید:', reply_markup=reply_markup)


def button(update: Update, context) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'buy_1_month':
        query.edit_message_text(text="شما پلن 1 ماهه را انتخاب کردید. لطفاً مبلغ 10,000 تومان را پرداخت کنید.")
    elif query.data == 'buy_3_months':
        query.edit_message_text(text="شما پلن 3 ماهه را انتخاب کردید. لطفاً مبلغ 25,000 تومان را پرداخت کنید.")
    elif query.data == 'buy_1_year':
        query.edit_message_text(text="شما پلن 1 ساله را انتخاب کردید. لطفاً مبلغ 80,000 تومان را پرداخت کنید.")
    elif query.data == 'change_language':
        query.edit_message_text(text="قابلیت تغییر زبان هنوز فعال نشده است.")
    elif query.data == 'manage_subscriptions':
        query.edit_message_text(text="مدیریت اشتراک‌ها در حال حاضر در دسترس نیست.")


@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'


if __name__ == '__main__':
    dispatcher = Dispatcher(bot, None, workers=0)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(📦 خرید وی‌پی‌ان)$'), buy))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(💬 پشتیبانی)$'), support))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(ℹ️ درباره ما)$'), about_us))
    dispatcher.add_handler(MessageHandler(Filters.regex('^(⚙️ تنظیمات)$'), settings))
    dispatcher.add_handler(CallbackQueryHandler(button))

    app.run(port=5000)
