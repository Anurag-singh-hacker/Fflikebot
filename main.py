from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ChatMemberHandler,
)
from telegram.constants import ChatMemberStatus
import httpx
import asyncio
import time

# ================= BOT CONFIG =================
BOT_TOKEN = "8457141988:AAFqXgZwhuIPp6WJ7-dQfSUFqrnzjFEfwJs"

OWNER_ID = 6826304542  # 🔴 APNA TELEGRAM USER ID DAALO (@userinfobot)

# 🔗 Channel Links
CHANNEL_LINK_1 = "https://t.me/+4lV7uE_l89w4NDZl"
CHANNEL_LINK_2 = "https://t.me/+CAPGfkPG_UQ4Njll"
CHANNEL_LINK_3 = "https://t.me/goodlikemee"

# ⏳ Anti Spam
cooldown = {}
COOLDOWN_TIME = 8

# 🧠 UID Memory
uid_joined = set()

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome\n\n"
        "/like 12345678\n"
        "/info 12345678\n\n"
        "☠️ Developer Anurag Singh"
    )

# ================= SPAM CHECK =================
def is_spamming(user_id):
    now = time.time()
    if user_id in cooldown and now - cooldown[user_id] < COOLDOWN_TIME:
        return True
    cooldown[user_id] = now
    return False

# ================= JOIN MESSAGE =================
async def send_join_message(update: Update):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_LINK_1)],
        [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_LINK_2)],
        [InlineKeyboardButton("📢 Join Channel 3", url=CHANNEL_LINK_3)],
    ]
    await update.message.reply_text(
        "🚀 Premium Access Required\n\n"
        "Join all channels first.\n"
        "Then send the command again.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ================= LIKE =================
async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if is_spamming(user_id):
        await update.message.reply_text("⏳ Please wait 8 seconds and try again.")
        return

    if not context.args:
        await update.message.reply_text("❌ Use: /like 12345678")
        return

    uid = context.args[0]

    if uid not in uid_joined:
        uid_joined.add(uid)
        await send_join_message(update)
        return

    msg = await update.message.reply_text("⏳ Processing likes...")

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            url = f"https://mukesh-ult-like.vercel.app/like?uid={uid}&region=ind&key=UDIT"
            r = await client.get(url)
            data = r.json()

        text = (
            f"🥰 Likes Given : {data.get('LikesGivenByAPI','N/A')}\n"
            f"🤗 Likes After : {data.get('LikesafterCommand','N/A')}\n"
            f"😍 Likes Before : {data.get('LikesbeforeCommand','N/A')}\n"
            f"😎 Nickname : {data.get('PlayerNickname','N/A')}\n"
            f"☠️ Level : {data.get('Level','N/A')}\n"
            f"🌍 Region : {data.get('Region','N/A')}\n"
            f"🆔 UID : {uid}\n\n"
            f"☠️ Developer Anurag Singh"
        )
        await msg.edit_text(text)

    except Exception:
        await msg.edit_text("❌ Like API error")

# ================= INFO =================
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if is_spamming(user_id):
        await update.message.reply_text("⏳ Please wait before retry.")
        return

    if not context.args:
        await update.message.reply_text("❌ Use: /info 12345678")
        return

    uid = context.args[0]

    if uid not in uid_joined:
        uid_joined.add(uid)
        await send_join_message(update)
        return

    msg = await update.message.reply_text("⏳ Fetching info...")

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            url = f"https://danger-info-alpha.vercel.app/accinfo?uid={uid}&key=DANGERxINFO"
            r = await client.get(url)
            data = r.json()

        text = "💎 ACCOUNT INFO 💎\n\n"
        for k, v in data.items():
            text += f"{k} : {v}\n"

        text += "\n☠️ Developer Anurag Singh"
        await msg.edit_text(text)

    except Exception:
        await msg.edit_text("❌ Info API error")

# ================= BOT PROTECTION =================
async def protect_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.my_chat_member.chat
    new_status = update.my_chat_member.new_chat_member.status
    added_by = update.effective_user

    if new_status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR):
        if not added_by or added_by.id != OWNER_ID:
            try:
                await context.bot.send_message(
                    chat.id,
                    "❌ You are not allowed to add this bot.\n\n"
                    "📩 Contact Admin to add:\n"
                    "Telegram 👉 @Developer_NovaG\n"
                    "Instagram 👉 @anuragkumarsinghofficial"
                )
            except:
                pass

            await context.bot.leave_chat(chat.id)

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("like", like))
    app.add_handler(CommandHandler("info", info))

    # 🔐 Protection
    app.add_handler(ChatMemberHandler(protect_bot, ChatMemberHandler.MY_CHAT_MEMBER))

    print("🤖 Bot Running (FULLY PROTECTED)")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
