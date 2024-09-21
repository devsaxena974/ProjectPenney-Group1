import os
import numpy as np
import json
import random

def game_simulation_with_probabilities(rounds=1000, random_seed=None):
    
    data_directory = 'data'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    
    def create_hands():
        sequences = []
        for i in range(8):
            seq = [(i >> j) & 1 for j in range(2, -1, -1)]
            sequences.append(seq)
        return sequences

    def binary_to_string(seq):
        return ''.join(['R' if bit == 1 else 'B' for bit in seq])

    def deck_to_string(deck):
        return ''.join(['R' if card == 1 else 'B' for card in deck])

    
    def game_simulation(sequences, deck, total_cards):
        win_matrix = np.zeros((8, 8))
        player1_wins = 0
        player2_wins = 0

        for i, player1_seq in enumerate(sequences):
            for j, player2_seq in enumerate(sequences):
                points_player_1, points_player_2 = 0, 0
                cards_player_1, cards_player_2 = 0, 0
                card_pile = []

                k = 0
                while k <= len(deck) - 3:
                    current_sequence = deck[k:k+3]
                    card_pile += deck[k:k+3]

                    if current_sequence == player1_seq:
                        if total_cards:
                            cards_player_1 += len(card_pile)
                            card_pile = []
                        else:
                            points_player_1 += 1
                        k += 3
                    elif current_sequence == player2_seq:
                        if total_cards:
                            cards_player_2 += len(card_pile)
                            card_pile = []
                        else:
                            points_player_2 += 1
                        k += 3
                    else:
                        k += 1

                if total_cards:
                    if cards_player_1 > cards_player_2:
                        win_matrix[i, j] += 1
                        player1_wins += 1
                    elif cards_player_2 > cards_player_1:
                        player2_wins += 1
                else:
                    if points_player_1 > points_player_2:
                        win_matrix[i, j] += 1
                        player1_wins += 1
                    elif points_player_2 > points_player_1:
                        player2_wins += 1

        return win_matrix, player1_wins, player2_wins

    
    def load_data(file):
        if os.path.exists(file):
            with open(file, 'r') as f:
                data = json.load(f)
                win_matrix = np.zeros((8, 8))
                win_data = data['win_data']
                total_rounds_played = data['total_rounds_played']

            sequences = create_hands()
            for i in range(len(sequences)):
                for j in range(len(sequences)):
                    p1_seq = binary_to_string(sequences[i])
                    p2_seq = binary_to_string(sequences[j])
                    combo_key = f"{p1_seq} vs {p2_seq}"
                    if combo_key in win_data:
                        win_matrix[i, j] = win_data[combo_key]

            return win_matrix, total_rounds_played
        else:
            return np.zeros((8, 8)), 0

    
    def save_data(file, win_matrix, sequences, total_rounds_played):
        win_data = {}

        for i in range(len(sequences)):
            for j in range(len(sequences)):
                p1_seq = binary_to_string(sequences[i])
                p2_seq = binary_to_string(sequences[j])
                wins = win_matrix[i, j]
                win_data[f"{p1_seq} vs {p2_seq}"] = int(wins)

        data = {
            'win_data': win_data,
            'total_rounds_played': total_rounds_played
        }

        with open(file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_deck_history(deck_file):
        if os.path.exists(deck_file):
            with open(deck_file, 'r') as f:
                deck_history = json.load(f)
                return deck_history
        else:
            return []

    def save_deck_history(deck_file, deck_history):
        with open(deck_file, 'w') as f:
            json.dump(deck_history, f)

    def load_win_counts(win_counts_file):
        if os.path.exists(win_counts_file):
            with open(win_counts_file, 'r') as f:
                win_counts = json.load(f)
                return win_counts['player1_wins'], win_counts['player2_wins']
        else:
            return 0, 0

    def save_win_counts(win_counts_file, player1_wins, player2_wins):
        with open(win_counts_file, 'w') as f:
            win_counts = {
                'player1_wins': player1_wins,
                'player2_wins': player2_wins
            }
            json.dump(win_counts, f)

    sequences = create_hands()

    
    data = {}
    for total_cards in [False, True]:
        if total_cards:
            data_file = os.path.join(data_directory, 'game_data_total_cards.json')
            deck_file = os.path.join(data_directory, 'deck_history_total_cards.json')
            win_counts_file = os.path.join(data_directory, 'win_counts_total_cards.json')
        else:
            data_file = os.path.join(data_directory, 'game_data_tricks.json')
            deck_file = os.path.join(data_directory, 'deck_history_tricks.json')
            win_counts_file = os.path.join(data_directory, 'win_counts_tricks.json')

        overall_win_matrix, total_rounds_played = load_data(data_file)
        deck_history = load_deck_history(deck_file)
        player1_wins, player2_wins = load_win_counts(win_counts_file)

        data[total_cards] = {
            'data_file': data_file,
            'deck_file': deck_file,
            'win_counts_file': win_counts_file,
            'overall_win_matrix': overall_win_matrix,
            'total_rounds_played': total_rounds_played,
            'deck_history': deck_history,
            'player1_wins': player1_wins,
            'player2_wins': player2_wins
        }

    
    for _ in range(rounds):
        deck = [1] * 26 + [0] * 26

        if random_seed is not None:
            random.seed(random_seed)

        random.shuffle(deck)
        deck_string = deck_to_string(deck)

        for total_cards in [False, True]:
            d = data[total_cards]

            win_matrix, p1_wins, p2_wins = game_simulation(sequences, deck, total_cards)

            d['overall_win_matrix'] += win_matrix
            d['player1_wins'] += p1_wins
            d['player2_wins'] += p2_wins
            d['total_rounds_played'] += 1
            d['deck_history'].append(deck_string)

    for total_cards in [False, True]:
        d = data[total_cards]

        save_data(d['data_file'], d['overall_win_matrix'], sequences, d['total_rounds_played'])
        save_deck_history(d['deck_file'], d['deck_history'])
        save_win_counts(d['win_counts_file'], d['player1_wins'], d['player2_wins'])

game_simulation_with_probabilities(rounds=2000)
