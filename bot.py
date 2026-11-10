import telebot
from telebot import types

TOKEN = "9086651569:AAGF03eaKwdiuTXgXYRg-94MbIHQjF9cULg"
bot = telebot.TeleBot(TOKEN)

# ተጠቃሚዎችን ለመያዝ (በጊዜያዊነት በዲክሽነሪ)
users = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    args = message.text.split()
    
    if user_id not in users:
        # አዲስ ሰው ሲገባ 500 ብር ቦነስ ይሰጠዋል
        users[user_id] = {"balance": 500, "referrals": 0, "referred_by": None}
        
        # ማንም ሰው በሌላ ሰው ሊንክ ከገባ
        if len(args) > 1 and args[1].startswith("ref_"):
            try:
                referrer_id = int(args[1].replace("ref_", ""))
                if referrer_id != user_id and referrer_id in users:
                    users[user_id]["referred_by"] = referrer_id
                    users[referrer_id]["referrals"] += 1
                    users[referrer_id]["balance"] += 100  # ኢንቫይት ሲያደርግ 100 ብር ሽልማት
                    
                    # ላኪውን ማሳወቅ
                    bot.send_message(
                        referrer_id, 
                        f"🎉 እንኳን ደስ አለዎት! አንድ ሰው በሊንክዎ ገብቷል። 100 ብር ተሸልመዋል!\n💰 አጠቃላይ ቀሪ ሂሳብዎ: {users[referrer_id]['balance']} ብር"
                    )
            except:
                pass

    # የቁልፍ ሰሌዳ ማዘጋጀት
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("💰 ሂሳቤን ማየት (Balance)"), types.KeyboardButton("🔗 የጋበዣ ሊንክ (Referral Link)"))
    markup.add(types.KeyboardButton("💸 ገንዘብ ማውጣት (Withdraw)"))
    
    welcome_text = (
        "ሰላም! እንኳን ወደ ኮሜዲያን ያሲን ሪፈራል ቦት በደህና መጡ። 🎭\n\n"
        "🎁 ቦቱን በመቀላቀልዎ 500 ብር ተሸልመዋል!\n"
        "👥 ጓደኛዎችዎን በመጋበዝ እያንዳንዱ ሰው ቦቱን ሲቀላቀል 100 ብር ያግኙ።\n"
        "💳 ገንዘብ ማውጣት የሚችሉት ቀሪ ሂሳብዎ 2500 ብር ሲደርስ ብቻ ነው።"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🔗 የጋበዣ ሊንክ (Referral Link)")
def get_referral_link(message):
    user_id = message.from_user.id
    bot_info = bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start=ref_{user_id}"
    
    text = (
        f"🔗 **የእርስዎ ልዩ የመጋበዣ ሊንክ ይኸውና:**\n\n`{ref_link}`\n\n"
        "ይህንን ሊንክ ለጓደኛዎችዎ ሼር በማድረግ ሰዎች ቦቱን ሲቀላቀሉ 100 ብር ወደ አካውንትዎ ይገባል!"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "💰 ሂሳቤን ማየት (Balance)")
def check_balance(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"balance": 500, "referrals": 0, "referred_by": None}
    
    user_info = users[user_id]
    text = (
        f"📊 **የመለያዎ ሁኔታ (Account Balance):**\n\n"
        f"👤 የጋበዟቸው ሰዎች ብዛት: {user_info['referrals']} ሰው\n"
        f"💰 አጠቃላይ ቀሪ ሂሳብዎ: {user_info['balance']} ብር\n\n"
        f"💡 *ማስታወሻ:* ገንዘብ ማውጣት የሚችሉት 2500 ብር ሲደርስ ነው።"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "💸 ገንዘብ ማውጣት (Withdraw)")
def withdraw_money(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"balance": 500, "referrals": 0, "referred_by": None}
    
    current_balance = users[user_id]["balance"]
    
    if current_balance >= 2500:
        bot.reply_to(message, "✅ የባንክ ወይም የቴሌብር አካውንት ቁጥርዎን ይላኩ (Withdrawal Request Submitted)።")
    else:
        needed = 2500 - current_balance
        bot.reply_to(
            message, 
            f"❌ ይቅርታ፣ ገንዘብ ማውጣት የሚችሉት ቢያንስ **2500 ብር** ሲኖርዎት ብቻ ነው።\n\n"
            f"የእርስዎ አሁን ያለው ሂሳብ: **{current_balance} ብር** ነው።\n"
            f"ለማውጣት ተጨማሪ **{needed} ብር** ይቀረዎታል! ጓደኛዎችዎን በመጋበዝ ሂሳብዎን ያሳድጉ።"
        )

bot.infinity_polling()
