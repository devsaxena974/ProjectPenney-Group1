import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
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

def format_data(data: list) -> np.ndarray:
    '''
    Responsible for formatting the numeric values for each array in the dictionary for annotations
    '''
    data_new = np.array(data, dtype = 'float32')
    np.fill_diagonal(data_new, np.nan)
    return np.round(np.flip(data_new, axis = 1))


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
                 library: str = 'matplotlib',
                ) -> tuple[plt.Figure, plt.Axes]:
    '''
    Generates a single heatmap using formatted data and annotations with either the MatPlotLib or Plotly libraries
    '''
    
    seqs = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

    if library == 'matplotlib':
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

    elif library == 'plotly':
        heatmap = go.Heatmap(
            z = arr,
            colorscale = 'Blues',
            colorbar = dict(title = 'Win %'),
            text = annots,
            hoverinfo = "text+z"
        )

        fig = go.Figure(data = [heatmap])
        fig.update_layout(title=title, xaxis_title='My Choice', yaxis_title='Opponent Choice')
        fig.update_xaxes(tickvals=list(range(8)), ticktext=seqs)
        fig.update_yaxes(tickvals=list(range(8)), ticktext=seqs[::-1])

        return fig, None


def make_heatmap_package(cards: np.ndarray,
                         cards_ties: np.ndarray,
                         tricks: np.ndarray,
                         tricks_ties: np.ndarray,
                         n,
                         library: str = 'matplotlib'
                        ) -> tuple[plt.Figure, plt.Axes]:
    
    '''
    Creates two side-by-side heatmaps using the specified library as a single figure to visualize both versions of the game.
    '''

    if library == 'matplotlib':
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
    
    elif library == 'plotly':
        #Cards heatmap
        cards_annots = make_annots(cards, cards_ties)
        fig1 = make_heatmap(cards, cards_annots, title = f'My Chance of Winning by Cards\n(n = {n})', library = 'plotly')[0]

        #Tricks heatmap
        tricks_annots = make_annots(tricks, tricks_ties)
        fig2 = make_heatmap(tricks, tricks_ties, title = f'My Chance of Winning by Tricks\n(n = {n})', library = 'plotly')[0]

        #Combine into one figure
        fig1.update_layout(grid = dict(columns = 2, rows = 1))
        for trace in fig2.data:
            fig1.add_trace(trace)

        return fig1, None


def get_heatmaps(format: str):
    '''
    This is the master function that can be called to generate new PNG or HTML heatmap images and save them to the 'figures' folder
    '''

    filepath = 'results/results.json'
    if os.path.exists(filepath):
        with open(filepath) as f:
            results = json.load(f)
    
    cards = format_data(results['cards'])
    cards_ties = format_data(results['cards_ties'])
    tricks = format_data(results['tricks'])
    tricks_ties = format_data(results['tricks_ties'])
    n = results['n']

    if not os.path.exists('figures'):
        os.makedirs('figures')
    
    if format == 'png':
        fig, ax = make_heatmap_package(cards, cards_ties, tricks, tricks_ties, n, library = 'matplotlib')
        fig.savefig('figures/heatmap.png', format = 'png')

    elif format == 'html':
        fig, _ = make_heatmap_package(cards, cards_ties, tricks, tricks_ties, n, library = 'plotly')
        fig.write_html('figures/heatmap.html')
    
    else:
        print("Format not supported, please enter either 'png' or 'html'")

if __name__ == '__main__':
    #get_heatmaps('png')
    #get_heatmaps('html')
