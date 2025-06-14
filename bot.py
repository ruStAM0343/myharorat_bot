import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8138354482:AAHFGXt49Cth3KBK8teojxH9aW3R0eFwXH8"
THINGSPEAK_CHANNEL_ID = "2973404"
THINGSPEAK_READ_API_KEY = "UB9BRI5LBT0HWAUF"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! /info buyrug‘i orqali sensor ma’lumotlarini olasiz.")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json?results=1&api_key={THINGSPEAK_READ_API_KEY}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()["feeds"][0]
                t = data.get("field1", "Nomaʼlum")
                h = data.get("field2", "Nomaʼlum")
                await update.message.reply_text(f"🌡 Harorat: {t}°C\n💧 Namlik: {h}%")
            else:
                await update.message.reply_text("❌ Ma’lumotlarni olishda xatolik!")
        except Exception as e:
            await update.message.reply_text(f"⚠️ Xatolik: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    print("🤖 Bot ishga tushdi...")
    app.run_polling()
