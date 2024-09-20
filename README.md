## Project Penney

Data for each simulation are stored as text files in the `data` folder with names like `deck_file` and `deck_history`. Heatmaps will be stored in a folder named `figures` with names `num_cards_probs.png` and `num_tricks_probs.png`. For reproducibility we used a random seed of 440. By default, there is no random seed set. To specify one, set the `random_seed` parameter when calling the simulation function. 

Files included:

* `simulation.py`: A Python file with code to run a function which simulates two version of Penney's Game. **Version 1** determines the winner by whichever player has the most cards in their pile. **Version 2** assigns points to tricks, and whichever player wins the most tricks wins the game. This function can run N additional game iterations and augment the results to the existing ones.

* `heatmap.py`: A Python file with code to run a function which converts the results of the simulation (stored as json files) into probability matrices and generates two heatmaps of said probabilities for both versions of the game.

## Write Ups
### Simulation Team

### Data Management/Processing Team

* Dev Saxena: I worked on converting our stored win data and round data into a probability matrix returned as a pandas dataframe for the data visualization team to use. 

### Data Visualization Team
