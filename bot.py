import telebot
from telebot import types
import mysql.connector
import textwrap

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='magang')

sql = mydb.cursor()

api = '6790229880:AAHI7AZngMlySaYuyamO8Vd8K32dlo_9In0'
bot = telebot.TeleBot(api)

@bot.message_handler(commands=['start'])
def action_start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('/tafsir')
    item2 = types.KeyboardButton('/tafsir_alquran [id_ayat]')
    markup.add(item1, item2)
    bot.reply_to(message, 'Selamat Datang di Telegbot Tafsir Al-misbah', reply_markup=markup)

@bot.message_handler(commands=['tafsir'])
def tafsir(message):
    sql.execute("SELECT name FROM tafsirs WHERE id = 6")
    hasil_sql = sql.fetchall()
    bot.reply_to(message, hasil_sql)
    

@bot.message_handler(commands=['tafsir_alquran'])
def tafsir_alquran(message):
    texts = message.text.split(' ')
    if len(texts) < 2 or not texts[1].isdigit():
        bot.reply_to(message, "Maaf, format perintah tidak valid. Silakan gunakan perintah /tafsir_alquran [id_ayat]")
        return
    
    id = texts[1]
    sql.execute(f"SELECT verses.text_indopak, verse_tafsirs.text FROM verses, verse_tafsirs WHERE verse_tafsirs.id_tafsir = 6 AND verses.id = {id} AND verse_tafsirs.id_verse = {id}")
    hasil_sql = sql.fetchall()
    pesan_balasan = ''
    for x in hasil_sql:
        ayat = f"Ayat:\n{x[0]}"
        tafsir = f"Tafsir:\n{textwrap.fill(x[1], width=50)}"  # Sesuaikan lebar dengan preferensi Anda
        pesan_balasan += f"{ayat}\n\n{tafsir}\n\n"  # Menambahkan baris kosong antara ayat dan tafsir
    bot.reply_to(message, pesan_balasan)

@bot.message_handler(func=lambda message: True)
def handle_unknown_commands(message):
    bot.reply_to(message, "Maaf, kode tidak dikenal. Silakan gunakan perintah yang valid.")

print('bot start running')
bot.polling()
