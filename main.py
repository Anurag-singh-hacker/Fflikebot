from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import httpx
import asyncio
import time

BOT_TOKEN = "8570487817:AAHtul4Nw2tVxPBhbDWMNKfP_1nUM5KJ_q0"

# 🔗 Channel Links
CHANNEL_LINK_1 = "https://t.me/+4lV7uE_l89w4NDZl"
CHANNEL_LINK_2 = "https://t.me/+CAPGfkPG_UQ4Njll"
CHANNEL_LINK_3 = "https://t.me/goodlikemee"
# 🔒 Anti Spam
cooldown = {}
COOLDOWN_TIME = 8

# 🧠 UID Memory (First time join show)
uid_joined = set()


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome\n\n"
        "/like 12345678\n"
        "/info 12345678\n\n"
        "☠️ Developer Anurag Singh"
    )


# ---------------- SPAM CHECK ----------------
def is_spamming(user_id):
    now = time.time()
    if user_id in cooldown:
        if now - cooldown[user_id] < COOLDOWN_TIME:
            return True
    cooldown[user_id] = now
    return False


# ---------------- JOIN BUTTON MESSAGE ----------------
async def send_join_message(update: Update):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_LINK_1)],
        [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_LINK_2)],
           [InlineKeyboardButton("📢 Join Channel 3", url=CHANNEL_LINK_3)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 Premium Access Required\n\n"
        "Join All Channels First.\n"
        "After Joining, Send Same Command Again.",
        reply_markup=reply_markup
    )


# ---------------- LIKE ----------------
async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if is_spamming(user_id):
        await update.message.reply_text("⏳ Please wait 30 second And try again.")
        return

    if not context.args:
        await update.message.reply_text("❌ Use: /like 12345678")
        return

    uid = context.args[0]

    # First time UID → show join buttons
    if uid not in uid_joined:
        uid_joined.add(uid)
        await send_join_message(update)
        return

    # Second time → run API
    msg = await update.message.reply_text(
        "wait..... 😊\n🤩 By Anurag Singh ...."
    )

    await asyncio.sleep(2)

    async with httpx.AsyncClient(timeout=20) as client:
        try:
            url = f"https://mukesh-ult-like.vercel.app/like?uid={uid}&region=ind&key=UDIT"
            r = await client.get(url)
            data = r.json()

            text = (
                f"🥰 Likes Given By API : {data.get('LikesGivenByAPI', 'N/A')}\n"
                f"🤗 Likes After Command : {data.get('LikesafterCommand', 'N/A')}\n"
                f"😍 Likes Before Command : {data.get('LikesbeforeCommand', 'N/A')}\n"
                f"😎 Player Nickname : {data.get('PlayerNickname', 'N/A')}\n"
                f"☠️ Level : {data.get('Level', 'N/A')}\n"
                f"💀 Region : {data.get('Region', 'N/A')}\n"
                f"👽 UID : {data.get('UID', uid)}\n"
                f"status : {data.get('status', 'N/A')}\n\n"
                f"☠️ Developer Anurag Singh"
            )

            await msg.edit_text(text)

        except:
            await msg.edit_text("❌ Like API error")


# ---------------- INFO ----------------
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if is_spamming(user_id):
        await update.message.reply_text("⏳ Please wait before using again.")
        return

    if not context.args:
        await update.message.reply_text("❌ Use: /info 12345678")
        return

    uid = context.args[0]

    # First time UID → show join buttons
    if uid not in uid_joined:
        uid_joined.add(uid)
        await send_join_message(update)
        return

    msg = await update.message.reply_text(
        "wait..... 😊\n🤩 By Anurag Singh ...."
    )

    await asyncio.sleep(2)

    async with httpx.AsyncClient(timeout=20) as client:
        try:
            url = f"http://danger-info-alpha.vercel.app/accinfo?uid={uid}&key=DANGERxINFO"
            r = await client.get(url)

            if r.status_code != 200:
                await msg.edit_text("❌ Info API error")
                return

            data = r.json()

            text = "💎 ACCOUNT INFORMATION 💎\n\n"
            for k, v in data.items():
                text += f"├─ {k} : {v}\n"

            text += "\n☠️ Developer Anurag Singh"

            await msg.edit_text(text)

        except:
            await msg.edit_text("❌ Info API error")


# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("like", like))
    app.add_handler(CommandHandler("info", info))

    print("🤖 Bot Running (Button Join Mode)...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
