import pytest
from unittest import mock
from autocomplete import AutoShips
from manual_ships import manually_create_new_ship
from lg import check_hit_or_miss, computer_shoots, update_used_blocks
from constants import (
    BLOCK_SIZE,
    LEFT_MARGIN,
    RECT_FOR_MESSAGES_AND_BUTTONS,
    UPPER_MARGIN,
    WHITE,
)
from drawing import screen, show_message_at_rect_center
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
    x_start, y_start = 1, 1
    x_end, y_end = 4, 1
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
    start_block = ((x_start - LEFT_MARGIN) // BLOCK_SIZE + 1, (y_start - UPPER_MARGIN) // BLOCK_SIZE + 1)
    end_block = ((x_end - LEFT_MARGIN) // BLOCK_SIZE + 1, (y_end - UPPER_MARGIN) // BLOCK_SIZE + 1)
    if start_block > end_block:
        start_block, end_block = end_block, start_block
    temp_ship = []
    if 15 < start_block[0] < 26 and 0 < start_block[1] < 11 and 15 < end_block[0] < 26 and 0 < end_block[1] < 11:
        temp_ship = create_new_ship(start_block, end_block, background_color)
    else:
        show_message_at_rect_center("SHIP IS BEYOND YOUR GRID! Try again!", RECT_FOR_MESSAGES_AND_BUTTONS,
                                    background_color)
    if temp_ship:
        validate_and_save_new_ship(
            human_ships_to_draw, human_ships_set, used_blocks_for_manual_drawing, num_ships_list, temp_ship,
            background_color
        )

    assert len(human_ships_to_draw) == 1

def test_check_hit_or_miss():
    # Create a test scenario
    fired_block = (1, 1)
    opponents_ships_list = [[(1, 1), (1, 2), (1, 3)]]
    computer_turn = False
    opponents_ships_list_original_copy = [[(1, 1), (1, 2), (1, 3)]]
    opponents_ships_set = {(1, 1), (1, 2), (1, 3)}
    computer = mock.Mock()
    # Call the function to be tested
    result = check_hit_or_miss(
        fired_block=fired_block,        opponents_ships_list=opponents_ships_list,
        computer_turn=computer_turn,        opponents_ships_list_original_copy=opponents_ships_list_original_copy,
     opponents_ships_set=opponents_ships_set,        computer=computer,
    )
    # Assertions
    assert result is True
    assert opponents_ships_list == [[(1, 2), (1, 3)]]
    assert opponents_ships_set == {(1, 2), (1, 3)}
    assert computer.update_hit_blocks.call_count == 1

def test_computer_shoots(mock_autoships, mock_grid):    # Create a test scenario
    computer = mock.Mock()
    computer_turn = True
    opponents_ships_list = [[(1, 1), (1, 2), (1, 3)]]
    opponents_ships_set = {(1, 1), (1, 2), (1, 3)}
    human_ships_set = {(2, 1), (2, 2)}
    human_ships_list = [[(2, 1), (2, 2)]]
    # Call the function to be tested
    computer_shoots(        computer=computer,
        computer_turn=computer_turn,        opponents_ships_list=opponents_ships_list,
        opponents_ships_set=opponents_ships_set,        human_ships_set=human_ships_set,
        human_ships_list=human_ships_list,        background_color='black',
    )
    # Assertions
    assert computer.make_a_guess.call_count == 1
    assert computer.update_miss_blocks.call_count == 1
    assert computer.update_hit_blocks.call_count == 0
    assert mock_grid.draw_hits_misses.call_count == 1

def test_update_used_blocks():    # Create a test scenario
    used_blocks_for_manual_drawing = set()
    x_start, y_start = 1, 1
    x_end, y_end = 5, 1
    # Call the function to be tested
    update_used_blocks(
        used_blocks_for_manual_drawing=used_blocks_for_manual_drawing,        x_start=x_start,
        y_start=y_start,        x_end=x_end,
        y_end=y_end,    )
    # Assertions
    assert used_blocks_for_manual_drawing == {(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)}