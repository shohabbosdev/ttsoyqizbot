from config import token, ttsurl
import telebot
import requests
import urllib3

bot = telebot.TeleBot(token, parse_mode="html")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, text=f"<b>Assalomu alaykum, bu botdan foydalanish uchun matnli xabar yozib qoldiring.</b>\n<i>Tez orada javobni oling</i>")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	try:
		headers = {"Content-Type": "application/json"} 
		data = {"text": message.text}
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

		response = requests.post(ttsurl, headers=headers, json=data, verify=False)
		status_message = bot.reply_to(
			message,
			"✅ <b>Siz yuborgan matn qabul qilindi!!!\nBiroz qayta ishlab sizga 🔉 faylini yuboramiz...</b>"
		)
		if response.status_code==200:
			bot.send_audio(
				message.chat.id, 
				response.content, 
				reply_to_message_id=message.id, 
				caption= f'✍️ <pre>{message.text}</pre>\n\n👉@ttsuzgenbot', 
				title='@ttsuzgenbot', 
				protect_content=True
			)
			bot.delete_message(
		            message.chat.id,
		            status_message.message_id
		        )
		else:
			bot.send_message(f'Kelgan xatolik: {response.status_code}')
	except Exception as e:
		bot.send_message(
			chat_id=message.chat.id,
			text=f"<u>Xatolik sodir bo'ldi:</u>\n<code>{e}</code>"
		)

bot.infinity_polling()
