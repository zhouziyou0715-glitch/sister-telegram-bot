import os
import anthropic
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

async def start(update: Update, context):
    await update.message.reply_text('姐姐在这里！')

async def chat(update: Update, context):
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": update.message.text}]
        )
        await update.message.reply_text(msg.content[0].text)
    except:
        await update.message.reply_text("姐姐暂时有点问题~")

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
