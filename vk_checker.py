import vk_api,  json, src.additional_func, src.handle_func
from vk_api.bot_longpoll import VkBotLongPoll
from src.config import vk_c, tg_c

vk_session = vk_api.VkApi(token = vk_c['token'])
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, vk_c['group_id'])

telegram_bot_token = tg_c['tg_tkn']
telegram_chat_id = tg_c['tg_chat_id']

for event in longpoll.listen():
    src.additional_func.happy_b()

    package = vk.messages.getByConversationMessageId(peer_id=event.obj['message']['peer_id'], conversation_message_ids=event.obj['message']['conversation_message_id'])

    print(f"\nНовое сообщение: \n\n{json.dumps(package)}\n\n")
    message_author_info = vk.users.get(user_ids=event.obj.message['from_id'])
    message_author = f"{message_author_info[0]['first_name']} {message_author_info[0]['last_name']}"
    message_object = package['items'][0]

    def main_forward(message):
        if "text" in message and message["text"] != "": 
            check_attacment = False
            for attachment in message["attachments"]:
                if "photo" in attachment:
                    check_attacment = True
            if check_attacment == False: src.handle_func.handle_text(message_author+" ✉", message["text"])
        src.handle_func.handler(message)

    main_forward(message_object)