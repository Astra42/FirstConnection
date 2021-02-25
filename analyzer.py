import vk_api

Token = open('pass.txt')

vk = vk_api.VkApi(token=Token.read())
session_api = vk.get_api()

phisycs = ['фарадей', 'формул', 'наука', 'science', 'веществ', 'ньютон', 'опыт']
history = ['полит', 'истор', 'сражен', 'войн', 'рим', 'галл']
socions = ['общ', 'экономика', 'полит', 'отношения', 'документ']
sport = ['спорт', 'атлет', 'фитнесс', 'образ', 'жизни', 'здоровье']
biology = ['био', 'анатомия', 'естеств', 'среда обитания']
IT = ['it', 'ит', 'современные технологии', 'информатика', 'программ', 'код', 'c++', 'c#']

sub = session_api.users.getSubscriptions(user_id=265219299, count=100, extended=True)['items']
ph, his, soc, sp, bio, it = 0, 0, 0, 0, 0, 0
for i in sub:
    if i['type'] == 'page':
        for j in phisycs:
            if (j in i['name'].lower()):
                ph += 1
        for j in history:
            if (j in i['name'].lower()):
                his += 1
        for j in socions:
            if (j in i['name'].lower()):
                soc += 1
        for j in sport:
            if (j in i['name'].lower()):
                sp += 1
        for j in biology:
            if (j in i['name'].lower()):
                bio += 1
        for j in IT:
            if (j in i['name'].lower()):
                it += 1
print(ph, his, soc, sp, bio, it)



friends = session_api.friends.get(user_id=265219299, count=5000,
                                  fields='photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group')[
    'items']

for i in sub:
    if i['type'] == 'page':
        print(i['name'])

# print(session_api.users.get(user_ids='df_nik', fields='status')[0])
# ближайший город(тюмень че, екат сам) из чуваков ищем тех г
# if i.get('occupation', False):
# if i['occupation'].get('name', '') in Towns:
# if (i.get('city', False)):
# if (i['city'].get('title', '') in Towns):
