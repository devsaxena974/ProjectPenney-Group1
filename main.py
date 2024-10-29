import os
from src.deck_generation import generate_data
from src.simulation import run_simulation
from src.heatmap import get_heatmaps

def penney_game(n: int, format: str, reset_probabilities = False):
    #num_iterations = n  # Number of decks to generate and rounds to simulate
    decks_file = 'data/ones_and_zeros'
    probabilities_file = 'results/results.json'
    #reset_probabilities = False  # Set to True to reset cumulative probabilities

    # Optionally reset probabilities
    if reset_probabilities and os.path.exists(probabilities_file):
        os.remove(probabilities_file)
        print(f"Deleted existing '{probabilities_file}' to reset cumulative probabilities.")

    # Generate decks and save to decks_file
    generate_data(n, decks_file)
    print(f"\nGenerated {n} decks and saved to '{decks_file}'.")

    # Run simulation using the generated decks
    run_simulation(rounds=n, decks_file=decks_file, probabilities_file=probabilities_file)
    print("Simulation completed and probabilities updated.")

    # Generate heatmaps
    get_heatmaps(format)
    print("Heatmap generation completed.")


