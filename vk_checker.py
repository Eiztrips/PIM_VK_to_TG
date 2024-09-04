import vk_api,  json, src.additional_func, src.handle_func
from vk_api.bot_longpoll import VkBotLongPoll
from src.config import vk_c, tg_c

vk_session = vk_api.VkApi(token = vk_c['token'])
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, vk_c['group_id'])

telegram_bot_token = tg_c['tg_tkn']
telegram_chat_id = tg_c['tg_chat_id']


while True:
    try:
        src.additional_func.happy_b()

        for event in longpoll.listen():

            package = vk.messages.getByConversationMessageId(peer_id=event.obj['message']['peer_id'], conversation_message_ids=event.obj['message']['conversation_message_id'])

            print(f"\nНовое сообщение: \n\n{json.dumps(package)}\n\n")

            message_author_info = vk.users.get(user_ids=event.obj.message['from_id'])
            message_author = f"{message_author_info[0]['first_name']} {message_author_info[0]['last_name']}"
            message_object = package['items'][0]
            repeat = False

            def main():
                global message_object, repeat
                while message_object['fwd_messages'][0]['text'] == '' and message_object['fwd_messages'][0]['attachments'] == []:

                    message_object = message_object['fwd_messages'][0]
                    

                    if message_object['fwd_messages'] == []:
                        break
                
                if 'text' in message_object['fwd_messages'][0]['fwd_messages'][0]:
                        repeat = True
                        
                if repeat: message_object = message_object['fwd_messages'][0]

                for fwd_message in message_object['fwd_messages']:

                    message_author_info_fwd = vk.users.get(user_ids=fwd_message['from_id'])
                    message_author_fwd = f"{message_author_info_fwd[0]['first_name']} {message_author_info_fwd[0]['last_name']}"

                    atachments_list = [attachment['type'] for attachment in fwd_message['attachments']]
                    check = {True:f"{message_author} ✉️\n\n", False: ''}[package["items"][0]["peer_id"] != 2000000006]
                    src.handle_func.handle_text(f'{check}Переслано от {message_author_fwd} 🔊', {True: f'{fwd_message["text"]}', False: ''}["text" in fwd_message and ('photo' not in atachments_list)])

                    if 'attachments' in fwd_message and fwd_message['attachments'] != []:
                        src.handle_func.handler(fwd_message)

                if repeat:
                    main()
                    repeat = False

            if message_object['fwd_messages'] != [] and 'fwd_messages' in message_object:
                main()

                        
            else:

                atachments_list = [attachment['type'] for attachment in message_object['attachments']]
                src.handle_func.handle_text({True: f'{message_author} ✉️', False: ''}[message_object["peer_id"] != 2000000006], {True: f'{message_object["text"]}', False: ''}['text' in message_object and ('photo' not in atachments_list)])

                if 'attachments' in message_object and message_object['attachments'] != []:
                    src.handle_func.handler(message_object)

    except Exception as e:
        print(f"\n\nПроизошла ошибка: \n{e}\n\n", f'[{str(e) == "fwd_messages"}]')

'''
ЗАДАЧИ
- Доработать обработку документов и записей со стен сообществ
- Объединять всё в одном сообщении
'''
