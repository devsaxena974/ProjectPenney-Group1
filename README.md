## Project Penney

This repository contains files which can be used to simulate a variation of Penney's Game known as the Humble-Nishiyama Randomness Game, in which two players compete to see how many times a selected three-color sequence (Black Black Red, Red Black Red, etc.) appears in a shuffled deck of cards. When a player's chosen sequence appears, they get all of the drawn cards up to that point. The winner is determined in one of two ways: highest number of cards held or highest number of times a player's sequence appeared, known as a "trick".

Files included:

* `simulation.py`: A Python file with code to run a function which simulates two version of Penney's Game. **Version 1** determines the winner by whichever player has the most cards in their pile. **Version 2** assigns points to tricks, and whichever player wins the most tricks wins the game. This function can run N additional game iterations and augment the results to the existing ones.

* `heatmap.py`: A Python file with code to run a function which converts the results of the simulation (stored as json files) into probability matrices and generates two heatmaps of said probabilities for both versions of the game.

Data for each simulation are stored as text files in the `data` folder with names like **example file name 1**, **example file name 2**. Heatmaps are stored in the figures `figures` folder with names `num_cards_probs.png` and `num_tricks_probs.png`.

## Write Ups
### Simulation Team

### Data Management/Processing Team

### Data Visualization Team
