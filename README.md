## Project Penney

### Description
--------------

This repository contains files which can be used to simulate a variation of Penney's Game known as the Humble-Nishiyama Randomness Game, in which two players compete to see how many times a selected three-color sequence (Black Black Red, Red Black Red, etc.) appears in a shuffled deck of cards. At the beginning of a game, both players choose a three-card sequence they will use for the whole game. The game can be played in two ways: by cards or by tricks. In the cards version, when a player's chosen sequence appears, they get all of the drawn cards up to that point. In the tricks version, each player takes their three card sequence each time it appears. The winner is determined in one of two ways: highest number of cards held or highest number of tricks. Probability rules show that Player Two can use Player One's chosen three-card sequence to choose a three-card sequence that gives them a much higher win probability than Player One. More can be found about how the game works and the accompanying logic by reading [this paper](https://www.datascienceassn.org/sites/default/files/Humble-Nishiyama%20Randomness%20Game%20-%20A%20New%20Variation%20on%20Penney%27s%20Coin%20Game.pdf) written by the game's creators. 

### Getting Started:
--------------
Need to use this section to explain to a new user how the code works.

### Files/Folders Included:
--------------

* `simulation.py`: A Python file with code to run a function which simulates two version of Penney's Game for a given number of iterations, with an option to set a random seed for reproducibility. **Version 1** determines the winner by whichever player has the most cards in their pile. **Version 2** assigns points to tricks, and whichever player wins the most tricks wins the game. This function can run N additional game iterations and augment the results to the existing ones.

* `processing.py`: A Python file that will contain the functions that take the raw simulation output and turn them into the nice .json file for visualization

* `heatmap.py`: A Python file with code to run a function which converts the results of the simulation (stored as json files) into probability matrices and generates two heatmaps of said probabilities for both versions of the game.

Data for each simulation are stored as json files in the `data` folder. The data folder shows game data, deck history, and player win counts for both the tricks and total cards game mode. The game data files include the total player 1 wins for each card hand and the total games played, this data is used to calculate the probabilities. Heatmaps are stored in the `figures` folder with names `num_cards_probs.png` and `num_tricks_probs.png`. By default, there is no random seed set. To specify one, set the `random_seed` parameter when calling the simulation function. 

### Details
-------------


