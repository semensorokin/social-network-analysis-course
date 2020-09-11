"""
Now let's load in a more complex graph and perform some basic analysis on it.

We will be looking at chess_graph.txt, which is a directed graph of chess games in edge list format.

!head -5 chess_graph.txt

1 2 0	885635999.999997
1 3 0	885635999.999997
1 4 0	885635999.999997
1 5 1	885635999.999997
1 6 0	885635999.999997

Each node is a chess player, and each edge represents a game.
The first column with an outgoing edge corresponds to the white player,
the second column with an incoming edge corresponds to the black player.

The third column, the weight of the edge, corresponds to the outcome of the game.
A weight of 1 indicates white won, a 0 indicates a draw, and a -1 indicates black won.

The fourth column corresponds to approximate timestamps of when the game was played.

We can read in the chess graph using read_edgelist, and tell it to create the graph using a nx.MultiDiGraph.
"""

import networkx as nx
import pandas as pd


chess = nx.read_edgelist('chess_graph.txt', data=[('outcome', int), ('timestamp', float)],
                         create_using=nx.MultiDiGraph())
print(chess.is_directed(), chess.is_multigraph())


# Looking at the degree of each node, we can see how many games each person played.
# A dictionary is returned where each key is the player, and each value is the number of games played.
games_played = dict(chess.degree())
print(games_played)


# Using list comprehension, we can find which player played the most games.
max_value = max(games_played.values())
max_key, = [i for i in games_played.keys() if games_played[i] == max_value]
print('Player {} played {} games.'.format(max_key, max_value))

# Let's use pandas to find out which players won the most games. First let's convert our graph to a DataFrame.
df = pd.DataFrame(list(chess.edges(data=True)), columns=['white', 'black', 'outcome'])
df.head()

# Next we can use a lambda to pull out the outcome from the attributes dictionary.
df['outcome'] = df['outcome'].map(lambda x: x['outcome'])
df.head()

# To count the number of times a player won as white, we find the rows where the
# outcome was '1', group by the white player, and sum.

# To count the number of times a player won as back, we find the rows where the
# outcome was '-1', group by the black player, sum, and multiply by -1.

# The we can add these together with a fill value of 0 for those players that
# only played as either black or white.
won_as_white = df[df['outcome']==1].groupby('white').sum()
won_as_black = -df[df['outcome']==-1].groupby('black').sum()
win_count = won_as_white.add(won_as_black, fill_value=0)
win_count.head()

# Using nlargest we find that player 330 won the most games at 109.
win_count.nlargest(5, 'outcome')
