from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler, ApplicationBuilder
import os
from dotenv import load_dotenv

load_dotenv()  # بارگذاری متغیرهای محیطی از فایل .env

app = Flask(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
application = ApplicationBuilder().token(TOKEN).build()


async def start(update: Update, context) -> None:
    keyboard = [
        [KeyboardButton('📦 خرید وی‌پی‌ان'), KeyboardButton('💬 پشتیبانی')],
        [KeyboardButton('ℹ️ درباره ما'), KeyboardButton('⚙️ تنظیمات')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('به ربات خوش آمدید! از منوی زیر استفاده کنید:', reply_markup=reply_markup)


async def buy(update: Update, context) -> None:
    keyboard = [
        [InlineKeyboardButton("خرید 1 ماهه - 10,000 تومان", callback_data='buy_1_month')],
        [InlineKeyboardButton("خرید 3 ماهه - 25,000 تومان", callback_data='buy_3_months')],
        [InlineKeyboardButton("خرید 1 ساله - 80,000 تومان", callback_data='buy_1_year')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('لطفاً یکی از پلن‌ها را انتخاب کنید:', reply_markup=reply_markup)


async def support(update: Update, context) -> None:
    await update.message.reply_text(
        'لطفاً سوال یا مشکل خود را ارسال کنید و تیم پشتیبانی ما به زودی با شما تماس خواهد گرفت.')


async def about_us(update: Update, context) -> None:
    await update.message.reply_text(
        'ما ارائه دهنده بهترین خدمات وی‌پی‌ان با کیفیت بالا هستیم. برای اطلاعات بیشتر به وبسایت ما مراجعه کنید.')


async def settings(update: Update, context) -> None:
    keyboard = [
        [InlineKeyboardButton("تغییر زبان", callback_data='change_language')],
        [InlineKeyboardButton("مدیریت اشتراک‌ها", callback_data='manage_subscriptions')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('لطفاً یکی از گزینه‌های زیر را انتخاب کنید:', reply_markup=reply_markup)


async def button(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'buy_1_month':
        await query.edit_message_text(text="شما پلن 1 ماهه را انتخاب کردید. لطفاً مبلغ 10,000 تومان را پرداخت کنید.")
    elif query.data == 'buy_3_months':
        await query.edit_message_text(text="شما پلن 3 ماهه را انتخاب کردید. لطفاً مبلغ 25,000 تومان را پرداخت کنید.")
    elif query.data == 'buy_1_year':
        await query.edit_message_text(text="شما پلن 1 ساله را انتخاب کردید. لطفاً مبلغ 80,000 تومان را پرداخت کنید.")
    elif query.data == 'change_language':
        await query.edit_message_text(text="قابلیت تغییر زبان هنوز فعال نشده است.")
    elif query.data == 'manage_subscriptions':
        await query.edit_message_text(text="مدیریت اشتراک‌ها در حال حاضر در دسترس نیست.")


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    application.update_queue.put(update)
    return 'ok'


if __name__ == '__main__':
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex('^(📦 خرید وی‌پی‌ان)$'), buy))
    application.add_handler(MessageHandler(filters.Regex('^(💬 پشتیبانی)$'), support))
    application.add_handler(MessageHandler(filters.Regex('^(ℹ️ درباره ما)$'), about_us))
    application.add_handler(MessageHandler(filters.Regex('^(⚙️ تنظیمات)$'), settings))
    application.add_handler(CallbackQueryHandler(button))

    app.run(port=5000)
