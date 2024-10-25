import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# Display settings for figures
FIG_HIGH = 8
FIG_WIDE = 8

TITLE_SIZE = 18
LABEL_SIZE = 14
TICKLABEL_SIZE = 12
TICK_SIZE = 10
ANNOT_SIZE = 8

def get_data() -> np.ndarray:
    '''
    Responsible for reading in .json file, pulling each array from the dictionary, and formatting the numeric values for annotations
    '''
    filepath = 'results/results.json'
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)

    # Need to find a way to iterate through dictionary and format each numpy array

    np.fill_diagonal(data, np.nan)
    return np.round(np.flip(data, axis = 1))


def make_annots(wins : np.ndarray, ties: np.ndarray) -> np.ndarray:
    '''
    Takes in two formatted arrays for wins and ties to return one array of strings of form "Win Percent (Tie Percent)" to use for cell annotations
    '''
    annots = []
    for i in range(8):
        row = []
        for j in range(8):
            if np.isnan(wins[i,j]):
                row.append('')
            else:
                row.append(f'{str(int(wins[i,j]))} ({str(int(ties[i,j]))})')
        annots.append(row)
    return np.array(annots)


def make_heatmap(arr: np.ndarray,
                 annots: np.ndarray,
                 ax: plt.Axes = None,
                 title: str = None,
                ) -> tuple[plt.Figure, plt.Axes]:
    '''
    Generates a single heatmap using formatted data and annotations. 
    '''
    
    seqs = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
    
    settings = {
        'vmin': 0,
        'vmax': 100,
        'linewidth': 0.01,
        'cmap': 'Blues',
        'cbar': False,
        'annot': annots,
        'fmt': ''
    }

    if ax is None:
        # Create a new figure
        fig, ax = plt.subplots(1, 1, figsize=(FIG_WIDE, FIG_HIGH))
    else:
        # Get the parent figure
        fig = ax.get_figure()

    sns.heatmap(data = arr, 
                ax = ax,
                vmin = 0,
                vmax = 100,
                linewidth = 0.01,
                cmap = 'Blues',
                cbar = False,
                annot = annots,
                fmt = '')

    ax.set_xticklabels(seqs, fontsize=TICKLABEL_SIZE)
    ax.set_yticklabels(seqs[::-1], fontsize=TICKLABEL_SIZE)
    ax.set_title(title, fontsize=TITLE_SIZE)
    ax.set_facecolor('lightgray')
    
    return fig, ax


def make_heatmap_package(cards: np.ndarray,
                         cards_ties: np.ndarray,
                         tricks: np.ndarray,
                         tricks_ties: np.ndarray,
                         n
                        ) -> tuple[plt.Figure, plt.Axes]:
    
    '''
    Creates two side-by-side heatmaps as a single figure to visualize both versions of the game.
    '''

    fig, ax = plt.subplots(1, 2, figsize = (FIG_WIDE*2, FIG_HIGH))

    # Cards heatmap (left)
    cards_annots = make_annots(cards, cards_ties)
    make_heatmap(cards, cards_annots, ax[0], 
                 title = f'My Chance of Winning by Cards\n(n = {n})')
    
    ax[0].set_xlabel('My Choice', fontsize = LABEL_SIZE)
    ax[0].set_ylabel('Opponent Choice', fontsize = LABEL_SIZE)

    # Tricks heatmap (right)
    tricks_annots = make_annots(tricks, tricks_ties)
    make_heatmap(tricks, tricks_annots, ax[1], 
                 title = f'My Chance of Winning by Tricks\n(n = {n})')
    ax[1].set_xlabel('My Choice', fontsize = LABEL_SIZE)
    ax[1].set_ylabel('Opponent Choice', fontsize = LABEL_SIZE)

    # Add custom colorbar
    cbar_ax = fig.add_axes([.92, 0.11, 0.02, .77])
    cb = fig.colorbar(ax[1].collections[0], cax=cbar_ax, format='%.0f%%')
    cb.outline.set_linewidth(.2)
    
    return fig, ax


def get_heatmaps():
    '''
    This will be the master function that can be called to generate new heatmaps and save them to the 'figures' folder
    '''



# if not os.path.exists('figures'):
#        os.makedirs('figures')
