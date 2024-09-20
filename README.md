## Project Penney

This repository contains files which can be used to simulate a variation of Penney's Game known as the Humble-Nishiyama Randomness Game, in which two players compete to see how many times a selected three-color sequence (Black Black Red, Red Black Red, etc.) appears in a shuffled deck of cards. When a player's chosen sequence appears, they get all of the drawn cards up to that point. The winner is determined in one of two ways: highest number of cards held or highest number of times a player's sequence appeared, known as a "trick".

Files included:

* `simulation.py`: A Python file with code to run a function which simulates two version of Penney's Game. **Version 1** determines the winner by whichever player has the most cards in their pile. **Version 2** assigns points to tricks, and whichever player wins the most tricks wins the game. This function can run N additional game iterations and augment the results to the existing ones.

* `heatmap.py`: A Python file with code to run a function which converts the results of the simulation (stored as json files) into probability matrices and generates two heatmaps of said probabilities for both versions of the game.

Data for each simulation are stored as text files in the `data` folder with names like `deck_file` and `deck_history`. Heatmaps are stored in the `figures` folder with names `num_cards_probs.png` and `num_tricks_probs.png`. By default, there is no random seed set. To specify one, set the `random_seed` parameter when calling the simulation function. 


## Write Ups
### Simulation Team

### Data Management/Processing Team

* Dev Saxena: I worked on converting our stored win data and round data into a probability matrix returned as a pandas dataframe for the data visualization team to use. 

### Data Visualization Team
* Annie Wicker: I worked on the function to generate the heatmaps and determine a color palette that would best convey the results. We used a red-white-green gradient color palette to represent low-medium-high win probabilities. We also worked with the Data Management and Processing team to adjust the heatmap function based on their determinations of the best way to store the simulation data. 
