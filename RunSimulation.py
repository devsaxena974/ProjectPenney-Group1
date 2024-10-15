import numpy as np
from tqdm import tqdm
from typing import List

def generate_data(num_iterations: int) -> List[List[int]]:
    red = '1' * 26
    black = '0' * 26
    deck = black + red  

    results = np.empty((num_iterations, 2), dtype=object)
    print(results.shape)
    
    for i in tqdm(range(num_iterations)):
        seed = i + 1  
        shuffled_deck = generate_sequence(deck, seed)  
        results[i] = [seed, ''.join(shuffled_deck)]  
    
    final_results = []
    decks_only = []
    for seed, binary_str in results:
        binary_list = list(binary_str)  
        final_results.append([seed, binary_list])
        decks_only.append(binary_list)  
    
    return final_results, decks_only

def generate_sequence(seq: str, seed: int) -> List[str]:
    np.random.seed(seed)  
    seq_list = list(seq)  
    np.random.shuffle(seq_list)  
    return seq_list
  
if __name__ == "__main__":
    res_with_seeds, decks_only = generate_data(1000000)
    print(res_with_seeds)
    print(decks_only)
    print(res_with_seeds[-1])  
    print(decks_only[-1])  
