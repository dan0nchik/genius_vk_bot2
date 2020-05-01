import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import keep_alive

# чтобы он писал в лс (хотя спрашивают в группе) - user_id=event.obj.message['user_id']
# чтобы отвечал в лс: if event.from_user:
storage = {}  # key: peer_id, values: [word, count]


def main():
    keep_alive.keep_alive()
    vk_session = vk_api.VkApi(
        token='7b97acdaf54b766b8569cbcf94534ffa75580a0efe1c85bf8c2874159fa95b7191f3ea1a6292b18292fbd')
    longpoll = VkBotLongPoll(vk_session, '193548634')  # id сообщества
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            if event.from_chat:
                if '!бот' in event.obj.message['text'].lower():
                    if event.obj.message['peer_id'] not in storage.keys():
                        storage[event.obj.message['peer_id']] = [None, 0]
                    vk.messages.send(peer_id=event.obj.message['peer_id'],
                                     message=f"Количество слов {storage.get(event.obj.message['peer_id'], [])[0]} "
                                     f"в чате: {storage.get(event.obj.message['peer_id'], [])[1]}\n"
                                     f"!сброс - сброс слова\n"
                                     f"!чистка - очистить слово\n"
                                     f"!слово - добавить слово",
                                     random_id=random.randint(0, 2 ** 64))
                    print(storage.get(event.obj.message['peer_id'])[0])
                elif '!сброс' in event.obj.message['text'].lower():

                    vk.messages.send(peer_id=event.obj.message['peer_id'],
                                     message=f"Слово {storage.get(event.obj.message['peer_id'])[0] } сброшено",
                                     random_id=random.randint(0, 2 ** 64))
                    storage.get(event.obj.message['peer_id'])[0] = ''
                elif '!чистка' in event.obj.message['text'].lower():
                    storage.get(event.obj.message['peer_id'])[1] = 0
                    vk.messages.send(peer_id=event.obj.message['peer_id'],
                                     message="Статистика очищена",
                                     random_id=random.randint(0, 2 ** 64))
                elif '!слово' in event.obj.message['text'].lower():
                    word = event.obj.message['text'].lower()
                    word = word.replace('!слово', '').lower()
                    word = word.replace(' ', '').lower()
                    storage[event.obj.message['peer_id']] = [word, 0]
                    print(word)
                    vk.messages.send(peer_id=event.obj.message['peer_id'],
                                     message=f"Теперь отслеживается слово {word}",
                                     random_id=random.randint(0, 2 ** 64))
                elif storage.get(event.obj.message['peer_id'], [''])[0] in event.obj.message['text'].lower():
                    storage.get(event.obj.message['peer_id'])[1] += event.obj.message['text'].lower().count(
                        storage.get(event.obj.message['peer_id'], [])[0])


if __name__ == '__main__':
    main()
