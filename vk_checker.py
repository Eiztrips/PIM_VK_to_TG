import vk_api, requests
from vk_api.bot_longpoll import VkBotLongPoll
from config import vk_c, tg_c

vk_session = vk_api.VkApi(token = vk_c['token'])
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, vk_c['group_id'])

telegram_bot_token = tg_c['tg_tkn']
telegram_chat_id = tg_c['tg_chat_id']

def handle_text(user, text):
    requests.post(
                f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
                data={
                     "chat_id": telegram_chat_id,
                     "text": f"<i>{user}</i>\n\n<b>{text}</b>",
                     "parse_mode": "HTML"
                     })

def handle_user(user):
    requests.post(
                f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
                data={
                     "chat_id": telegram_chat_id,
                     "text": f"<i>{user}</i>",
                     "parse_mode": "HTML"
                     })

def handle_photo(message): #Доработать обработку более 2 фотографий
    attachments = message['attachments']
    media_group = []

    for attachment in attachments:
        if attachment['type'] == 'photo':
            image = attachment['photo']['orig_photo']['url']
            media_group.append(image)

    for img in media_group:
        requests.post(
            f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto",
            data={
                 'chat_id': telegram_chat_id,
                 'photo': img
                 })

def handle_video(message): #Доработать передачу видео
    attachments = message['attachments']

    for attachment in attachments:
        if attachment['type'] == 'video':
             title = attachment['video']['title']
             requests.post(
                f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
                data={
                     "chat_id": telegram_chat_id,
                     "text": f"<b>Видеозапись: {title}</b>",
                     "parse_mode": "HTML"
                     })

def handle_audio_message(message):
    attachments = message['attachments']

    for attachment in attachments:
        if attachment['type'] == 'audio_message':
            audio_message = attachment['audio_message']
            audio_url = audio_message['link_mp3']
            audio_data = requests.get(audio_url).content
            requests.post(
                f"https://api.telegram.org/bot{telegram_bot_token}/sendVoice",
                files={"voice": audio_data},
                data={"chat_id": telegram_chat_id}
    )

def handle_audio(message): #Доработать передачу аудио
    attachments = message['attachments']

    for attachment in attachments:
        if attachment['type'] == 'audio':
            author = attachment['audio']['artist']
            title = attachment['audio']['title']
            requests.post(
               f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
               data={
                    "chat_id": telegram_chat_id,
                    "text": f"<b>Аудиозапись: {author} - {title}</b>",
                    "parse_mode": "HTML"
                    })

def handle_doc(message):
    attachments = message['attachments']

    for attachment in attachments:
         if attachment['type'] == 'doc':
            doc_url = attachment['doc']['url']
            doc_title = attachment['doc']['title']
            requests.post(
               f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
               data={
                    "chat_id": telegram_chat_id,
                    "text": f"<b><a href='{doc_url}'>{doc_title}</a></b>",
                    "parse_mode": "HTML"
                    })

def handle_sticker(message):
    attachments = message['attachments']

    for attachment in attachments:
        if attachment['type'] == 'sticker':
            for sticker_image in attachment['sticker']['images']:
                if sticker_image['width'] == 128 and sticker_image['height'] == 128:
                    requests.post(
                        f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto",
                        data={
                             "chat_id": telegram_chat_id,
                             "photo": sticker_image['url']
                             })

def handle_poll(message):
    attachments = message['attachments']

    for attachment in attachments:
        if attachment['type'] == 'poll':
            requests.post(
               f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
               data={
                    "chat_id": telegram_chat_id,
                    "text": f"<b>Опрос: {attachment['poll']['question']}</b>",
                    "parse_mode": "HTML"
                    })

def handle_wall(message):
    attachments = message['attachments']

    for attachment in attachments:
        if attachment['type'] == 'wall':
            requests.post(
               f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
               data={
                    "chat_id": telegram_chat_id,
                    "text": f"<b>Запись со стены сообщества: {attachment['wall']['from']['name']}</b>",
                    "parse_mode": "HTML"
                    })

def headler(message):
    handle_photo(message)
    handle_video(message)
    handle_audio_message(message)
    handle_audio(message)
    handle_doc(message)
    handle_sticker(message)
    handle_poll(message)
    handle_wall(message)

for event in longpoll.listen():
    print(f"Новое сообщение: \n\n{event.obj.message}\n\n")

    message_author_info = vk.users.get(user_ids=event.obj.message['from_id'])
    message_author = f"{message_author_info[0]['first_name']} {message_author_info[0]['last_name']}"
    message_object = event.obj.message

    if message_object['fwd_messages'] != []:
        while message_object['fwd_messages'][0]['text'] == '' and message_object['fwd_messages'][0]['attachments'] == []:
            message_object = message_object['fwd_messages'][0]
            if message_object['fwd_messages'] == []:
                break

        for fwd_message in message_object['fwd_messages']:

            message_author_info_fwd = vk.users.get(user_ids=fwd_message['from_id'])
            message_author_fwd = f"{message_author_info_fwd[0]['first_name']} {message_author_info_fwd[0]['last_name']}"

            handle_text(f'{message_author} ✉️\n\nПереслано от {message_author_fwd} 🔊', {True: f'{fwd_message["text"]}', False: f''}["text" in fwd_message])

            if 'attachments' in fwd_message and fwd_message['attachments'] != []:
                headler(fwd_message)
    else:
        handle_text(f'{message_author} ✉️', {True: f'{message_object["text"]}', False: f''}['text' in message_object])
        if 'attachments' in message_object and message_object['attachments'] != []:
            headler(message_object)

'''
ЗАДАЧИ
- Обойти группировку сообщений (при отсылании более 3 сообщений, json пакет регистрирует только первое сообщение)
- Доработать пересылку аудиозаписей и видеозаписей
'''
