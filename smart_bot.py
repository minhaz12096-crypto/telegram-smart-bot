import telebot
from telebot import types
import schedule
import time
import threading

BOT_TOKEN = "8500048782:AAF-FX5ZJP7Ij5RJMwi002o_ePIQFoOthAY"   # তোমার টোকেন

bot = telebot.TeleBot(BOT_TOKEN)

REACTION_EMOJI = "🔥"

DAILY_MESSAGE = """🌟 প্রতিদিনের আপডেট

গ্রুপে স্বাগতম! 
নিয়ম মেনে চলুন।
নতুন কনটেন্ট চেক করুন।

ধন্যবাদ ❤️"""

# Auto Reaction
@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'sticker', 'animation'])
def auto_react(message):
    try:
        bot.set_message_reaction(message.chat.id, message.message_id, [types.ReactionTypeEmoji(REACTION_EMOJI)])
    except:
        pass

# Auto Approve Join
@bot.chat_join_request_handler()
def approve_join(request):
    try:
        bot.approve_chat_join_request(request.chat.id, request.from_user.id)
    except:
        pass

# Auto Ban on Leave + Log
@bot.chat_member_handler()
def ban_on_leave(update):
    try:
        old = update.old_chat_member
        new = update.new_chat_member
        if old and old.status in ['member', 'administrator'] and new and new.status in ['left', 'kicked']:
            user = new.user
            chat_id = update.chat.id
            if user.is_bot:
                return
            bot.ban_chat_member(chat_id, user.id)
            user_name = f"@{user.username}" if user.username else user.first_name
            log_text = f"🚫 **Ban করা হয়েছে**\nUser: {user_name}\nকারণ: Left করেছে"
            bot.send_message(chat_id, log_text, parse_mode='Markdown')
    except:
        pass

# Daily Post (chat_id এখানে বসাও)
def send_daily_post():
    chat_id = -100xxxxxxxxxx   # ← এখানে তোমার গ্রুপের chat_id বসাও
    if chat_id:
        try:
            bot.send_message(chat_id, DAILY_MESSAGE, parse_mode='Markdown')
        except:
            pass

def schedule_thread():
    schedule.every(24).hours.do(send_daily_post)
    while True:
        schedule.run_pending()
        time.sleep(60)

print("Bot চালু হয়েছে...")
threading.Thread(target=schedule_thread, daemon=True).start()

bot.infinity_polling(allowed_updates=['message', 'chat_join_request', 'chat_member'])
