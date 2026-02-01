import logging
import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ---------- تنظیمات ----------
TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = '@RT_Trading_mobin'
CHANNEL_LINK = "https://t.me/RT_Trading_mobin"

ADMIN_IDS = [5681126670]  # 👈 آیدی عددی خودت رو اینجا بذار
USERS_FILE = "users.json"

# ---------- لاگ ----------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------- مدیریت کاربران ----------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def register_user(user_id):
    users = load_users()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if str(user_id) not in users:
        users[str(user_id)] = {
            "first_seen": now,
            "last_seen": now
        }
    else:
        users[str(user_id)]["last_seen"] = now

    save_users(users)

# ---------- منوی اصلی ----------
def main_menu():
    keyboard = [
        [InlineKeyboardButton("دریافت کانفیگ‌های رایگان🎁", callback_data='config')],
        [InlineKeyboardButton("دانلودر ⬇️", callback_data='downloader')],
        [InlineKeyboardButton("چنل ترید و تحلیل📊", callback_data='channel')],
        [InlineKeyboardButton("آیدی سازنده جهت پشتیبانی☎️", callback_data='support')]
    ]
    return InlineKeyboardMarkup(keyboard)

def join_keyboard():
    keyboard = [
        [InlineKeyboardButton("📢 عضویت در چنل", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ عضو شدم", callback_data='check_join')]
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- بررسی عضویت ----------
async def is_member(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# ---------- start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    register_user(user_id)

    if await is_member(context.bot, user_id):
        await update.message.reply_text(
            "درود❤️ خوش آمدید، یکی از گزینه‌ها رو انتخاب کنید👇",
            reply_markup=main_menu()
        )
    else:
        await update.message.reply_text(
            "برای استفاده از ربات باید ابتدا عضو چنل بشی 👇\n"
            "بعد از عضویت روی «عضو شدم» بزن.",
            reply_markup=join_keyboard()
        )

# ---------- آمار کاربران (فقط ادمین) ----------
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        return  # هیچ جوابی نده

    users = load_users()
    total = len(users)

    await update.message.reply_text(
        f"📊 آمار ربات:\n\n"
        f"👤 تعداد کل کاربران: {total}"
    )

# ---------- دکمه‌ها ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == 'check_join':
        if await is_member(context.bot, user_id):
            await query.edit_message_text(
                "درود❤️ خوش آمدید، یکی از گزینه‌ها رو انتخاب کنید👇",
                reply_markup=main_menu()
            )
        else:
            await query.answer("❌ هنوز عضو چنل نشدی", show_alert=True)
        return

    if not await is_member(context.bot, user_id):
        await query.edit_message_text(
            "برای استفاده از ربات باید ابتدا عضو چنل بشی 👇\n"
            "بعد از عضویت روی «عضو شدم» بزن.",
            reply_markup=join_keyboard()
        )
        return

    if data == 'support':
        await query.edit_message_text("آیدی سازنده: @RT_mobin برای پشتیبانی")

    elif data == 'channel':
        await query.edit_message_text(
            "چنل ترید و تحلیل 📊\n"
            "[ورود به چنل](https://t.me/RT_Trading_mobin)",
            parse_mode='Markdown'
        )

    elif data == 'downloader':
        await query.edit_message_text("⬇️ این بخش به زودی فعال می‌شود ⏳")

    elif data == 'config':
        config_text = """```
کد کانفیگ 1:
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTpvWklvQTY5UTh5aGNRVjhrYTNQYTNB@82.38.31.89:8080#%40RT_mobin

کد کانفیگ 2:
vless://bb8c74a1-abc1-4511-b100-9876e30cb65c@172.64.145.38:8443?path=%2F%3Fed%3D2560&security=tls&alpn=http%2F1.1&encryption=none&insecure=0&host=xfjd79v2tjscrm6jqo.zjde5.de5.net&type=ws&allowInsecure=0&sni=xfjd79v2tjscrm6jqo.zjde5.de5.net#%40RT_mobin

کد کانفیگ 3:
vmess://eyJhZGQiOiIxNDcuMTM1LjIxMS42MSIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiJjZGMyNzg4MC1hYzJiLTU5MWYtYjY3Ny1mY2IwMmZjYjQyOGEiLCJpbnNlY3VyZSI6IjAiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjgwODAiLCJwcyI6IlZJUF9Nb2Jpbl9mYXN08J+RkSIsInNjeSI6ImNoYWNoYTIwLXBvbHkxMzA1Iiwic25pIjoiIiwidGxzIjoiIiwidHlwZSI6Im5vbmUiLCJ2IjoiMiJ9

کد کانفیگ 4:
vless://396c904b-4b62-4334-b793-ee25fc0c61cc@188.114.96.3:443?path=%2FeyJqdW5rIjoiTHczMWlhREZIb0ljUDhoaCIsInByb3RvY29sIjoidmwiLCJtb2RlIjoicHJveHlpcCIsInBhbmVsSVBzIjpbXX0%3D%3Fed%3D2560&security=tls&encryption=none&insecure=0&host=8vmU06cxdz59m931xnREgj8qpnoq1-06.pages.dev&fp=chrome&type=ws&allowInsecure=0&sni=pages.dev#%40RT_mobin2

پایین صفحه گزینه کپی رو انتخاب و توی برنامه مد نظر واردش کنید و لذت ببرید
```"""
        await query.edit_message_text(
            "🎁 کانفیگ‌های رایگان:\n\n" + config_text,
            parse_mode='Markdown'
        )

# ---------- ارسال پیام به همه کاربران ----------
async def update_all_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # فقط ادمین‌ها می‌توانند از این دستور استفاده کنند
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ شما مجوز استفاده از این دستور را ندارید.")
        return

    # متن ارسالی از کاربر
    message_text = ' '.join(context.args)

    if not message_text:
        await update.message.reply_text("❌ لطفاً متن پیام خود را وارد کنید.")
        return

    # بارگذاری کاربران
    users = load_users()

    # ارسال پیام به همه کاربران
    for user in users:
        try:
            await context.bot.send_message(chat_id=user, text=message_text)
        except Exception as e:
            logger.error(f"خطا در ارسال پیام به کاربر {user}: {e}")

    await update.message.reply_text("✅ پیام شما به همه کاربران ارسال شد.")

# ---------- اجرا ----------
def main():
    app = Application.builder().token(TOKEN).build()
    
    # اضافه کردن دستور جدید برای ارسال پیام به همه کاربران
    app.add_handler(CommandHandler("update", update_all_users))

    # دستورات قبلی
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(buttons))
    
    app.run_polling()

if __name__ == '__main__':
    main()
