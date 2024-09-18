## Project Penney

Data for each simulation are stored as **whatever this is** in the `data` folder with names like **example file name 1**, **example file name 2**. Heatmaps are stored in the `figures` folder with names num_cards_probs.png and num_tricks_probs.png. 

Files included:

* simulation.ipynb: A Jupyter notebook with code to run a function which simulates two version of Penney's Game. **Version 1** determines the winner by whichever player has the most cards in their pile. **Version 2** assigns points to tricks, and whichever player wins the most tricks wins the game. This function can run N additional game iterations and augment the results to the existing ones.

* heatmap.ipynb: A Jupyter notebook with code to run a function which converts the results of the simulation into *this data format* and generates a heatmap of win probabilities for both versions of the game.
