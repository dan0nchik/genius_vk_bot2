import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


def main():
    vk_session = vk_api.VkApi(
        token='7b97acdaf54b766b8569cbcf94534ffa75580a0efe1c85bf8c2874159fa95b7191f3ea1a6292b18292fbd')
    # токен к моему сообществу
    longpoll = VkBotLongPoll(vk_session, '193548634')  # id сообщества
    word = 'гений'
    counter = 0
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            if event.from_chat:
                if word in event.obj.message['text'].lower():
                    counter += 1
                if '!бот' in event.obj.message['text']:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Количество выбранных слов в чате: {counter}\n"
                                             f"!сброс - сброс слова\n"
                                             f"!чистка - очистить слово\n"
                                             f"!слово - добавить слово",
                                     random_id=random.randint(0, 2 ** 64))
                if '!сброс' in event.obj.message['text']:
                    word = ''
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Слово сброшено",
                                     random_id=random.randint(0, 2 ** 64))
                if '!чистка' in event.obj.message['text'].lower():
                    counter = 0
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Статистика очищена",
                                     random_id=random.randint(0, 2 ** 64))

                if '!слово' in event.obj.message['text'].lower():
                    word = event.obj.message['text'].lower()
                    word = word.replace('!слово', '')
                    word = word.replace(' ', '')
                    print(word)
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"Теперь отслеживается слово {word}",
                                     random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
