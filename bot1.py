import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import time
from threading import Timer

TOKEN = '7703329384:AAGCP5Nye7AHGqoIrwgEDuG_yYXBuikDvFs'
bot = telebot.TeleBot(TOKEN)

CHANNEL_USERNAME = '@urban_so2'  # Kanalınızın kullanıcı adı
GROUP_USERNAME = '@urbangroups'  # Grubunuzun kullanıcı adı

# Kullanıcıların hatalı doğrulama denemelerini takip etmek için bir sözlük
failed_attempts = {}
block_time = {}

# Kullanıcıların aktifliklerini kontrol etmek için bir sözlük (zamanlayıcı)
user_last_activity = {}

# Kullanıcı mesajlarını saklayacağız (silme işlemi için)
user_messages = {}

# Şifre doğrulama işlemi
passwords = {}

# /start komutuna yanıt verme
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id not in passwords:
        ask_for_password(message)
    else:
        send_verification_buttons(message)

# Şifre sorma işlemi
def ask_for_password(message):
    bot.send_message(message.chat.id, "Lütfen şifrenizi girin:")

# Kullanıcının yazdığı mesajı kontrol etme
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id

    if user_id not in passwords:
        if message.text == "1955":
            passwords[user_id] = "1955"  # Şifre doğruysa kaydet
            bot.send_message(message.chat.id, "Şifre doğru! Doğrulama işlemini başlatıyoruz.")
            send_verification_buttons(message)
        else:
            bot.send_message(message.chat.id, "Şifre Yanlış ❌ Tekrar Deneyiniz.")
    else:
        send_verification_buttons(message)

# Doğrulama butonlarını gösterme
def send_verification_buttons(message):
    keyboard = InlineKeyboardMarkup()
    join_button = InlineKeyboardButton("Kanalı Ziyaret Et", url=f"https://t.me/urban_so2")
    keyboard.add(join_button)
    group_button = InlineKeyboardButton("Gruba Katıl", url=f"https://t.me/urbangroups")
    keyboard.add(group_button)
    verify_button = InlineKeyboardButton("Doğrula ✅", callback_data="verify")
    keyboard.add(verify_button)
    no_verify_button = InlineKeyboardButton("Doğrulama Yapmak İstemiyorum ❌", callback_data="no_verify")
    keyboard.add(no_verify_button)

    bot.send_photo(message.chat.id, "https://i.ibb.co/smxhqYB/photo.jpg", caption="Lütfen kanalımıza katılın ve doğrulama butonuna basın.", reply_markup=keyboard)

# Kullanıcı doğrulama işlemi
@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify_user(call):
    user_id = call.from_user.id
    current_time = time.time()

    # Kullanıcının 5 defa hatalı denemesi olup olmadığını kontrol et
    if user_id in failed_attempts and failed_attempts[user_id] >= 5:
        if current_time - block_time[user_id] < 300:  # 5 dakika (300 saniye)
            # 5 dakika boyunca engellenmişse, kullanıcıya engellendi mesajı gönder
            bot.answer_callback_query(call.id, "5 dakika boyunca doğrulama yapamazsınız.")
            return
        else:
            # Engelleme süresi dolmuşsa, sayacı sıfırla
            failed_attempts[user_id] = 0

    try:
        # Kanal ve grup üyeliklerini kontrol et
        channel_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        group_member = bot.get_chat_member(GROUP_USERNAME, user_id)

        # Kanal ve grup üyeliği kontrolü
        if channel_member.status in ['member', 'administrator', 'creator'] and group_member.status in ['member', 'administrator', 'creator']:
            # Kullanıcı her ikisine de katıldıysa, başarı mesajı gönder
            keyboard = InlineKeyboardMarkup()
            cheat_button = InlineKeyboardButton("Hileyi Kullan", url="https://www.dosya.tc/server2/x211s5/NerestPCFree_0.32.1.exe.html")
            keyboard.add(cheat_button)

            # Fotoğraf URL'sini belirt
            thank_you_photo = 'https://i.ibb.co/cFTGyBz/photo.jpg'  # Başarı mesajı için fotoğraf

            # Teşekkür mesajı ve fotoğraf
            bot.send_photo(call.message.chat.id, thank_you_photo, caption="Kanala katıldığınız için teşekkür ederim! Hoş geldiniz.", reply_markup=keyboard)

            # Başarıyla doğrulama yapıldığında, mesajları silme işlemini başlat
            delete_user_messages(user_id)
        else:
            # Kullanıcı sadece kanala katıldıysa
            if channel_member.status in ['member', 'administrator', 'creator'] and group_member.status not in ['member', 'administrator', 'creator']:
                keyboard = InlineKeyboardMarkup()
                group_button = InlineKeyboardButton("Gruba Katıl", url=f"https://t.me/urbangroups")
                keyboard.add(group_button)

                # Görsel URL'sini belirt
                photo_url = "https://i.ibb.co/PDWRMVC/photo.png"  # Katılmadığınız için görsel

                # "Doğrula ✅" butonunu ekle
                verify_button = InlineKeyboardButton("Doğrula ✅", callback_data="verify")
                keyboard.add(verify_button)

                bot.send_photo(call.message.chat.id, photo_url, caption="Sadece kanala katıldınız, ancak gruba katılmadınız. Lütfen gruba katılın ve tekrar doğrulama butonuna basın.", reply_markup=keyboard)

            # Kullanıcı sadece gruba katıldıysa
            elif group_member.status in ['member', 'administrator', 'creator'] and channel_member.status not in ['member', 'administrator', 'creator']:
                keyboard = InlineKeyboardMarkup()
                channel_button = InlineKeyboardButton("Kanala Katıl", url=f"https://t.me/urban_so2")
                keyboard.add(channel_button)

                # Görsel URL'sini belirt
                photo_url = "https://i.ibb.co/PDWRMVC/photo.png"  # Katılmadığınız için görsel

                # "Doğrula ✅" butonunu ekle
                verify_button = InlineKeyboardButton("Doğrula ✅", callback_data="verify")
                keyboard.add(verify_button)

                bot.send_photo(call.message.chat.id, photo_url, caption="Sadece gruba katıldınız, ancak kanala katılmadınız. Lütfen kanala katılın ve tekrar doğrulama butonuna basın.", reply_markup=keyboard)

            # Kullanıcı her iki yere de katılmamışsa uyarı gönder
            else:
                keyboard = InlineKeyboardMarkup()
                join_button = InlineKeyboardButton("Kanala Katıl", url=f"https://t.me/urban_so2")
                group_button = InlineKeyboardButton("Gruba Katıl", url=f"https://t.me/urbangroups")
                keyboard.add(join_button, group_button)

                # Görsel URL'sini belirt
                photo_url = "https://i.ibb.co/PDWRMVC/photo.png"  # Katılmadığınız için görsel

                # "Doğrula ✅" butonunu ekle
                verify_button = InlineKeyboardButton("Doğrula ✅", callback_data="verify")
                keyboard.add(verify_button)

                # Kullanıcıya her iki yere de katılması gerektiğini belirten mesaj
                bot.send_photo(call.message.chat.id, photo_url, caption="Kanala ve gruba katılmamışsınız. Lütfen her ikisine de katılın ve tekrar doğrulama butonuna basın.", reply_markup=keyboard)

            # Hatalı doğrulama denemesi sayısını artır
            if user_id in failed_attempts:
                failed_attempts[user_id] += 1
            else:
                failed_attempts[user_id] = 1

            # Eğer 5 hatalı denemeye ulaşırsa, kullanıcının 5 dakika boyunca botu kullanması engellenir
            if failed_attempts[user_id] >= 5:
                block_time[user_id] = current_time
                bot.send_message(call.message.chat.id, "5 hatalı denemeden sonra 5 dakika boyunca doğrulama yapamazsınız.")

    except Exception as e:
        bot.send_message(call.message.chat.id, "Bir hata oluştu. Lütfen tekrar deneyin.")
        print(e)

