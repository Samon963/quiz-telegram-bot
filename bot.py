import os
import json
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

nest_asyncio.apply()

# # System Environment Variable se token read karega (Secure Way)
BOT_TOKEN = os.environ.get("8682638608:AAGuaIGzYJVMkplryDfHZklky8NaKBsNMUk")


SAMPLE_JSON = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct_option_id": 2,
        "explanation": "Paris is the capital of France."
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "correct_option_id": 1,
        "explanation": "Mars appears red due to iron oxide."
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name

    welcome_text = (
        f"👋 Hello {user_name} 🌟\n\n"
        "🎯 *MCQ Quiz Bot* - Send JSON to create anonymous quiz polls!\n\n"
        "✨ *How it works:*\n"
        "1️⃣ Copy the JSON template below\n"
        "2️⃣Give your questions to  CHATGPT\n"
        "3️⃣ Send back → Get instant anonymous quiz polls! 🚀"
        "🎉Made By @Samon963"
    )

    await update.message.reply_text(welcome_text, parse_mode="Markdown")
    await update.message.reply_text(f"json\n{json.dumps(SAMPLE_JSON, indent=2)}\n", parse_mode="Markdown")

async def process_quiz_data(update: Update, context: ContextTypes.DEFAULT_TYPE, raw_text: str):
    try:
        data = json.loads(raw_text)
        if isinstance(data, dict):
            data = [data]

        for item in data:
            question_text = str(item.get("question", "")).strip()
            explanation_text = str(item.get("explanation", "")).strip()
            options = item.get("options", [])

            correct_id = int(
    item.get("correct_option_id", item.get("correctoptionid", 0))
)            # Limit Check: Truncate explanation to 200 chars max
            if len(explanation_text) > 200:
                explanation_text = explanation_text[:197] + "..."

            # Limit Check: Handle long questions over 300 chars
            if len(question_text) > 300:
                await update.message.reply_text(
                    f"📖 Question Context:\n\n{question_text}",
                    parse_mode="Markdown"
                )
                poll_question = "Select the correct option based on the text above:"
            else:
                poll_question = question_text

            # Send Native Quiz Poll (Anonymous = True)
            await update.message.reply_poll(
                question=poll_question,
                options=options,
                type="quiz",
                correct_option_id=correct_id,
                explanation=explanation_text,
                is_anonymous=True
            )
            await asyncio.sleep(0.5)

    except json.JSONDecodeError:
        await update.message.reply_text("❌ Invalid JSON format. Please send a valid JSON text.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error creating quiz: {str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await process_quiz_data(update, context, update.message.text)

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is live! Go test it on Telegram.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
