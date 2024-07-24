import os
import telebot
from googletrans import Translator

def main():

	BOT_TOKEN = os.getenv("BOT_TOKEN")
	bot = telebot.TeleBot(BOT_TOKEN)
	translator = Translator()

	auto_translation_sources = []
	auto_translation_dest = ["English"]

	@bot.message_handler(commands=['start', 'help'])
	def send_welcome(message):
		bot.reply_to(message, "AzaTranslatorBot welcomes you. This bot will translate your messages to anyone of the available languages. Run /langs to see te available languages, then run /<language> to start the translating process.")

	@bot.message_handler(commands=['langs'])
	def command_langs(message):
		bot.reply_to(message, "Available languages:\n- English\n- Italian\n- Bengali\n\nExample: if you want to translate some text from any language to English, run the command /English. You will then be prompted to send your message in a foreign language and the bot will translate it for you. For all the other languages, just replace /English with any one of the other available languages.")

	@bot.message_handler(commands=['English', 'Italian', 'Bengali'])
	def command_select_lang(message):
		chosen_lang = message.text[1:]
		text = f"Now send the message in foreign language you want to translate to {chosen_lang}"
		to_translate = bot.send_message(message.chat.id, text, parse_mode="Markdown")
		bot.register_next_step_handler(to_translate, translate, chosen_lang)

	@bot.message_handler(commands=['autoFromEnglish', 'autoFromItalian', 'autoFromBengali'])
	def command_set_auto_translation_from(message):
		chosen_lang = find_lang(message.text)
		auto_translation_sources.append(match_lang_code(chosen_lang))
		bot.reply_to(message, f"Automatic translation has been set for {chosen_lang} language. Remember to set also the destination language (currently set to {auto_translation_dest[0]}) using the command /autoTo<language>.")

	@bot.message_handler(commands=['autoToEnglish', 'autoToItalian', 'autoToBengali'])
	def commanf_set_auto_translation_to(message):
		chosen_lang = find_lang(message.text)
		auto_translation_dest[0] = chosen_lang
		bot.reply_to(message, f"Destination language for automatic translation has been set to {chosen_lang}")

	@bot.message_handler(func=lambda message: True)	
	def auto_translate(message):
		if auto_translation_sources and translator.detect(message.text).lang in auto_translation_sources:
			dest_lang_code = match_lang_code(auto_translation_dest[0])
			translated_msg = translator.translate(message.text, dest=dest_lang_code).text
			bot.reply_to(message, translated_msg)
		
	def match_lang_code(lang_name):
		lang_code = None
		if lang_name == "English":
			lang_code = "en"
		elif lang_name == "Italian":
			lang_code = "it"
		elif lang_name == "Bengali":
			lang_code = "bn"
		
		return lang_code

	def find_lang(text):
		if 'English' in text:
			return 'English'
		elif 'Italian' in text:
			return 'Italian'
		elif 'Bengali' in text:
			return 'Bengali'

	def translate(text_to_translate, dest_lang):
		dest_lang_code = match_lang_code(dest_lang)
		translated_msg = translator.translate(text_to_translate.text, dest=dest_lang_code).text
		bot.send_message(text_to_translate.chat.id, translated_msg, parse_mode="Markdown")

	bot.infinity_polling()

if __name__ == '__main__':
	main()