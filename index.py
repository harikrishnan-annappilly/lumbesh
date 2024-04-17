import telebot
from model import Base, engine, Session, CodeModel
from friend_code import get_friend_codes
from bot_configs import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)
Base.metadata.create_all(engine)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


def get_codes(message_id, type=1):
    session = Session()
    bot.send_message(message_id, f'Fetching 🔍')

    fetched_codes = get_friend_codes(type)
    sent_codes = [
        code.code
        for code in session.query(CodeModel)
        .filter(CodeModel.message_id == message_id, CodeModel.code.in_(fetched_codes))
        .all()
    ]
    new_codes = list(set(fetched_codes) - set(sent_codes))

    if not len(new_codes):
        session.close()
        bot.send_message(message_id, f'No new friend codes are present 😔')
        return

    for index, code_id in enumerate(new_codes):
        bot.send_message(message_id, f'{index+1}) `{code_id}`', parse_mode='Markdown')
        if (index + 1) % 5 == 0:
            bot.send_message(message_id, f'-')

        code = CodeModel(message_id, code_id)
        session.add(code)
        session.commit()

    session.close()
    bot.send_message(message_id, f'Done ✅')


@bot.message_handler(commands=['get_friend_code_set_1'])
def send_welcome(message):
    get_codes(message.chat.id, type=1)


@bot.message_handler(commands=['get_friend_code_set_2'])
def send_welcome(message):
    get_codes(message.chat.id, type=2)


bot.set_my_commands(
    [
        telebot.types.BotCommand("/start", "main menu"),
        telebot.types.BotCommand("/get_friend_code_set_1", "gives max 20 friend code"),
        telebot.types.BotCommand("/get_friend_code_set_2", "gives max 30 friend code"),
    ]
)

bot.infinity_polling()
