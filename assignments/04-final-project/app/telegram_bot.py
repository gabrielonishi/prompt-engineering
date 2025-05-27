#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sqlite3
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackContext
)

# Import other modules
from sentiment_analyzer import analyze_sentiment
from database_setup import connect_db, create_tables, DATABASE_FILE

# Load environment variables from .env file
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Needed by sentiment_analyzer

# Ensure the database file path is correct relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DATABASE_FILE)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define conversation states
ASK_MOOD_SCALE, ASK_MOOD_DESCRIPTION = range(2)

# --- Database Interaction Functions ---
def get_or_create_patient(telegram_id: int) -> int | None:
    """Gets patient ID from DB based on telegram_id, creates if not exists."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id FROM patients WHERE telegram_id = ?", (telegram_id,))
        result = cursor.fetchone()
        if result:
            logger.info(f"Found existing patient_id: {result[0]} for telegram_id: {telegram_id}")
            return result[0]
        else:
            # Create new patient (minimal data for MVP)
            cursor.execute("INSERT INTO patients (telegram_id) VALUES (?)", (telegram_id,))
            conn.commit()
            new_patient_id = cursor.lastrowid
            logger.info(f"Created new patient_id: {new_patient_id} for telegram_id: {telegram_id}")
            return new_patient_id
    except sqlite3.Error as e:
        logger.error(f"Database error in get_or_create_patient: {e}")
        # Handle error appropriately, maybe raise it or return None/error code
        return -1 # Indicate error
    finally:
        if conn:
            conn.close()

def save_mood_entry(patient_id: int, mood_scale: int, mood_description: str, sentiment: str):
    """Saves the mood entry to the database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO mood_history (patient_id, mood_scale, mood_description, sentiment_analysis)
            VALUES (?, ?, ?, ?)
        """, (patient_id, mood_scale, mood_description, sentiment))
        conn.commit()
        logger.info(f"Saved mood entry for patient_id {patient_id}")
    except sqlite3.Error as e:
        logger.error(f"Database error in save_mood_entry: {e}")
        # Handle error appropriately
    finally:
        if conn:
            conn.close()

# --- Bot Command Handlers ---
async def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks for the mood scale."""
    if update.message is None or update.message.from_user is None:
        logger.error("Update or message is None, cannot proceed.")
        return ConversationHandler.END
    
    user = update.message.from_user
    logger.info(f"User {user.first_name} ({user.id}) started the conversation.")

    # Get or create patient record
    patient_id = get_or_create_patient(user.id)
    if patient_id == -1:
        await update.message.reply_text("Desculpe, ocorreu um erro ao acessar seus dados. Tente novamente mais tarde.")
        return ConversationHandler.END
    
    if context is None or context.user_data is None:
        logger.error("Context is None, cannot store patient_id.")
        await update.message.reply_text("Desculpe, ocorreu um erro ao iniciar a conversa. Tente novamente mais tarde.")
        return ConversationHandler.END

    context.user_data['patient_id'] = patient_id # Store patient_id for later use

    reply_keyboard = [['1', '2', '3', '4', '5']]
    await update.message.reply_text(
        "Olá! Como você está se sentindo hoje em uma escala de 1 (muito mal) a 5 (muito bem)?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return ASK_MOOD_SCALE

async def ask_mood_description(update: Update, context: CallbackContext) -> int:
    """Stores the mood scale and asks for the description."""        

    if update.message is None or update.message.from_user is None:
        logger.error("Update or message is None, cannot proceed.")
        return ConversationHandler.END

    user = update.message.from_user
    mood_scale_text = update.message.text
    logger.info(f"Mood scale from {user.first_name}: {mood_scale_text}")

    # Basic validation
    if mood_scale_text not in ['1', '2', '3', '4', '5']:
        reply_keyboard = [['1', '2', '3', '4', '5']]
        await update.message.reply_text(
            "Por favor, escolha um número de 1 a 5.",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
        return ASK_MOOD_SCALE # Stay in the same state

    if context.user_data is None:
        context.user_data = {}
    context.user_data['mood_scale'] = int(mood_scale_text)

    await update.message.reply_text(
        "Obrigado. Poderia descrever brevemente como foi o seu dia ou como está se sentindo?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ASK_MOOD_DESCRIPTION

async def process_description_and_end(update: Update, context: CallbackContext) -> int:
    """Stores the description, performs analysis, saves data, and ends."""
    if update.message is None or update.message.from_user is None:
        logger.error("Update or message is None, cannot proceed.")
        return ConversationHandler.END

    user = update.message.from_user
    mood_description = update.message.text
    if context.user_data is None:
        context.user_data = {}
    mood_scale = context.user_data.get('mood_scale')
    patient_id = context.user_data.get('patient_id')

    if mood_scale is None or patient_id is None:
        logger.error(f"Missing mood_scale or patient_id for user {user.id}")
        await update.message.reply_text("Ocorreu um erro ao processar seus dados. Por favor, comece novamente com /start.")
        context.user_data.clear()
        return ConversationHandler.END

    if mood_description is None:
        logger.error("Mood description is None.")
        await update.message.reply_text("Não foi possível entender sua mensagem. Por favor, tente novamente.")
        return ConversationHandler.END

    logger.info(f"Mood description from {user.first_name}: {mood_description}")

    # --- Integration Point ---
    # 1. Analyze Sentiment (Using imported function)
    logger.info("Calling sentiment analyzer...")
    sentiment = analyze_sentiment(mood_description)
    logger.info(f"Sentiment analysis result: {sentiment}")

    # 2. Save to Database (Using imported function)
    logger.info("Saving data to database...")
    save_mood_entry(patient_id, mood_scale, mood_description, sentiment)
    # --- End Integration Point ---

    await update.message.reply_text(
        "Obrigado por compartilhar! Suas informações foram registradas. Tenha um bom dia!"
    )

    # Clear user data for this conversation
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    if update.message is not None and update.message.from_user is not None:
        user = update.message.from_user
        logger.info(f"User {user.first_name} canceled the conversation.")
        await update.message.reply_text(
            "Ok, cancelado. Se precisar, pode começar de novo com /start.", reply_markup=ReplyKeyboardRemove()
        )
    if context.user_data is not None:
        context.user_data.clear()
    return ConversationHandler.END

async def error_handler(update: object, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.error(f'Update "{update}" caused error "{context.error}"')

def main() -> None:
    """Run the bot."""
    # --- Database Setup ---
    # Ensure the database and tables exist before starting the bot
    logger.info(f"Checking/Creating database tables at: {DB_PATH}")
    # Need to temporarily change dir for create_tables if it relies on relative path
    original_dir = os.getcwd()
    os.chdir(BASE_DIR)
    try:
        create_tables() # Function from database_setup.py
    finally:
        os.chdir(original_dir) # Change back to original directory
    logger.info("Database setup complete.")
    # --- End Database Setup ---

    from telegram.ext import (
        ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters
    )
    if not TELEGRAM_TOKEN:
        raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables. Please set it in the .env file.")
    if not GOOGLE_API_KEY:
        # Allow running without Google API key for testing basic flow, sentiment will be placeholder
        print("Warning: GOOGLE_API_KEY environment variable not found. Sentiment analysis will use placeholders.")
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_MOOD_SCALE: [MessageHandler(filters.Regex('^[1-5]$'), ask_mood_description)],
            ASK_MOOD_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_description_and_end)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        # Optional: Add a timeout
        # conversation_timeout=300 # 5 minutes
    )

    application.add_handler(conv_handler)

    # Log all errors
    application.add_error_handler(error_handler)

    # Start the Bot
    logger.info("Bot started polling...")
    application.run_polling()

if __name__ == '__main__':
    main()

