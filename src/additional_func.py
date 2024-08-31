import datetime, requests
from src.config import tg_c, happy_b_day

telegram_bot_token = tg_c['tg_tkn']
telegram_chat_id = tg_c['tg_chat_id']

def happy_b(current_date = datetime.datetime.now().strftime('%m-%d')):
            content = open('other_files/date_cheker.txt', 'r+')

            if current_date in happy_b_day and content.read() != current_date:
                content.close()

                if type(happy_b_day[current_date]) is list:
                    response = requests.post(
                       f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
                       data={
                            "chat_id": telegram_chat_id,
                            "text": f"<b>У пользователей {', '.join(happy_b_day[current_date])} сегодня день рождения!!! 🎉</b>",
                            "parse_mode": "HTML"
                            })
                    
                else: 
                    response = requests.post(
                       f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage",
                       data={
                            "chat_id": telegram_chat_id,
                            "text": f"У пользователя <i><b>{happy_b_day[current_date]}</b></i> сегодня день рождения!!! 🎉",
                            "parse_mode": "HTML"
                            })
                    
                print(response.json())

                content = open('other_files/date_cheker.txt', 'w')
                content.write(current_date)
                content.close()
            else: content.close()

happy_b()