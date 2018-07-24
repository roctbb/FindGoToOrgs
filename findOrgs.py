import networkx as nx
import matplotlib.pyplot as plt
import time
import vk

session = vk.Session(access_token='fc93487c59aa386098d898af27c8eba1cfdd9d09462c6c67bb8f5173b14af1ac847a5589894ad76149622')
api = vk.API(session)

# создаем пустой граф
G = nx.Graph()

# выбираем группу
members = api.groups.getMembers(group_id='80270762', fields='domain', v=5.74)['items']
members += api.groups.getMembers(group_id='80270762', fields='domain', v=5.74, offset=1000)['items']

print('members:', len(members))

# каждого участника добавляем в граф
for member in members:
    G.add_node(member['domain'], label='{} {}'.format(member['first_name'], member['last_name']))


n = 0
for member in members:
    try:

        if n % 10 == 0:
            print('done {} / {}'.format(n, len(members)))
        n += 1
        # print("current user: {} {}".format(member['first_name'], member['last_name']))
        friends = api.friends.get(user_id=member['id'], fields='domain', v=5.74)
        # print(len(friends['items']))
        for friend in friends['items']:
            if G.has_node(friend['domain']):
                G.add_edge(friend['domain'], member['domain'])

        time.sleep(0.20)
    except Exception as e:
        print(e)

# сохраняем в файле
nx.write_gexf(G, 'friends.gexf')
i = 0
for member in sorted(G.nodes(), key=lambda x:G.degree(x), reverse=True):
    print(i,':', member, '-', G.degree(member))
    i += 1