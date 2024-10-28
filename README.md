## Project Penney

### Description
--------------

This repository contains files which can be used to simulate a variation of Penney's Game known as the Humble-Nishiyama Randomness Game, in which two players compete to see how many times a selected three-color sequence (Black Black Red, Red Black Red, etc.) appears in a shuffled deck of cards. At the beginning of a game, both players choose a three-card sequence they will use for the whole game. The game can be played in two ways: by cards or by tricks. In the cards version, when a player's chosen sequence appears, they get all of the drawn cards up to that point. In the tricks version, each player takes their three card sequence each time it appears. The winner is determined in one of two ways: highest number of cards held or highest number of tricks. Probability rules show that Player Two can use Player One's chosen three-card sequence to choose a three-card sequence that gives them a much higher win probability than Player One. More can be found about how the game works and the accompanying logic by reading [this paper](https://www.datascienceassn.org/sites/default/files/Humble-Nishiyama%20Randomness%20Game%20-%20A%20New%20Variation%20on%20Penney%27s%20Coin%20Game.pdf) written by the game's creators. 

### Getting Started:
--------------
#### `simulation.py`
The main function, `run_simulation`, sets the number of rounds and optional random seed for shuffling the deck. For each round a shuffled deck of cards is created and games are simulated for all possible combinations each player can have. The results are saved and loaded into JSON files.

The `data` folder stores JSON files for game data, deck history, and win counts. `os.makedirs(data_folder)` creates the folder if it does not already exist.

The `generate_hands` function generates all possible hands in binary. 1 represents red and 0 represents black. Each hand is generated and returned as a list of lists. The `binary_to_color_string` function converts a binary list like [1,0,1] to "RBR".

The `simulate_game` function runs a single game between each possible combination of player hands against a shuffled deck. Its parameters are `hands`, `shuffled_deck`, and `count_total_cards`. For each pair of player card choices, this function goes through the deck and checks for matches against each hand. 

The `load_game_data` and `save_game_data` functions load and save the win matrix and total rounds played into JSON files. The deck history is saved for analysis purposes. 


#### `processing.py`
can someone update this once the processing file has code in it

#### `heatmap.py`
This file generates heatmaps based on pre-calculated win data from the simulation. The function takes the processed data and creates two customizable heatmaps for each version of the game.

The `get_data` function reads game results from a JSON file, formats them into a matrix, and prepares the data for visualization. 

The `make_annots` function creates uniform standards for each box in the heatmap. It formats the matrix annotations as "Win Percent (Tie Percent)". 

The `make_heatmaps` function takes in data, annotations, axis labels, and a title.

`make_heatmap_package` combins two heatmaps into one figure for side-by-side comparison. Finally, the `get_heatmaps` function calls `make_heatmap_package` to generate visualizations and save the final figure to `folders`. 


### Files/Folders Included:
--------------

* `simulation.py`: A Python file with code to run a function which simulates two version of Penney's Game for a given number of iterations, with an option to set a random seed for reproducibility. **Version 1** determines the winner by whichever player has the most cards in their pile. **Version 2** assigns points to tricks, and whichever player wins the most tricks wins the game. This function can run N additional game iterations and augment the results to the existing ones.

* `processing.py`: A Python file that will contain the functions that take the raw simulation output and turn them into the nice .json file for visualization

* `heatmap.py`: A Python file with code to run a function which converts the results of the simulation (stored as json files) into probability matrices and generates two heatmaps of said probabilities for both versions of the game.

Data for each simulation are stored as json files in the `data` folder. The data folder shows game data, deck history, and player win counts for both the tricks and total cards game mode. The game data files include the total player 1 wins for each card hand and the total games played, this data is used to calculate the probabilities. Heatmaps are stored in the `figures` folder with names `num_cards_probs.png` and `num_tricks_probs.png`. By default, there is no random seed set. To specify one, set the `random_seed` parameter when calling the simulation function. 

### Details
-------------
We need to explain (from Ron's Github):
#### Data Generation
The generation code first creates a string representing a full deck of cards, with 26 "red" cards (represented by '1') and 26 "black" cards (represented by '0'). The function to generate sequences takes this string, uses a provided seed value to initialize the random number generator, and then shuffles the characters in the string using numpy's shuffle function. This shuffled string is then converted back to a list and returned. The sequence generation function is then called multiple times, each time with a different seed value, in order to produce a list of multiple shuffled decks.

#### Data Scoring
The data scoring code replicates the game by taking in the produced decks and evaluating them using binary sequences selected by two players. The algorithm goes through the deck in groups of three cards, matching each sequence to the players' target sequences to give points depending on the results, with ties being considered individually. The complexity is approximately O(N⋅M), in which N represents the quantity of decks. M represents the total 3-bit sequences possible (8 in total), since every pair of sequences is examined in all decks. The results assume symmetry as only Player 1's wins and draws are recorded, with Player 2's results being the opposite.

#### Heatmaps
The results are presented as two side-by-side, 8x8 heatmaps created using a numpy array of win probabilities (**it is a numpy array right...?**). The left heatmap reflects the win probabilities of the cards version of the game. The right heatmap reflects the win probabilities of the tricks version of the game. The y-axis shows all possible three-card combinations an opponent could choose. The x-axis shows all possible three-card combinations "you" could choose. Each cell shows the probability of "you" winning based on your chosen sequence and your opponent's chosen sequence. The colorbar is shared between the two heatmaps, with high win probabilities represented by dark shades of blue and low win probabilities represented by light shades of blue. The diagonal, or the occurence of you and your opponent choosing the same three-card sequence, is grey because that is not an option in this version of the game. 


