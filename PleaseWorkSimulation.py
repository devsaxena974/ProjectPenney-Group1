import os
import json
import random
import numpy as np
from tqdm import tqdm
from typing import List

def run_simulation(rounds=1000, random_seed=None):
    def generate_data(num_iterations: int) -> List[List[str]]:
        """Generate multiple shuffled decks."""
        red = '1' * 26  # Represent red cards with '1'
        black = '0' * 26  # Represent black cards with '0'
        deck = black + red  # Combine into a full deck

        results = []

        for i in tqdm(range(num_iterations)):
            seed = random_seed or i + 1  # Use the seed for shuffling, or use a default seed if not provided
            shuffled_deck = generate_sequence(deck, seed)  # Shuffle the deck using the seed
            results.append(shuffled_deck)  # Store the shuffled deck

        return results  # Return all shuffled decks

    def generate_sequence(seq: str, seed: int) -> List[str]:
        """Shuffle a sequence using a specific seed."""
        np.random.seed(seed)
        seq_list = list(seq)
        np.random.shuffle(seq_list)
        return seq_list

    def score_deck(deck: List[str], seq1: str, seq2: str, score_by_points=False) -> tuple:
        """Simulate a single game between Player 1 and Player 2 based on their sequences."""
        p1_score = 0
        p2_score = 0
        pile = 2  # Initial pile size

        i = 0
        while i < len(deck) - 2:
            current_sequence = ''.join(deck[i:i+3])  # Take a slice of 3 cards from the deck as a string
            if current_sequence == seq1:
                if score_by_points:
                    p1_score += 1  # Award 1 point if scoring by points
                    i += 3  # Move to the next 3 cards for both methods
                else:
                    p1_score += pile  # Add the number of cards in the pile to Player 1's score
                    pile = 2  # Reset the pile after Player 1 collects the cards
                    i += 3  # Skip the next 3 cards as the pile is wiped
            elif current_sequence == seq2:
                if score_by_points:
                    p2_score += 1  # Award 1 point if scoring by points
                    i += 3  # Move to the next 3 cards for both methods
                else:
                    p2_score += pile  # Add the number of cards in the pile to Player 2's score
                    pile = 2  # Reset the pile after Player 2 collects the cards
                    i += 3  # Skip the next 3 cards as the pile is wiped
            else:
                pile += 1  # Add a card to the pile
                i += 1  # Move to the next card

        return p1_score, p2_score

    def run_iteration(num_iter: int):
        """Run the simulation for a specified number of iterations."""
        # Binary sequences (in 3-bit format)
        sequences = ['000', '001', '010', '011', '100', '101', '110', '111']

        num_sequences = len(sequences)

        # Initialize matrices to store counts
        win_matrix_cards = np.zeros((num_sequences, num_sequences))
        tie_matrix_cards = np.zeros((num_sequences, num_sequences))
        win_matrix_points = np.zeros((num_sequences, num_sequences))
        tie_matrix_points = np.zeros((num_sequences, num_sequences))
        games_played = np.zeros((num_sequences, num_sequences))

        # Generate all shuffled decks
        all_decks = generate_data(num_iter)  # This will generate `num_iter` decks

        # Simulate games for each deck and count wins and ties
        for deck in all_decks:
            # Play each combination of Player 1 and Player 2 sequences
            for i in range(num_sequences):
                for j in range(num_sequences):
                    if j != i:  # Only compare distinct sequences
                        p1_seq = sequences[i]  # Player 1's sequence (binary)
                        p2_seq = sequences[j]  # Player 2's sequence (binary)

                        # Score the deck by total cards
                        p1_cards, p2_cards = score_deck(deck, p1_seq, p2_seq)

                        # Score the deck by points
                        p1_points, p2_points = score_deck(deck, p1_seq, p2_seq, score_by_points=True)

                        # Update games played
                        games_played[i, j] += 1

                        # Determine the winner or tie based on cards collected
                        if p1_cards > p2_cards:
                            win_matrix_cards[i, j] += 1
                        elif p1_cards == p2_cards:
                            tie_matrix_cards[i, j] += 1
                        # No need to count Player 2 wins separately

                        # Determine the winner or tie based on points
                        if p1_points > p2_points:
                            win_matrix_points[i, j] += 1
                        elif p1_points == p2_points:
                            tie_matrix_points[i, j] += 1
                        # No need to count Player 2 wins separately

        return win_matrix_cards, tie_matrix_cards, win_matrix_points, tie_matrix_points, games_played

    # Initialize sequences (we need the length)
    sequences = ['000', '001', '010', '011', '100', '101', '110', '111']
    num_sequences = len(sequences)

    # File to store probabilities
    probabilities_file = 'probabilities.json'

    # Initialize cumulative counts and total games played per combination
    if os.path.exists(probabilities_file):
        with open(probabilities_file, 'r') as f:
            data = json.load(f)
        # Load cumulative probabilities
        cumulative_prob_cards = np.array(data['cards']) / 100  # Convert back to probabilities
        cumulative_prob_ties_cards = np.array(data['cards_ties']) / 100
        cumulative_prob_tricks = np.array(data['tricks']) / 100
        cumulative_prob_ties_tricks = np.array(data['tricks_ties']) / 100
        cumulative_games_played = data['n']
    else:
        cumulative_prob_cards = np.zeros((num_sequences, num_sequences))
        cumulative_prob_ties_cards = np.zeros((num_sequences, num_sequences))
        cumulative_prob_tricks = np.zeros((num_sequences, num_sequences))
        cumulative_prob_ties_tricks = np.zeros((num_sequences, num_sequences))
        cumulative_games_played = 0

    # Run the iteration and get current counts
    win_matrix_cards, tie_matrix_cards, win_matrix_points, tie_matrix_points, games_played = run_iteration(rounds)

    # Update cumulative games played
    cumulative_games_played += rounds

    # Update cumulative probabilities
    # Compute total previous games per combination
    total_games_per_combination = cumulative_games_played - rounds + games_played

    # Update probabilities for 'cards'
    cumulative_prob_cards = (cumulative_prob_cards * (total_games_per_combination - games_played) + win_matrix_cards) / total_games_per_combination

    # Update probabilities for 'cards_ties'
    cumulative_prob_ties_cards = (cumulative_prob_ties_cards * (total_games_per_combination - games_played) + tie_matrix_cards) / total_games_per_combination

    # Update probabilities for 'tricks'
    cumulative_prob_tricks = (cumulative_prob_tricks * (total_games_per_combination - games_played) + win_matrix_points) / total_games_per_combination

    # Update probabilities for 'tricks_ties'
    cumulative_prob_ties_tricks = (cumulative_prob_ties_tricks * (total_games_per_combination - games_played) + tie_matrix_points) / total_games_per_combination

    # Replace NaN with 0.0 (in case of divisions by zero)
    cumulative_prob_cards = np.nan_to_num(cumulative_prob_cards)
    cumulative_prob_ties_cards = np.nan_to_num(cumulative_prob_ties_cards)
    cumulative_prob_tricks = np.nan_to_num(cumulative_prob_tricks)
    cumulative_prob_ties_tricks = np.nan_to_num(cumulative_prob_ties_tricks)

    # Multiply probabilities by 100 to save as percentages in JSON (without percent sign)
    # Round to one decimal place to avoid floating-point artifacts
    cumulative_prob_cards_percent = np.round(cumulative_prob_cards * 100, 1)
    cumulative_prob_ties_cards_percent = np.round(cumulative_prob_ties_cards * 100, 1)
    cumulative_prob_tricks_percent = np.round(cumulative_prob_tricks * 100, 1)
    cumulative_prob_ties_tricks_percent = np.round(cumulative_prob_ties_tricks * 100, 1)

    # Prepare the data to be saved in the JSON file
    data_to_save = {
        'cards': cumulative_prob_cards_percent.tolist(),
        'cards_ties': cumulative_prob_ties_cards_percent.tolist(),
        'tricks': cumulative_prob_tricks_percent.tolist(),
        'tricks_ties': cumulative_prob_ties_tricks_percent.tolist(),
        'n': cumulative_games_played
    }

    with open(probabilities_file, 'w') as f:
        json.dump(data_to_save, f)

    # Function to print matrices as percentages with one decimal
    def print_percentage_matrix(matrix, title):
        print(title)
        matrix_percent = np.flipud(matrix * 100)
        # Format the matrix to have percentages with one decimal place
        formatted_matrix = np.array2string(
            matrix_percent,
            formatter={'float_kind': lambda x: f'{x:0.1f}%'},
            max_line_width=np.inf
        )
        print(formatted_matrix)
        print()

    # Print cumulative probabilities with formatted percentages
    print_percentage_matrix(cumulative_prob_cards, "Probability of Player 1 Wins by Total Cards:")
    print_percentage_matrix(cumulative_prob_ties_cards, "Probability of Ties by Total Cards:")
    print_percentage_matrix(cumulative_prob_tricks, "Probability of Player 1 Wins by Points:")
    print_percentage_matrix(cumulative_prob_ties_tricks, "Probability of Ties by Points:")
    print("Total Games Played per Combination (n):")
    print(data_to_save['n'])

    return cumulative_prob_cards, cumulative_prob_ties_cards, cumulative_prob_tricks, cumulative_prob_ties_tricks

# Example of running the simulation
if __name__ == "__main__":
    p1_wins_cards_array, ties_cards_array, p1_wins_points_array, ties_points_array = run_simulation(1000)  # Adjust the number of rounds as needed
