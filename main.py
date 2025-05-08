import telebot
import csv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive

import os

API_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 1035101385

if not API_TOKEN:
    print("Errore: Token del bot non trovato nelle variabili d'ambiente!")
    exit(1)

try:
    bot = telebot.TeleBot(API_TOKEN)
    bot.get_me() # Verifica che il token sia valido
except Exception as e:
    print(f"Errore nell'inizializzazione del bot: {e}")
    exit(1)

# START
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🔥 Foto e Video Hot", callback_data="foto_video"),
        InlineKeyboardButton("💋 Incontri Privati", callback_data="incontri_privati")
    )
    bot.send_message(message.chat.id,
        "👋 Benvenuto maschio alpha!\nCosa stai cercando oggi? Scegli un'opzione qui sotto:",
        reply_markup=markup
    )

# PRIMA SCELTA: categoria
@bot.callback_query_handler(func=lambda call: call.data in ["foto_video", "incontri_privati"])
def categoria(call):
    if call.data == "foto_video":
        bot.send_message(call.message.chat.id,
            "Hai scelto *Foto e Video Hot* 🔥\nSeleziona cosa ti eccita di più:",
            parse_mode="Markdown"
        )
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📸 Solo Foto", callback_data="contributo_foto"),
            InlineKeyboardButton("🎥 Solo Video", callback_data="contributo_video")
        )
    else:
        bot.send_message(call.message.chat.id,
            "Hai scelto *Incontri Privati* 💋\nCome preferisci incontrarci?",
            parse_mode="Markdown"
        )
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📍 In città", callback_data="contributo_citta"),
            InlineKeyboardButton("🛎️ In hotel", callback_data="contributo_hotel")
        )
    bot.send_message(call.message.chat.id, "👇 Scegli una delle opzioni:", reply_markup=markup)

# CONTRIBUTO (unificato)
@bot.callback_query_handler(func=lambda call: call.data.startswith("contributo_"))
def contributo(call):
    tipo = call.data.replace("contributo_", "")
    titoli = {
        "foto": "📸 Solo Foto",
        "video": "🎥 Solo Video",
        "citta": "📍 Incontri in città",
        "hotel": "🛎️ Incontri in hotel"
    }

    scelta = titoli.get(tipo, "Servizio Speciale")

    bot.send_message(call.message.chat.id,
        f"Sei sempre più vicino ai tuoi caldi e sensuali *{scelta}*… 😈\n\n"
        "Ti devo chiedere solo un piccolo favore, amore mio… puoi donarmi *1 euro*? Sai, tanti omuncoli scrivono e poi spariscono… noi donne vere preferiamo gli uomini veri, quelli che sanno cosa vogliono 😘\n\n"
        "Grazie per il tuo tempo, la tua voglia, e la tua generosità. Ti saprò ripagare con tutta me stessa… 💋\n\n"
        "👉 Paga ora su Ko-fi: [clicca qui](https://ko-fi.com/lisaenaloveyou)",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


keep_alive()

bot.polling()
