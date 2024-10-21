import os
import numpy as np
import json
import random
# importing time module for processing testing
import time

def run_simulation(rounds=1000, deck_data_file=None, random_seed=None):
    
    data_folder = 'data'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    def generate_hands():
        hands = []
        for i in range(8):
            combo = [(i >> j) & 1 for j in range(2, -1, -1)]
            hands.append(combo)
        return hands

    def binary_to_color_string(bits):
        return ''.join(['R' if bit == 1 else 'B' for bit in bits])
    
    def simulate_game(hands, shuffled_deck, count_total_cards):
        win_matrix = np.zeros((8, 8))
        player1_wins = 0
        player2_wins = 0

        for i, player1_hand in enumerate(hands):
            for j, player2_hand in enumerate(hands):
                player1_points, player2_points = 0, 0
                player1_cards, player2_cards = 0, 0
                current_pile = []

                k = 0
                while k <= len(shuffled_deck) - 3:
                    sequence = shuffled_deck[k:k+3]
                    current_pile += shuffled_deck[k:k+3]

                    if sequence == player1_hand:
                        if count_total_cards:
                            player1_cards += len(current_pile)
                            current_pile = []
                        else:
                            player1_points += 1
                        k += 3
                    elif sequence == player2_hand:
                        if count_total_cards:
                            player2_cards += len(current_pile)
                            current_pile = []
                        else:
                            player2_points += 1
                        k += 3
                    else:
                        k += 1

                if count_total_cards:
                    if player1_cards > player2_cards:
                        win_matrix[i, j] += 1
                        player1_wins += 1
                    elif player2_cards > player1_cards:
                        player2_wins += 1
                else:
                    if player1_points > player2_points:
                        win_matrix[i, j] += 1
                        player1_wins += 1
                    elif player2_points > player1_points:
                        player2_wins += 1

        return win_matrix, player1_wins, player2_wins
    
    # util function to convert all single quotes in the file with double quotes
    def convert_single_to_double_quotes(file_path):
        with open(file_path, 'r') as file:
            data = file.read()

        # Replace single quotes with double quotes
        data = data.replace("'", '"')

        with open(file_path, 'w') as file:
            file.write(data)
    
    # new function to load deck data from json file
    def load_deck_data_from_file(deck_data_file):
        # convert file into correct json format
        convert_single_to_double_quotes(deck_data_file)
        with open(deck_data_file, 'r') as f:
            deck_data = json.load(f)
        return deck_data

    def load_game_data(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                loaded_data = json.load(f)
                win_matrix = np.zeros((8, 8))
                win_data = loaded_data['win_data']
                total_rounds_played = loaded_data['total_rounds_played']

            hands = generate_hands()
            for i in range(len(hands)):
                for j in range(len(hands)):
                    p1_hand = binary_to_color_string(hands[i])
                    p2_hand = binary_to_color_string(hands[j])
                    combo_key = f"{p1_hand} vs {p2_hand}"
                    if combo_key in win_data:
                        win_matrix[i, j] = win_data[combo_key]

            return win_matrix, total_rounds_played
        else:
            return np.zeros((8, 8)), 0

    def save_game_data(file_path, win_matrix, hands, total_rounds_played):
        win_data = {}

        for i in range(len(hands)):
            for j in range(len(hands)):
                p1_hand = binary_to_color_string(hands[i])
                p2_hand = binary_to_color_string(hands[j])
                wins = win_matrix[i, j]
                win_data[f"{p1_hand} vs {p2_hand}"] = int(wins)

        data_to_save = {'win_data': win_data,
            'total_rounds_played': total_rounds_played}

        with open(file_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def load_deck_data(deck_file_path):
        if os.path.exists(deck_file_path):
            with open(deck_file_path, 'r') as f:
                loaded_deck_history = json.load(f)
                return loaded_deck_history
        else:
            return []

    def save_deck_data(deck_file_path, deck_history):
        with open(deck_file_path, 'w') as f:
            json.dump(deck_history, f)

    def load_wins_data(wins_file_path):
        if os.path.exists(wins_file_path):
            with open(wins_file_path, 'r') as f:
                loaded_wins = json.load(f)
                return loaded_wins['player1_wins'], loaded_wins['player2_wins']
        else:
            return 0, 0

    def save_wins_data(wins_file_path, player1_wins, player2_wins):
        with open(wins_file_path, 'w') as f:
            win_counts = {'player1_wins': player1_wins, 'player2_wins': player2_wins}
            json.dump(win_counts, f)

    hands = generate_hands()

    simulation_data = {}
    for i in [False, True]:
        if i:
            data_file_path = os.path.join(data_folder, 'game_data_total_cards.json')
            deck_file_path = os.path.join(data_folder, 'deck_history_total_cards.json')
            wins_file_path = os.path.join(data_folder, 'win_counts_total_cards.json')
        else:
            data_file_path = os.path.join(data_folder, 'game_data_tricks.json')
            deck_file_path = os.path.join(data_folder, 'deck_history_tricks.json')
            wins_file_path = os.path.join(data_folder, 'win_counts_tricks.json')

        overall_win_matrix, total_rounds_played = load_game_data(data_file_path)
        deck_history = load_deck_data(deck_file_path)
        player1_wins, player2_wins = load_wins_data(wins_file_path)

        simulation_data[i] = {
            'data_file': data_file_path,
            'deck_file': deck_file_path,
            'wins_file': wins_file_path,
            'overall_win_matrix': overall_win_matrix,
            'total_rounds_played': total_rounds_played,
            'deck_history': deck_history,
            'player1_wins': player1_wins,
            'player2_wins': player2_wins}
    
     # Load the deck data from file
    if deck_data_file:
        deck_data = load_deck_data_from_file(deck_data_file)
    else:
        raise ValueError("A deck data file must be provided!")

    # Ensure the number of rounds doesn't exceed the number of decks in the file
    if len(deck_data) < rounds:
        raise ValueError("Not enough decks in the provided file for the number of rounds!")

    
    # for _ in range(rounds):
    #     shuffled_deck = [1] * 26 + [0] * 26

    #     if random_seed is not None:
    #         random.seed(random_seed)

    #     random.shuffle(shuffled_deck)
    #     deck_string = binary_to_color_string(shuffled_deck)

    #     for i in [False, True]:
    #         sim_data = simulation_data[i]

    #         win_matrix, p1_wins, p2_wins = simulate_game(hands, shuffled_deck, i)

    #         sim_data['overall_win_matrix'] += win_matrix
    #         sim_data['player1_wins'] += p1_wins
    #         sim_data['player2_wins'] += p2_wins
    #         sim_data['total_rounds_played'] += 1
    #         sim_data['deck_history'].append(deck_string)

    # Temporary new scheme to use the decks already in the file
    # Start timing the simulation part
    simulation_start_time = time.time()

    for round_idx in range(rounds):
        # Use the deck from the file instead of generating a new one
        deck_string = deck_data[round_idx]
        shuffled_deck = [int(char) for char in deck_string]

        for i in [False, True]:
            sim_data = simulation_data[i]

            win_matrix, p1_wins, p2_wins = simulate_game(hands, shuffled_deck, i)

            sim_data['overall_win_matrix'] += win_matrix
            sim_data['total_rounds_played'] += 1
    
    # End timing
    simulation_end_time = time.time()
    simulation_duration = simulation_end_time - simulation_start_time
    print(f"Simulation time: {simulation_duration} seconds")


    for i in [False, True]:
        sim_data = simulation_data[i]

        save_game_data(sim_data['data_file'], sim_data['overall_win_matrix'], hands, sim_data['total_rounds_played'])
        save_deck_data(sim_data['deck_file'], sim_data['deck_history'])
        save_wins_data(sim_data['wins_file'], sim_data['player1_wins'], sim_data['player2_wins'])

if __name__ == "__main__":
    rounds = int(input('How many rounds would you like to simulate?\n'))
    seed_bool = input('Would you like to set a random seed? (Enter "yes" or "no")\n')
    # add an input prompt for the deck we want to use
    deck_data_file = input('Please enter the path to the deck data file:\n')
    if seed_bool == "yes":
        seed = int(input('What random seed would you like to use?\n'))
    else:
        seed = None
    print('Running simulation...')
    run_simulation(rounds = rounds, deck_data_file=deck_data_file, random_seed = seed)
