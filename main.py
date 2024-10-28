def main():
    num_iterations = 1000  # Number of decks to generate and rounds to simulate
    decks_file = 'data/ones_and_zeros'
    probabilities_file = 'results/probabilities.json'
    reset_probabilities = False  # Set to True to reset cumulative probabilities

    # Optionally reset probabilities
    if reset_probabilities and os.path.exists(probabilities_file):
        os.remove(probabilities_file)
        print(f"Deleted existing '{probabilities_file}' to reset cumulative probabilities.")

    # Generate decks and save to decks_file
    generate_data(num_iterations, decks_file)
    print(f"\nGenerated {num_iterations} decks and saved to '{decks_file}'.")

    # Run simulation using the generated decks
    run_simulation(rounds=num_iterations, decks_file=decks_file, probabilities_file=probabilities_file)
    print("Simulation completed and probabilities updated.")

    # Generate heatmaps
    get_heatmaps('png')
    print("Heatmap generation completed.")

if __name__ == "__main__":
    main()
