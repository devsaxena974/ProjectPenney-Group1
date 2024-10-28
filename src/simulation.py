import numpy as np
from tqdm import tqdm
import json
from typing import List

def generate_sequence(seq: str, seed: int) -> List[str]:
    """Shuffle a sequence using a specific seed."""
    np.random.seed(seed)
    seq_list = list(seq)
    np.random.shuffle(seq_list)
    return seq_list

def generate_data(num_iterations: int, output_file: str, random_seed=None) -> None:
    """Generate multiple shuffled decks and save them to a data file."""
    red = '1' * 26  # Represent red cards with '1'
    black = '0' * 26  # Represent black cards with '0'
    deck = black + red  # Combine into a full deck

    results = []

    for i in tqdm(range(num_iterations), desc="Generating decks"):
        seed = random_seed or i + 1  # Use the seed for shuffling, or use a default seed if not provided
        shuffled_deck = generate_sequence(deck, seed)  # Shuffle the deck using the seed
        results.append(shuffled_deck)  # Store the shuffled deck

    # Save the results to a data file
    with open(output_file, 'w') as f:
        json.dump(results, f)
