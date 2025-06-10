# These tests concern the eco queue correction system. 
# Ideally, users set well-defined simulations that do not require the eco queue correction system
# Eco queue correction is designed to edge cases in possibly ambiguously defined simulations, which is useful for optimization purposes.

# Test cases are designed in the notebooks folder prior to being written here.
# To run a test, just do 'pytest' in the root folder
import b2sim.engine as b2
import pytest

def test_eco_queue_correction_1():
    # This test concerns an example where the user tries to use eco sends long after they have become unavailable.

    expected_output = [5000, 1000]

    rounds = b2.Rounds(0.1)

    eco_queue = [
        b2.ecoSend(send_name='Grouped Reds', time = rounds.getTimeFromRound(14)),
        b2.ecoSend(send_name='Grouped Blues', time = rounds.getTimeFromRound(15)),
    ]

    initial_state_game = {
        'Cash': 0,
        'Eco': 1000,
        'Eco Queue': eco_queue,
        'Rounds': rounds, #Determines the lengths of the rounds in the game state
        'Game Round': 13.99
    }

    game_state = b2.GameState(initial_state_game)
    game_state.fastForward(target_round = 16)

    assert abs(game_state.cash - expected_output[0]) + abs(game_state.eco - expected_output[1]) < 0.01

def test_eco_queue_correction_2():
    # This test concerns an example where the user does not designate an eco send to use at simulation start.
    # The code should be able to infer that the user wants to use the 'Zero' send from simluation start to Round 15.
    
    expected_output = [2286.3999999999933,1116.799999999995]

    rounds = b2.Rounds(0.1)

    eco_queue = [
        b2.ecoSend(send_name='Grouped Yellows', time = rounds.getTimeFromRound(15))
    ]

    initial_state_game = {
        'Cash': 0,
        'Eco': 1000,
        'Eco Queue': eco_queue,
        'Rounds': rounds, #Determines the lengths of the rounds in the game state
        'Game Round': 13.99
    }

    game_state = b2.GameState(initial_state_game)
    game_state.fastForward(target_round = 16)

    assert abs(game_state.cash - expected_output[0]) + abs(game_state.eco - expected_output[1]) < 0.01