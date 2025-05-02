# This file is runs a series of tests on the code to make sure it functions correctly
# I don't want to push flawed code onto the internet!

# Test cases are designed in the notebooks folder prior to being written here.
# To run a test, just do 'pytest' in the root folder

import b2sim.engine as b2

# Constant eco'ing of grouped blacks from Round 14 to Round 17
def test_basic_case():
    rounds = b2.Rounds(0.1)

    farms = [
        b2.initFarm(rounds.getTimeFromRound(7), upgrades = [3,2,0]),
        b2.initFarm(rounds.getTimeFromRound(13.9), upgrades = [3,2,0])
    ]

    initial_state_game = {
        'Cash': 0,
        'Eco': 800,
        'Eco Send': b2.ecoSend(send_name = 'Grouped Blacks'),
        'Rounds': rounds,
        'Farms': farms,
        'Game Round': 13.99
    }

    game_state = b2.GameState(initial_state_game)
    game_state.fastForward(target_round = 17)

    assert (game_state.cash == 1083.0) and (game_state.eco == 1391.0)

def test_eco_queue():
    rounds = b2.Rounds(info = [(1,9.5), (2,7), (10,5.75)], mode = 'Stall Times')

    buy_queue = [
        [b2.buyDefense(5600 - 0.7*2500, message="sell into hrp")], #Sell into HRP
        [b2.buyDefense(2550,min_buy_time=rounds.getTimeFromRound(14), message="buy l2g")] #Buy Lead to Gold
    ]

    eco_queue = [
        b2.ecoSend(time=rounds.getTimeFromRound(10), send_name='Grouped Reds'),
        b2.ecoSend(time=rounds.getTimeFromRound(12), send_name='Spaced Rainbows'),
        b2.ecoSend(time=rounds.getTimeFromRound(13), send_name='Zero'),
        b2.ecoSend(time=rounds.getTimeFromRound(14), send_name='Grouped Blacks')
    ]
    
    initial_state_game = {
        'Cash': 2800,
        'Eco': 700,
        'Rounds': rounds,
        'Game Round': 10,
        'Buy Queue': buy_queue,
        'Eco Queue': eco_queue
    }

    game_state = b2.GameState(initial_state_game)
    game_state.fastForward(target_round = 15)

    assert (game_state.cash == 24) and (game_state.eco == 955)