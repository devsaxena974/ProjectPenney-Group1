import numpy as np
from tqdm import tqdm
from typing import List

def generate_data(num_iterations: int) -> List[List[str]]:
        """Generate multiple shuffled decks."""
        red = '1' * 26  # Represent red cards with '1'
        black = '0' * 26  # Represent black cards with '0'
        deck = black + red  # Combine into a full deck

        results = []

        for i in tqdm(range(num_iterations)):
            seed = None or i + 1  # Use the seed for shuffling, or use a default seed if not provided
            shuffled_deck = generate_sequence(deck, seed)  # Shuffle the deck using the seed
            results.append(shuffled_deck)  # Store the shuffled deck

        return results  # Return all shuffled decks

def generate_sequence(seq: str, seed: int) -> List[str]:
        """Shuffle a sequence using a specific seed."""
        np.random.seed(seed)
        seq_list = list(seq)
        np.random.shuffle(seq_list)
        return seq_list

'''
if __name__ == "__main__":
    res_with_seeds, decks_only = generate_data(1000000)
    print(res_with_seeds)
    print(decks_only)
    print(res_with_seeds[-1])  
    print(decks_only[-1])  
'''