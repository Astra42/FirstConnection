import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# API токен сообщества
mytoken = 'f6aaa34bf1046779717aea0fada497eb7944995efdb74bf7dfeebd2ef424709f2fa98d86c6826153512ae'


# Функция посылающая сообщение
def write_msg(user_id, message):
    random_id = vk_api.utils.get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


# Авторизуемся как сообщество
vk = vk_api.VkApi(token=mytoken)
longpoll = VkLongPoll(vk)

# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:

            # Сообщение от пользователя
            request = event.text

            # Логика формирования ответа бота
            if ('Привет' in request):
                otvet = 'Ну привет, если не шутишь!'
            else:
                otvet = ''

            write_msg(event.user_id, otvet)