import requests, json
from src.config import tg_c

telegram_bot_token = tg_c['tg_tkn']
telegram_chat_id = tg_c['tg_chat_id']

def handle_text(user, text):
            response = requests.post(
                        f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
                        data={
                             "chat_id": telegram_chat_id,
                             "text": f"<i>{user}</i>\n\n<b>{text}</b>",
                             "parse_mode": "HTML"
                             })
            print(response.json())

def handle_user(user):
    response = requests.post(
                f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
                data={
                     "chat_id": telegram_chat_id,
                     "text": f"<i>{user}</i>",
                     "parse_mode": "HTML"
                     })
    print(response.json())

def handle_photo(message):
    attachments = message['attachments']
    media_group = []
    for attachment in attachments:
        if attachment['type'] == 'photo':
            image = {"type": "photo", "media": f"{attachment['photo']['orig_photo']['url']}"}
            media_group.append(image)
    if media_group != []:
        media_group[0]["caption"] = f"{message['text']}"
        response = requests.post(
            f"https://api.telegram.org/bot{telegram_bot_token}/sendMediaGroup",
            data={
                 'chat_id': telegram_chat_id,
                 'media': json.dumps(media_group)
                 })
        print(response.json())

def handle_video(message):
    attachments = message['attachments']
    for attachment in attachments:
        if attachment['type'] == 'video':
            title = attachment['video']['title']
            response = requests.post(
               f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
               data={
                    "chat_id": telegram_chat_id,
                    "text": f"<a href='https://vk.com/video{attachment['video']['owner_id']}_{attachment['video']['id']}'>Видеозапись: {title}</a>",
                    "parse_mode": "HTML"
                    })
            print(response.json())

def handle_audio_message(message):
    attachments = message['attachments']
    for attachment in attachments:
        if attachment['type'] == 'audio_message':
            audio_message = attachment['audio_message']
            audio_url = audio_message['link_mp3']
            audio_data = requests.get(audio_url).content
            response = requests.post(
                f"https://api.telegram.org/bot{telegram_bot_token}/sendVoice",
                files={"voice": audio_data},
                data={"chat_id": telegram_chat_id})
            print(response.json()
    )
            
def handle_audio(message):
    attachments = message['attachments']
    for attachment in attachments:
        if attachment['type'] == 'audio':
            audio_file = requests.get(attachment['audio']['url'])
            with open('other_files/audio.mp3', 'wb') as f:
                f.write(audio_file.content)
            with open('other_files/audio.mp3', 'rb') as audio_file:
                files = {'audio': audio_file}
                data = {'chat_id': telegram_chat_id, 'title': attachment['audio']['title'], 'performer': attachment['audio']['artist']}
                response = requests.post(f'https://api.telegram.org/bot{telegram_bot_token}/sendAudio', files=files, data=data)
            print(response.json())

def handle_doc(message):
    attachments = message['attachments']
    for attachment in attachments:
         if attachment['type'] == 'doc':
            doc_url = attachment['doc']['url']
            doc_title = attachment['doc']['title']
            response = requests.post(
               f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
               data={
                    "chat_id": telegram_chat_id,
                    "text": f"<b><a href='{doc_url}'>{doc_title}</a></b>",
                    "parse_mode": "HTML"
                    })
            print(response.json())

def handle_sticker(message):
    attachments = message['attachments']
    for attachment in attachments:
        if attachment['type'] == 'sticker':
            for sticker_image in attachment['sticker']['images']:
                if sticker_image['width'] == 128 and sticker_image['height'] == 128:
                    response = requests.post(
                        f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto",
                        data={
                             "chat_id": telegram_chat_id,
                             "photo": sticker_image['url']
                             })
                    print(response.json())

def handle_poll(message):
    attachments = message['attachments']
    for attachment in attachments:
        if attachment['type'] == 'poll':
            response = requests.post(
               f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
               data={
                    "chat_id": telegram_chat_id,
                    "text": f"<b>Опрос: {attachment['poll']['question']}</b>",
                    "parse_mode": "HTML"
                    })
            print(response.json())

def handle_wall(message):
    attachments = message['attachments']
    for attachment in attachments:
        if attachment['type'] == 'wall':
            response = requests.post(
               f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
               data={
                    "chat_id": telegram_chat_id,
                    "text": "<b>Запись со стены сообщества</b>",
                    "parse_mode": "HTML"
                    })
            print(response.json())

def handler(message):
    handle_photo(message)
    handle_video(message)
    handle_audio_message(message)
    handle_audio(message)
    handle_doc(message)
    handle_sticker(message)
    handle_poll(message)
    handle_wall(message)