import os
from src.deck_generation import generate_data
from src.simulation import run_simulation
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Display settings for figures
FIG_HIGH = 8
FIG_WIDE = 8

TITLE_SIZE = 18
LABEL_SIZE = 14
TICKLABEL_SIZE = 12
TICK_SIZE = 10
ANNOT_SIZE = 8

def format_data(data: list) -> np.ndarray:
    '''
    Formats the numeric values for each array in the dictionary for annotations.
    '''
    data_new = np.array(data, dtype='float32')
    np.fill_diagonal(data_new, np.nan)
    return np.round(np.flip(data_new, axis=1))

def make_annots(wins: np.ndarray, ties: np.ndarray) -> np.ndarray:
    '''
    Creates an array of strings in the form "Win Percent (Tie Percent)" for cell annotations.
    '''
    annots = []
    for i in range(8):
        row = []
        for j in range(8):
            if np.isnan(wins[i, j]):
                row.append('')
            else:
                row.append(f'{int(wins[i, j])} ({int(ties[i, j])})')
        annots.append(row)
    return np.array(annots)

def make_heatmap(arr: np.ndarray,
                 annots: np.ndarray,
                 ax: plt.Axes = None,
                 title: str = None,
                 library: str = 'matplotlib',
                 cbar_ax=None) -> tuple:
    '''
    Generates a single heatmap using formatted data and annotations.
    '''
    seqs = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

    if library == 'matplotlib':
        if ax is None:
            # Create a new figure
            fig, ax = plt.subplots(1, 1, figsize=(FIG_WIDE, FIG_HIGH))
        else:
            # Get the parent figure
            fig = ax.get_figure()

        sns.heatmap(data=arr,
                    ax=ax,
                    vmin=0,
                    vmax=100,
                    linewidth=0.01,
                    cmap='Blues',
                    cbar=False,
                    annot=annots,
                    fmt='')

        ax.set_xticklabels(seqs, fontsize=TICKLABEL_SIZE)
        ax.set_yticklabels(seqs[::-1], fontsize=TICKLABEL_SIZE)
        ax.set_title(title, fontsize=TITLE_SIZE)
        ax.set_facecolor('lightgray')
        
        return fig, ax

def make_heatmap_package(cards: np.ndarray,
                         cards_ties: np.ndarray,
                         tricks: np.ndarray,
                         tricks_ties: np.ndarray,
                         n,
                         library: str = 'matplotlib') -> tuple:
    '''
    Creates two side-by-side heatmaps to visualize both versions of the game.
    '''
    if library == 'matplotlib':
        fig, ax = plt.subplots(1, 2, figsize=(FIG_WIDE*2, FIG_HIGH))

        # Cards heatmap (left)
        cards_annots = make_annots(cards, cards_ties)
        make_heatmap(cards, cards_annots, ax[0], 
                    title=f'My Chance of Winning by Cards\n(n = {n})')
    
        ax[0].set_xlabel('My Choice', fontsize=LABEL_SIZE)
        ax[0].set_ylabel('Opponent Choice', fontsize=LABEL_SIZE)

        # Tricks heatmap (right)
        tricks_annots = make_annots(tricks, tricks_ties)
        make_heatmap(tricks, tricks_annots, ax[1], 
                    title=f'My Chance of Winning by Tricks\n(n = {n})')
        
        ax[1].set_xlabel('My Choice', fontsize=LABEL_SIZE)
        ax[1].set_ylabel('Opponent Choice', fontsize=LABEL_SIZE)

        # Add custom colorbar
        cbar_ax = fig.add_axes([.92, 0.11, 0.02, .77])
        cb = fig.colorbar(ax[1].collections[0], cax=cbar_ax, format='%.0f%%')
        cb.outline.set_linewidth(.2)
        
        return fig, ax

        #Cards heatmap
        cards_annots = make_annots(cards, cards_ties)
        fig.add_trace(
            go.Heatmap(
                z = cards,
                colorscale = 'Blues',
                colorbar = dict(title = 'Win %', thickness = 20),
                text = cards_annots,
                texttemplate = '%{text}',
                hoverinfo = 'text+z',
                showscale= False
            ),
            row = 1, col = 1
        )

        #Tricks heatmap
        tricks_annots = make_annots(tricks, tricks_ties)
        fig.add_trace(
            go.Heatmap(
                z = tricks,
                colorscale = 'Blues',
                colorbar = dict(title = 'Win %', thickness = 20),
                text = tricks_annots,
                texttemplate = '%{text}',
                hoverinfo = 'text+z'
            ),
            row = 1, col = 2
        )

        fig.update_layout(
            width = FIG_WIDE*2*100, height = FIG_HIGH*100,
            margin = dict(l = 50, r = 50, t = 80, b = 50)
        )

        tick_labels = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
        fig.update_xaxes(title_text = 'My Choice', tickvals = list(range(8)), ticktext = tick_labels, showgrid = False, row = 1, col = 1)
        fig.update_yaxes(title_text = 'Opponent Choice', tickvals=list(range(8)), ticktext = tick_labels[::-1], showgrid = False, row = 1, col = 1)

        fig.update_xaxes(title_text = 'My Choice', tickvals = list(range(8)), ticktext = tick_labels, showgrid = False, row = 1, col = 2)
        fig.update_yaxes(title_text = 'Opponent Choice', tickvals=list(range(8)), ticktext = tick_labels[::-1], showgrid = False, row = 1, col = 2)

        return fig, None


def get_heatmaps(format: str):
    '''
    Generates heatmap images and saves them to the 'figures' folder.
    '''
    probabilities_file = 'results/probabilities.json'
    if os.path.exists(probabilities_file):
        with open(probabilities_file, 'r') as f:
            results = json.load(f)
    else:
        print(f"Probabilities file '{probabilities_file}' not found.")
        return

    cards = format_data(results['cards'])
    cards_ties = format_data(results['cards_ties'])
    tricks = format_data(results['tricks'])
    tricks_ties = format_data(results['tricks_ties'])
    n = results['n']

    # Ensure the 'figures' directory exists
    figures_dir = 'figures'
    os.makedirs(figures_dir, exist_ok=True)
    
    if format == 'png':
        fig, ax = make_heatmap_package(cards, cards_ties, tricks, tricks_ties, n, library='matplotlib')
        fig.savefig(os.path.join(figures_dir, 'heatmap.png'), format='png', bbox_inches='tight')
        plt.close(fig)  # Close the figure to free memory
        print(f"Heatmap saved as '{figures_dir}/heatmap.png'.")
    else:
        print("Format not supported, please enter 'png'.")
