import networkx as nx

G = nx.read_gexf('friends.gexf')
i = 0
for member in sorted(G.nodes(), key=lambda x:G.degree(x), reverse=True):
    print(i,':', member, '-', G.degree(member))
    i += 1