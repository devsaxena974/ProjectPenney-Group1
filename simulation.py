import random
import numpy as np

def game_simulation_with_probabilities(rounds=10000, total_cards=False):


    def create_hands():
        sequences = []
        for i in range(8):
            seq = [(i >> j) & 1 for j in range(2, -1, -1)]
            sequences.append(seq)
        return sequences


    def binary_to_string(seq):
        return ''.join(['R' if bit == 1 else 'B' for bit in seq])


    def game_simulation(sequences, deck, total_cards=False):
        win_matrix = np.zeros((8, 8))

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
                    elif cards_player_2 > cards_player_1:
                        win_matrix[i, j] += 0
                else:
                    if points_player_1 > points_player_2:
                        win_matrix[i, j] += 1
                    elif points_player_2 > points_player_1:
                        win_matrix[i, j] += 0

        return win_matrix


    sequences = create_hands()
    overall_win_matrix = np.zeros((8, 8))
    deck_history = []

    for _ in range(rounds):
        deck = [1] * 26 + [0] * 26
        random.shuffle(deck)

        deck_history.append(deck)


        win_matrix = game_simulation(sequences, deck, total_cards)
        overall_win_matrix += win_matrix

    win_probabilities = overall_win_matrix / rounds

    print("Winning probabilities for each sequence combination (Player 1 vs Player 2):\n")
    for i in range(len(sequences)):
        for j in range(len(sequences)):
            p1_seq = binary_to_string(sequences[i])
            p2_seq = binary_to_string(sequences[j])
            probability = win_probabilities[i, j]
            print(f"Player 1: {p1_seq} vs Player 2: {p2_seq} --> Probability that Player 1 wins: {probability:.5f}")

    print("\nDeck history for each round (binary 0s and 1s for Black and Red):\n")
    for round_num, deck in enumerate(deck_history, start=1):
        print(f"Round {round_num}: {deck}")


game_simulation_with_probabilities(rounds=3000, total_cards=False)