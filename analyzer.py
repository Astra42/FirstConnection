from passwords import token, token_vk, id_group_vk
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from threading import Thread

import traceback
import vk_api

# Авторизация пользователя
vk = vk_api.VkApi(token=token)
session_api = vk.get_api()

# Авторизация группы
vk = vk_api.VkApi(token=token_vk)
ses_api = vk.get_api()
longPool = VkBotLongPoll(vk, id_group_vk)

phisycs = ['энергия', ' ток ', 'наука', 'science', 'веществ', 'ньютон', 'опыт']
history = ['полит', 'истор', ' сражен', 'войн', 'рим', 'галл', 'hist']
socions = [' общ', 'экономика', 'полит', 'отношения', 'документ', ' акт ', ' граждан', 'soci']
sport = [' спорт', 'атлет', 'фитнесс', 'здоров', 'воркаут', 'sport', 'зож', 'образ жизни']
biology = ['био', 'анатомия', 'естеств', ' живот', 'мед', 'сердц', ' насек']
IT = ['it','современные технологии', 'информатика', 'программ', 'код', 'c++', 'c#', 'python', 'print', ' ии ']


class MyError(Exception):
    pass


class Analyze(Thread):
    def __init__(self, id_chat, id_user, mes_id):
        Thread.__init__(self)
        self.chat_id = id_chat
        self.user_id = id_user
        self.id_mes = mes_id

    def run(self):
        try:
            check = session_api.users.get(user_ids=self.user_id)[0].get('is_closed', True)
            if check:
                raise MyError('У пользователя закрытый профиль!')
            sub = session_api.users.getSubscriptions(user_id=self.user_id, count=100, extended=True)['items']
            wallNotes = session_api.wall.get(owner_id=self.user_id, count=70, filter='owner', extended=True)['items']
            # ph, his, soc, sp, bio, it = 0, 0, 0, 0, 0, 0
            mass = [0, 0, 0, 0, 0, 0]
            for i in sub:
                if i['type'] == 'page':
                    for j in phisycs:
                        if j in i['name'].lower():
                            mass[0] += 2
                    for j in history:
                        if j in i['name'].lower():
                            mass[1] += 2
                    for j in socions:
                        if j in i['name'].lower():
                            mass[2] += 2
                    for j in sport:
                        if j in i['name'].lower():
                            mass[3] += 2
                    for j in biology:
                        if j in i['name'].lower():
                            mass[4] += 2
                    for j in IT:
                        if j in i['name'].lower():
                            mass[5] += 2
            for i in wallNotes:
                for j in phisycs:
                    if j in i['text'].lower():
                        mass[0] += 3
                for j in history:
                    if j in i['text'].lower():
                        mass[1] += 3
                for j in socions:
                    if j in i['text'].lower():
                        mass[2] += 3
                for j in sport:
                    if j in i['text'].lower():
                        mass[3] += 3
                for j in biology:
                    if j in i['text'].lower():
                        mass[4] += 3
                for j in IT:
                    if j in i['text'].lower():
                        mass[5] += 3
            friends = session_api.friends.get(user_id=self.user_id, order='hints', count=35)['items']
            kol = 1
            vk.method('messages.send', {'peer_id': self.chat_id, 'random_id': 0,
                                        'message': 'Обработанно друзей: (0/{})'.format(len(friends))})
            # ph, his, soc, sp, bio, it = 0, 0, 0, 0, 0, 0
            mass1 = [0, 0, 0, 0, 0, 0]
            for k in friends:
                check = session_api.users.get(user_ids=k)[0].get('is_closed', True)
                if check:
                    kol += 1
                    continue
                sub = session_api.users.getSubscriptions(user_id=k, count=60, extended=True)['items']
                wallNotes = session_api.wall.get(owner_id=k, count=60, filter='owner', extended=True)['items']
                for i in sub:
                    if i['type'] == 'page':
                        for j in phisycs:
                            if j in i['name'].lower():
                                mass1[0] += 1
                        for j in history:
                            if j in i['name'].lower():
                                mass1[1] += 1
                        for j in socions:
                            if j in i['name'].lower():
                                mass1[2] += 1
                        for j in sport:
                            if j in i['name'].lower():
                                mass1[3] += 1
                        for j in biology:
                            if j in i['name'].lower():
                                mass1[4] += 1
                        for j in IT:
                            if j in i['name'].lower():
                                mass1[5] += 1
                for i in wallNotes:
                    for j in phisycs:
                        if j in i['text'].lower():
                            mass1[0] += 3
                    for j in history:
                        if j in i['text'].lower():
                            mass1[1] += 3
                    for j in socions:
                        if j in i['text'].lower():
                            mass1[2] += 3
                    for j in sport:
                        if j in i['text'].lower():
                            mass1[3] += 3
                    for j in biology:
                        if j in i['text'].lower():
                            mass1[4] += 3
                    for j in IT:
                        if j in i['text'].lower():
                            mass1[5] += 3
                if kol % 3 == 0:
                    vk.method('messages.edit', {'peer_id': self.chat_id, 'random_id': 0, 'message_id': self.id_mes + 1,
                                                'message': 'Обработанно друзей: ({}/{})'.format(kol, len(friends))})
                kol += 1
            mass[mass1.index(max(mass1))] += 5
            vk.method('messages.edit', {'peer_id': self.chat_id, 'random_id': 0, 'message_id': self.id_mes + 1,
                                        'message': 'Обработанно друзей: ({}/{})'.format(len(friends), len(friends))})
            text_mes = 'Аналитика пользователя по специальностям:\n'
            mass_spec = ['Физика', 'История', 'Обществознание', 'Спорт', 'Биология', 'IT']
            univ_mass = ['Физико-технологическом институте', 'Историческом факультете',
                         'Институте экономики и управления',
                         'Институте физической культуры, спорта и полодежной политики',
                         'Институте естественных наук и математики',
                         'Институте радиоэлектроники и информационных технологий и Институте фундаментального образования']
            univ_mass_new = univ_mass.copy()
            mass_new = mass.copy()
            mass_new_spec = mass_spec.copy()
            mass = []
            mass_spec = []
            univ_mass = []
            while mass_new:
                mass.append(max(mass_new))
                mass_spec.append(mass_new_spec[mass_new.index(max(mass_new))])
                univ_mass.append(univ_mass_new[mass_new.index(max(mass_new))])
                del mass_new_spec[mass_new.index(max(mass_new))]
                del univ_mass_new[mass_new.index(max(mass_new))]
                del mass_new[mass_new.index(max(mass_new))]
            for i in range(len(mass)):
                cur = round((mass[i] / sum(mass)) * 100, 2)
                text_mes += '{} - {}%\n'.format(mass_spec[i], cur)
            vk.method('messages.send', {'peer_id': self.chat_id, 'random_id': 0, 'message': text_mes})
            invite = 'Будем ждать вас в {}\n Уральского Федерального Университета!'.format(univ_mass[0])
            vk.method('messages.send', {'peer_id': self.chat_id, 'random_id': 0, 'message': invite, 'attachment':'photo-202856797_457239023'})


        except MyError as e:
            vk.method('messages.send', {'peer_id': self.chat_id, 'random_id': 0, 'message': "Опс... %s" % e})
        except Exception:
            vk.method('messages.send', {'peer_id': self.chat_id, 'random_id': 0,
                                        'message': 'Опс... Похоже произошёл сбой, попробуйте позже...'})
            vk.method('messages.send', {'peer_id': 265219299, 'message': traceback.format_exc(), 'random_id': 0})


running = True
while running:
    try:
        for event in longPool.listen():
            print(event)
            if event.type == VkBotEventType.MESSAGE_NEW:
                chat_id = event.object.peer_id
                from_id = event.object.from_id
                text_m = event.object.text.lower()
                id_mes_con = event.object.conversation_message_id
                er_text = event.object.text
                id_mes = event.object.id
                if text_m.isdigit():
                    analyze = Analyze(chat_id, text_m, id_mes)
                    analyze.start()
    except Exception:
        pass
