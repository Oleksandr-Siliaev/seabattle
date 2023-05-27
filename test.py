import pytest
import pygame
from unittest import mock
from autocomplete import AutoShips
from manual_ships import manually_create_new_ship
from lg import check_hit_or_miss, computer_shoots, update_used_blocks
# Mocking the necessary objects
@pytest.fixture
def mock_autoships():
    return mock.create_autospec(AutoShips)
@pytest.fixture
def mock_grid():
    return mock.Mock()

def test_manually_create_new_ship(mock_autoships, mock_grid):    # Create a test scenario
    # Create a test scenario
    human_ships_to_draw = []
    human_ships_set = set()
    used_blocks_for_manual_drawing = set()
    num_ships_list = [0, 0, 0, 0]
    x_start, y_start = 1065 , 416
    x_end, y_end = 1235, 440
    background_color = 'black'

    # Call the function to be tested
    manually_create_new_ship(
        human_ships_to_draw=human_ships_to_draw,
        human_ships_set=human_ships_set,
        used_blocks_for_manual_drawing=used_blocks_for_manual_drawing,
        num_ships_list=num_ships_list,
        x_start=x_start,
        y_start=y_start,
        x_end=x_end,
        y_end=y_end,
        background_color=background_color,
    )

    # Assertions
    assert len(human_ships_to_draw) == 1

def test_check_hit_or_miss():
    # Create a test scenario
    fired_block = (23, 3)
    opponents_ships_list = [[(23, 3), (23, 4), (23, 5), (23, 6)], [(22, 1), (21, 1), (20, 1)], [(19, 10), (18, 10), (17, 10)], [(20, 8), (20, 7)], [(17, 4), (16, 4)], [(25, 5), (25, 6)], [(24, 1)], [(17, 6)], [(18, 2)]]
    computer_turn = True
    opponents_ships_list_original_copy = [[(23, 3), (23, 4), (23, 5), (23, 6)], [(22, 1), (21, 1), (20, 1)], [(19, 10), (18, 10), (17, 10)], [(20, 8), (20, 7)], [(17, 4), (16, 4)], [(25, 5), (25, 6)], [(24, 1)], [(17, 6)], [(18, 2)], [(21, 3)]]
    opponents_ships_set = {(23, 4), (20, 8), (17, 6), (16, 4), (22, 1), (18, 10), (20, 1), (20, 7), (21, 3), (23, 3), (23, 6), (24, 1), (25, 6), (23, 5), (17, 4), (17, 10), (19, 10), (25, 5), (18, 2), (21, 1)}
    computer = mock.Mock()
    # Call the function to be tested
    result = check_hit_or_miss(
        fired_block=fired_block,        opponents_ships_list=opponents_ships_list,
        computer_turn=computer_turn,        opponents_ships_list_original_copy=opponents_ships_list_original_copy,
     opponents_ships_set=opponents_ships_set,        computer=computer,
    )
    # Assertions
    assert result is True
    assert opponents_ships_list == [[(23, 4), (23, 5), (23, 6)], [(22, 1), (21, 1), (20, 1)], [(19, 10), (18, 10), (17, 10)], [(20, 8), (20, 7)], [(17, 4), (16, 4)], [(25, 5), (25, 6)], [(24, 1)], [(17, 6)], [(18, 2)]]
    assert opponents_ships_set == { (20, 8), (17, 6), (16, 4), (22, 1), (18, 10), (20, 1), (20, 7), (21, 3), (23, 4), (23, 6), (24, 1), (25, 6), (23, 5), (17, 4), (17, 10), (19, 10), (25, 5), (18, 2), (21, 1)}
def test_computer_shoots(mock_autoships, mock_grid):    # Create a test scenario

    fire_block = computer_shoots()
    # Assertions
    assert fire_block != None

def test_update_used_blocks():    # Create a test scenario
    human_ships_to_draw = []
    human_ships_set = set()
    used_blocks_for_manual_drawing = set()
    num_ships_list = [0, 0, 0, 0]
    x_start, y_start = 1065, 416
    x_end, y_end = 1235, 440
    background_color = 'black'

    # Call the function to be tested
    manually_create_new_ship(
        human_ships_to_draw=human_ships_to_draw,
        human_ships_set=human_ships_set,
        used_blocks_for_manual_drawing=used_blocks_for_manual_drawing,
        num_ships_list=num_ships_list,
        x_start=x_start,
        y_start=y_start,
        x_end=x_end,
        y_end=y_end,
        background_color=background_color,
    )

    # Call the function to be tested
    last_ship = list(human_ships_to_draw.pop())
    update_used_blocks(ship = last_ship, method= used_blocks_for_manual_drawing.discard)
    # Assertions
    assert len(human_ships_to_draw) == 0

