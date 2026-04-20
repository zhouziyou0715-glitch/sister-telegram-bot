import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import anthropic

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def start(update, context):
    update.message.reply_text('姐姐在这里！随时可以和我聊天~')

def handle_message(update, context):
    user_message = update.message.text
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": user_message}]
        )
        
        reply = message.content[0].text
        update.message.reply_text(reply)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        update.message.reply_text("姐姐暂时遇到了一点问题，稍后再试试吧~")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
