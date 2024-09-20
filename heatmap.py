import seaborn as sns
import matplotlib.pyplot as plt
from  matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import os

#Initialize dummy matrices
card_wins_matrix = np.zeros((8,8))
trick_wins_matrix = np.zeros((8,8))

#Fill dummy matrices
i = 0
for x in range(8):
    for z in range(8):
        card_wins_matrix[x,z] = i
        trick_wins_matrix[x,z] = 64-i
        i+=1

print(card_wins_matrix)
print(trick_wins_matrix)
#Save dummy matrices
np.save("card_wins.npy",card_wins_matrix)
np.save("trick_wins.npy",trick_wins_matrix)

sequences = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
def create_heatmaps(card_wins = 'card_wins.npy', trick_wins = 'trick_wins.npy'):

    if not os.path.exists('figures'):
        os.makedirs('figures')
   
    card_wins_matrix = np.load(card_wins)
    trick_wins_matrix = np.load(trick_wins)

    card_wins_df = pd.DataFrame(card_wins_matrix, index = sequences, columns = sequences)
    trick_wins_df = pd.DataFrame(trick_wins_matrix, index = sequences, columns = sequences)

    #Heatmap for number of cards
    plt.figure(figsize=(10,8))
    sns.heatmap(card_wins_df,
                annot=True,
                cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256),
                linewidths=.5,
                cbar_kws={'label': 'Win Probability'})
    plt.title('Win Probabilities for Card Wins')
    plt.xlabel('Player 2 Choice')
    plt.ylabel('Player 1 Choice')
    plt.savefig('figures/num_card_probs.png', bbox_inches = 'tight')

    #Heatmap for number of tricks
    plt.figure(figsize=(10,8))
    sns.heatmap(trick_wins_df,
                annot=True,
                cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256),
                linewidths=.5,
                cbar_kws={'label': 'Win Probability'})
    plt.title('Win Probabilities for Trick Wins')
    plt.xlabel('Player 2 Choice')
    plt.ylabel('Player 1 Choice')
    plt.savefig('figures/num_trick_probs.png', bbox_inches = 'tight')

    create_heatmaps()