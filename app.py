import telebot
from telebot import util
from config import token
from braille_converter import BrailleConverter
from jpgtotext import jpgtotext
from texttospeech import image_detect
from io import BytesIO
from time import sleep
from keep_alive import keep_alive

keep_alive()


MAX_CAPTION_LENGTH = 1024
MAX_MESSAGE_LENGTH = 4096
CHUNK_SIZE = 1000  # Reduced for safety margin

class TTSBot:
    def __init__(self):
        self.bot = telebot.TeleBot(token, parse_mode="html")
        self.convertor = BrailleConverter()
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message, 
                "✋ <b>Assalomu alaykum, bu botdan foydalanish uchun matnli xabar yozib qoldiring.</b>\n"
                "⚡️ <i>Tez orada javobni oling</i> 🆗\n\n"
                "▶️ @ttsuzgenbot"
            )

        @self.bot.message_handler(content_types=['photo'])
        def handle_photo(message):
            try:
                state_message = self.send_processing_sticker(message.chat.id)
                result_text = self.process_photo(message)
                self.send_text_result(message, result_text)
                self.send_audio_result(message, result_text)
                self.bot.delete_message(message.chat.id, state_message.id)
            except Exception as e:
                self.handle_error(message, e)

        @self.bot.message_handler(func=lambda message: True)
        def handle_text(message):
            try:
                chunks = self.split_text(message.text)
                for chunk in chunks:
                    self.send_text_audio(message, chunk)
            except Exception as e:
                self.handle_error(message, e)

    def send_processing_sticker(self, chat_id):
        return self.bot.send_sticker(chat_id, telebot.types.InputFile('soundsticker.tgs'))

    def process_photo(self, message):
        photo = message.photo[-1]
        file_info = self.bot.get_file(photo.file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)
        image_stream = BytesIO(downloaded_file)
        image_stream.name = 'temp_image.jpg'
        return image_detect(image_stream)

    def split_text(self, text):
        if len(text) <= CHUNK_SIZE:
            return [text]
        return [text[i:i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]

    def send_text_result(self, message, text):
        chunks = self.split_text(text)
        for chunk in chunks:
            caption = (
                "📝 <b>Natija:</b>\n"
                f"<code>{chunk[:MAX_CAPTION_LENGTH-100]}</code>"
                "\n👉 @ttsuzgenbot"
            )
            self.bot.send_message(message.chat.id, caption)

    def send_audio_result(self, message, text):
        chunks = self.split_text(text)
        for chunk in chunks:
            state_message = self.send_processing_sticker(message.chat.id)
            try:
                self.bot.send_audio(
                    message.chat.id,
                    audio=texttospeech(chunk),
                    caption="🎧 <b>Audio</b>",
                    title='@ttsuzgenbot',
                    performer='Telegram bot',
                    protect_content=True,
                    thumb=telebot.types.InputFile('images.jpg')
                )
            finally:
                self.bot.delete_message(message.chat.id, state_message.id)

    def send_text_audio(self, message, text):
        state_message = self.send_processing_sticker(message.chat.id)
        try:
            braille_text = self.convertor.convert_chars_to_braille(text)
            caption = (
                "✍️ <b>Matn:</b>\n"
                f"<code>{text[:300]}...</code>\n\n"
                "✏️ <b>Brayl:</b>\n"
                f"<code>{braille_text[:300]}...</code>\n\n"
                "👉 @ttsuzgenbot"
            )
            self.bot.send_audio(
                message.chat.id,
                audio=texttospeech(text),
                caption=caption,
                reply_to_message_id=message.id,
                title='@ttsuzgenbot',
                performer='Telegram bot',
                protect_content=True,
                thumb=telebot.types.InputFile('images.jpg')
            )
        finally:
            self.bot.delete_message(message.chat.id, state_message.id)

    def handle_error(self, message, error):
        error_message = "Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring."
        self.bot.send_message(message.chat.id, error_message)
        print(f"Error: {str(error)}")

    def run(self):
        self.bot.infinity_polling()

if __name__ == "__main__":
    bot = TTSBot()
    bot.run()
