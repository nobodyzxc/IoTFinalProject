import configparser
import os, json, logging
from pyngrok import ngrok
import telegram, requests
from functools import partial
from getpass import getpass

from IOTF.comm import control_gate, show_LCD

import serial
from time import sleep

from reg_plate_gen import gen_plate

from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters, Updater, StringCommandHandler, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram import Location, InlineKeyboardMarkup, InlineKeyboardButton

import pexpect

def decrypt_token(fn):
    global phrase
    get = pexpect.spawn(f'openssl rsautl -inkey meta/key.txt -decrypt -in {fn}')
    get.expect("Enter pass phrase for meta/key.txt:")
    if not phrase: phrase = getpass('Enter pass phrase for meta/key.txt:')
    get.sendline(phrase)
    get.expect(pexpect.EOF)
    return get.before.decode('utf-8').strip()

phrase = None
ADMIN_ID = int(decrypt_token(os.path.join('meta', 'encrypted.admin.id')))

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
tgtoken = decrypt_token(os.path.join('meta', 'encrypted.telegram.token'))
bot = telegram.Bot(token=tgtoken)
ino = serial.Serial("/dev/ttyACM0",9600)

def tg_report_other(message):
    try:
        bot.forwardMessage(
            chat_id=ADMIN_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id)
    except Exception as e:
        bot.sendMessage(
            chat_id=ADMIN_ID,
            text="error from other {}".format(e))


def register(bot, update, args):

    emoji = {
        '⭕': "ok" + " " + str(update.message.chat.id),
        '❌': "no" + " " + str(update.message.chat.id)
    }

    bot.sendMessage(chat_id=ADMIN_ID,
                    text="📍 同意她/他 @{} 成為使用者?".format(str(update.message.from_user.username)),
                    reply_markup = InlineKeyboardMarkup([[
                            InlineKeyboardButton(emoji, callback_data = hand) for emoji, hand in emoji.items()
                        ]]),
                    )

def play(bot, update):
    try:
        result = update.callback_query.data.split()
        mine, chat, plate, *_ = result

        if mine == 'ok':
            update.callback_query.edit_message_text('已開門')
            bot.sendMessage(
                chat_id=int(chat),
                text="大門已經開啟，如有問題請聯繫管理員")
            show_LCD(ino, 1, plate)
            sleep(3)
            control_gate(ino, 1)
            sleep(15)
            control_gate(ino, 0)
            sleep(3)
            show_LCD(ino, -1, plate)

        else:
            update.callback_query.edit_message_text('忽略此請求')
            bot.sendMessage(
                chat_id=int(chat),
                text="大門已經開啟，如有問題請聯繫管理員")
            show_LCD(ino, 0, '')
    except Exception as e:
        print(e)


def chatid(bot, update):
    update.message.reply_text("❓ 您的Chat ID為 {}\n使用 /register 指令註冊".format(update.message.chat.id))

def listRegistration(bot, update):
    data = json.load(open('data.json'))
    print(update.message.chat.id, data)
    plates = data.get(str(update.message.chat.id), [])
    if plates:
        update.message.reply_text('\n'.join(plates))
    else:
        update.message.reply_text("尚無車牌，請先註冊")

def addRegistration(bot, update):
    new = update.message.text.split()[1]
    data = json.load(open('data.json'))
    plates = data.get(update.message.chat.id, [])
    plates += [new]
    data[update.message.chat.id] = plates
    with open('data.json', 'w') as output:
        json.dump(data, output)

    plate = gen_plate(new)
    bot.send_photo(update.message.chat.id, photo=open(plate, 'rb'))
    update.message.reply_text(f'{new} 已加入')

def start(bot, update):
    update.message.reply_text("❓ 您的Chat ID為 {}\n使用 /register 指令註冊".format(update.message.chat.id))

def add(bot, update, args):
    if ADMIN_ID == update.message.chat.id:
        isUser = False
        with open('./userlist.txt', 'r') as the_file:
            for x in the_file:
                if int(x) == (int)(args[0]):
                    isUser = True
        if isUser == True:
            update.message.reply_text("✉ 此用戶已在用戶名單內")
            return
        else:
            with open('./userlist.txt', 'a') as the_file:
                the_file.write('{}\n'.format(int(args[0])))
        update.message.reply_text("🌷成功將用戶id {} 加入".format(int(args[0])))
    else:
        update.message.reply_text("❌您必須是管理者才可以使用add user的功能")

@app.route('/access', methods=['POST'])
def access_handler():
    if request.method == "POST":
        if 'user' in request.form and 'plate' in request.form:
            user, plate = request.form['user'], request.form['plate']
            emoji = {
                '⭕ 開門': "ok {} {}".format(user, plate),
                '❌ 不開': "no {} {}".format(user, plate)
            }

            bot.sendMessage(chat_id=user,
                    text="辨識到車牌 '{}': 是否開門？".format(plate),
                    reply_markup = InlineKeyboardMarkup(
                        [[ InlineKeyboardButton(emoji, callback_data = hand)
                            for emoji, hand in emoji.items()
                        ]])
                    )
            return 'ok'
    return 'failed'

@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
#dispatcher.add_handler(CommandHandler('register', register, pass_args=True))
dispatcher.add_handler(CommandHandler('chatid', chatid))
dispatcher.add_handler(CommandHandler('list', listRegistration))
dispatcher.add_handler(CommandHandler('add', addRegistration))
#dispatcher.add_handler(CommandHandler('add', add, pass_args=True))
dispatcher.add_handler(CommandHandler('start', start))
#dispatcher.add_handler(MessageHandler(Filters.document.pdf, reply_handler))
#dispatcher.add_handler(MessageHandler(Filters.document.jpg, reply_handler))
#dispatcher.add_handler(MessageHandler(Filters.forwarded, reply_handler))
dispatcher.add_handler(CallbackQueryHandler(play))


def main():
    print("============ Setup ngrok ======================")
    ngrok.set_auth_token(decrypt_token(os.path.join('meta', 'encrypted.ngrok.token')))
    hook_url = ngrok.connect(8501).replace("http", "https")
    print("Hook url: " + hook_url)

    print("============ Webhook set ======================")

    requests.get("https://api.telegram.org/bot" + tgtoken + "/setWebhook?url=" + hook_url + "/hook")

    print("============ App run ==========================")
    port = int(os.environ.get("PORT", 8501))

    app.run(debug=False, port=port)
    #ngrok.disconnect(hook_url)

if __name__ == "__main__":
    main()
