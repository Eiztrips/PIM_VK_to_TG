import vk_api, requests, json
from vk_api.bot_longpoll import VkBotLongPoll
from config import vk_c, tg_c


vk_session = vk_api.VkApi(token = vk_c['token'])
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, vk_c['group_id'])

telegram_bot_token = tg_c['tg_tkn']
telegram_chat_id = tg_c['tg_chat_id']


while True:
    try:
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
        
        def handle_video(message): #Доработать передачу видео
            attachments = message['attachments']
        
            for attachment in attachments:
                if attachment['type'] == 'video':
                    title = attachment['video']['title']
                    response = requests.post(
                       f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
                       data={
                            "chat_id": telegram_chat_id,
                            "text": f"<b>Видеозапись: {title}</b>",
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
                    with open('audio.mp3', 'wb') as f:
                        f.write(audio_file.content)

                    with open('audio.mp3', 'rb') as audio_file:
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
                            "text": f"<b>Запись со стены сообщества: {attachment['wall']['from']['name']}</b>",
                            "parse_mode": "HTML"
                            })
                    
                    print(response.json())
        
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
            response = vk.messages.getByConversationMessageId(peer_id=event.obj['message']['peer_id'], conversation_message_ids=event.obj['message']['conversation_message_id'])
        
            print(f"\nНовое сообщение: \n\n{json.dumps(response)}\n\n")
        
            message_author_info = vk.users.get(user_ids=event.obj.message['from_id'])
            message_author = f"{message_author_info[0]['first_name']} {message_author_info[0]['last_name']}"
            message_object = response['items'][0]
        
            if message_object['fwd_messages'] != []:
                while message_object['fwd_messages'][0]['text'] == '' and message_object['fwd_messages'][0]['attachments'] == []:
                    message_object = message_object['fwd_messages'][0]
                    if message_object['fwd_messages'] == []:
                        break
                    
                for fwd_message in message_object['fwd_messages']:
                
                    message_author_info_fwd = vk.users.get(user_ids=fwd_message['from_id'])
                    message_author_fwd = f"{message_author_info_fwd[0]['first_name']} {message_author_info_fwd[0]['last_name']}"

                    atachments_list = [attachment['type'] for attachment in fwd_message['attachments']]
                    handle_text(f'{message_author} ✉️\n\nПереслано от {message_author_fwd} 🔊', {True: f'{fwd_message["text"]}', False: f''}["text" in fwd_message and (not('photo' in atachments_list))])
        
                    if 'attachments' in fwd_message and fwd_message['attachments'] != []:
                        headler(fwd_message)
            else:

                atachments_list = [attachment['type'] for attachment in message_object['attachments']]
                handle_text(f'{message_author} ✉️', {True: f'{message_object["text"]}', False: f''}['text' in message_object and (not('photo' in atachments_list))])

                if 'attachments' in message_object and message_object['attachments'] != []:
                    headler(message_object)

    except Exception:
        print(Exception)
        pass

'''
ЗАДАЧИ
- Доработать пересылку видеозаписей
'''