# Doğrulama Yapmak İstemiyorum butonuna tıklama
@bot.callback_query_handler(func=lambda call: call.data == "no_verify")
def no_verify(call):
    bot.send_video(call.message.chat.id, "https://www.dropbox.com/scl/fi/dqsss091ktkhvgq6lwvdm/Adanal-daki-Dalyarak-Market-i-C-stak-Edit.mp4?rlkey=yok95i9iiqbqw8r766hu3esxm&st=zg8pcqe1&raw=1")
    bot.send_message(call.message.chat.id, "Oldu yarram, başka bir isteğin var mı ?", reply_markup=no_verify_keyboard())

def no_verify_keyboard():
    keyboard = InlineKeyboardMarkup()
    apology_button = InlineKeyboardButton("Özür Dilerim ✅", callback_data="verify")
    no_verify_button = InlineKeyboardButton("İstemiyorum ❌", callback_data="final_no_verify")
    keyboard.add(apology_button, no_verify_button)
    return keyboard

@bot.callback_query_handler(func=lambda call: call.data == "final_no_verify")
def final_no_verify(call):
    bot.send_video(call.message.chat.id, "https://www.dropbox.com/scl/fi/wqe913fhc01uwlms2u1uw/Dalyarak-edit.mp4?rlkey=zvrogd304332y91yvgcio4m1m&st=rzp1stdf&raw=1")
    bot.send_message(call.message.chat.id, "SEN HARBİ DALYARAKSIN ☠️", reply_markup=final_apology_keyboard())

def final_apology_keyboard():
    keyboard = InlineKeyboardMarkup()
    apology_button = InlineKeyboardButton("Özür Dilerim Efendim ✅", callback_data="verify")
    keyboard.add(apology_button)
    return keyboard

# Kullanıcı mesajlarını silme (Doğrulama başarılı olursa)
def delete_user_messages(user_id):
    if user_id in user_messages:
        for msg in user_messages[user_id]:
            try:
                bot.delete_message(msg.chat.id, msg.message_id)
            except Exception as e:
                print(f"Mesaj silinirken hata oluştu: {e}")
        del user_messages[user_id]  # Kullanıcıyı mesajlardan sil
    else:
        print("Kullanıcı mesajları zaten silindi.")

# Kullanıcı etkileşimi zaman aşımı
def reset_user_timer(message):
    user_id = message.from_user.id
    user_last_activity[user_id] = time.time()

    # 10 dakika (600 saniye) içinde herhangi bir etkileşim olmazsa, mesajları sil
    Timer(600, check_inactivity, [user_id, message]).start()

def check_inactivity(user_id, message):
    if user_id in user_last_activity:
        last_activity_time = user_last_activity[user_id]
        if time.time() - last_activity_time >= 600:
            # 10 dakika boyunca kullanıcı etkileşimi yoksa, mesajları sil
            delete_user_messages(user_id)
            bot.send_message(message.chat.id, "Yeniden başlatmak için /start komutunu kullanın.")

# Kullanıcı herhangi bir mesaj yazarsa /start komutunu tetikle
@bot.message_handler(func=lambda message: True)
def auto_start(message):
    # Kullanıcı mesaj yazarsa, doğrudan /start komutunu çalıştırıyoruz, ancak herhangi bir mesaj verme yapılmaz
    start(message)

# Botu çalıştırma
bot.polling()
