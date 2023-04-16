import requests
import io
from dadata             import Dadata
from telebot            import TeleBot as tb
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage   import PDFPage

tgbot_token  = '1785558469:AAF3nOKfNTgDUcZvY-RLVN-7F8Bs9nsYTx4'
dadata_token = "d784903f877eba7baf20125f67c1f37a87c4e038"

dadata = Dadata(dadata_token)
bot    = tb(tgbot_token)

@bot.message_handler(commands=['start'])
def func(message):
    user_id = message.from_user.id
    bot.send_message(user_id, user_id)

@bot.message_handler(regexp='[AaАа][HnНн][EeЕеИиIi][KkCcКк][ДдDd][ОоOo][ТтTtDdДд]')
def anny_k_dot(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Мой создатель - опытный \nЯ-же бот - подопытный\nТы - приёмный')

@bot.message_handler(func=lambda msg: len(msg.text) == 10 and msg.text.isdigit())
def x(message):
    user_id = message.from_user.id
    get_vypiska(message.text)
    content = parse_vypiska()
    status = is_okay(content)
    if status is True:
        bot.send_message(user_id, 'Всё окей. Доверяем =)')
    elif status is False:
        bot.send_message(user_id, 'Есть недостоверные сведения =|')
    else:
        bot.send_message(user_id, 'Не могу считать отчётность =(')

def get_vypiska(inn):
    result = dadata.find_by_id("party", inn)
    ogrn = result[0]['data']['ogrn']
    file_link = f'https://выставить-счет.рф/vipiska-egrul/{ogrn}.pdf'
    r = requests.get(file_link)
    with open('res.pdf', 'wb') as file:
        file.write(r.content)

def parse_vypiska():
    pdf_path = 'res.pdf'
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text.replace(' ', '').lower()
    else:
        return 'HHH'

def is_okay(content):
    if 'недостоверны' in content:
        return False
    elif content == 'HHH':
        return None
    else:
        return True

bot.polling(none_stop=True)