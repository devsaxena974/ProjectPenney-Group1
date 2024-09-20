import seaborn as sns
import matplotlib.pyplot as plt
from  matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import os
import re
import json

win_counts_file = 'game_data.json'

def matrix_creator(win_counts_file):
    combinations = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
    matrix = pd.DataFrame(0.0, index=combinations, columns=combinations)

    # load the json data
    if os.path.exists(win_counts_file):                # Check if the win counts file exists
        with open(win_counts_file, 'r') as f:          # Open the file in read mode
            win_counts = json.load(f)                  # Load the win counts
            #return win_counts['player1_wins'], win_counts['player2_wins'] # Return the win counts
    
    num_rounds = win_counts['total_rounds_played']

    games = win_counts['win_data']
    for game in games:
        # strip the player combos to index the matrix at correct loc
        p1 = game[0:3]
        p2 = game[7:10]
        # calculate the probabilites for the win
        num_wins = win_counts['win_data'][game]
        prob = num_wins / num_rounds
        
        # save the data in the matrix
        matrix.loc[p1, p2] = float(prob)

        #print(win_counts['win_data'][game])

    return matrix

result = matrix_creator(win_counts_file)

sequences = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
def create_heatmaps(card_wins = result):

    if not os.path.exists('figures'):
        os.makedirs('figures')
       
    #Heatmap for number of cards
    plt.figure(figsize=(10,8))
    sns.heatmap(card_wins,
                annot=True,
                annot_kws={'color': 'black'},
                cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256),
                linewidths=.5,
                cbar_kws={'label': 'Win Probability'})
    plt.title('Win Probabilities for Card Scoring')
    plt.xlabel('Player 2 Choice')
    plt.ylabel('Player 1 Choice')
    plt.savefig('figures/num_card_probs.png', bbox_inches = 'tight')

    #Heatmap for number of tricks
    #plt.figure(figsize=(10,8))
    #sns.heatmap(trick_wins_df,
     #           annot=True,
      #          cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256),
     #           linewidths=.5,
     #           cbar_kws={'label': 'Win Probability'})
   # plt.title('Win Probabilities for Trick Scoring')
   # plt.xlabel('Player 2 Choice')
   # plt.ylabel('Player 1 Choice')
   # plt.savefig('figures/num_trick_probs.png', bbox_inches = 'tight')

create_heatmaps()
