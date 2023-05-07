from random import choice
from typing import Callable

from autocomplete import AutoShips

computer_available_to_fire_set = {(x, y) for x in range(16, 26) for y in range(1, 11)}
around_last_computer_hit_set = set()

dotted_set_for_computer_not_to_shoot = set()
hit_blocks_for_computer_not_to_shoot = set()
last_hits_list = []

hit_blocks = set()
dotted_set = set()
destroyed_computer_ships = []

human_destroyed_ships_count = {4: 0, 3: 0, 2: 0, 1: 0, "#": 0}
computer_destroyed_ships_count = {4: 0, 3: 0, 2: 0, 1: 0, "#": 0}


def computer_shoots() -> tuple:
    global computer_available_to_fire_set
    if not computer_available_to_fire_set:
        computer_available_to_fire_set = {(x, y) for x in range(16, 26) for y in range(1, 11)}

    set_to_shoot_from = computer_available_to_fire_set
    if around_last_computer_hit_set:
        set_to_shoot_from = around_last_computer_hit_set
    computer_fired_block = choice(tuple(set_to_shoot_from))
    computer_available_to_fire_set.discard(computer_fired_block)
    return computer_fired_block


def check_hit_or_miss(
    *,
    fired_block: tuple,
    opponents_ships_list: list[list],
    computer_turn: bool,
    opponents_ships_list_original_copy: list,
    opponents_ships_set: set,
    computer: AutoShips,
) -> bool:
    for elem in opponents_ships_list:
        diagonal_only = True
        if fired_block in elem:
            ind = opponents_ships_list.index(elem)
            if len(elem) == 1:
                diagonal_only = False
            update_dotted_and_hit_sets(
                fired_block=fired_block,
                computer_turn=computer_turn,
                diagonal_only=diagonal_only,
            )
            elem.remove(fired_block)
            opponents_ships_set.discard(fired_block)
            if computer_turn:
                last_hits_list.append(fired_block)
                update_around_last_computer_hit(
                    fired_block=fired_block,
                    computer_hits=True,
                )
            if not elem:
                update_destroyed_ships(
                    ind=ind,
                    computer_turn=computer_turn,
                    opponents_ships_list_original_copy=opponents_ships_list_original_copy,
                )
                if computer_turn:
                    last_hits_list.clear()
                    around_last_computer_hit_set.clear()
                else:
                    destroyed_computer_ships.append(computer.ships[ind])
            return True
    add_missed_block_to_dotted_set(
        fired_block=fired_block,
    )
    if computer_turn:
        update_around_last_computer_hit(
            fired_block=fired_block,
            computer_hits=False,
        )
    return False


def update_destroyed_ships(
    *,
    ind: int,
    computer_turn: bool,
    opponents_ships_list_original_copy: list,
) -> None:
    ship = sorted(opponents_ships_list_original_copy[ind])
    for i in range(-1, 1):
        update_dotted_and_hit_sets(
            fired_block=ship[i],
            computer_turn=computer_turn,
            diagonal_only=False,
        )
    if computer_turn:
        human_destroyed_ships_count[len(ship)] += 1
        human_destroyed_ships_count["#"] += 1
    else:
        computer_destroyed_ships_count[len(ship)] += 1
        computer_destroyed_ships_count["#"] += 1


def update_around_last_computer_hit(
    *,
    fired_block: tuple,
    computer_hits: bool,
) -> None:
    global around_last_computer_hit_set, computer_available_to_fire_set
    if computer_hits and fired_block in around_last_computer_hit_set:
        around_last_computer_hit_set = computer_hits_twice()
    elif computer_hits and fired_block not in around_last_computer_hit_set:
        computer_first_hit(fired_block=fired_block)
    elif not computer_hits:
        around_last_computer_hit_set.discard(fired_block)

    around_last_computer_hit_set -= dotted_set_for_computer_not_to_shoot
    around_last_computer_hit_set -= hit_blocks_for_computer_not_to_shoot
    computer_available_to_fire_set -= around_last_computer_hit_set
    computer_available_to_fire_set -= dotted_set_for_computer_not_to_shoot


def computer_first_hit(*, fired_block: tuple) -> None:
    x_hit, y_hit = fired_block
    if x_hit > 16:
        around_last_computer_hit_set.add((x_hit - 1, y_hit))
    if x_hit < 25:
        around_last_computer_hit_set.add((x_hit + 1, y_hit))
    if y_hit > 1:
        around_last_computer_hit_set.add((x_hit, y_hit - 1))
    if y_hit < 10:
        around_last_computer_hit_set.add((x_hit, y_hit + 1))


def computer_hits_twice() -> set:
    last_hits_list.sort()
    new_around_last_hit_set = set()
    for i in range(len(last_hits_list) - 1):
        x1 = last_hits_list[i][0]
        x2 = last_hits_list[i + 1][0]
        y1 = last_hits_list[i][1]
        y2 = last_hits_list[i + 1][1]
        if x1 == x2:
            if y1 > 1:
                new_around_last_hit_set.add((x1, y1 - 1))
            if y2 < 10:
                new_around_last_hit_set.add((x1, y2 + 1))
        elif y1 == y2:
            if x1 > 16:
                new_around_last_hit_set.add((x1 - 1, y1))
            if x2 < 25:
                new_around_last_hit_set.add((x2 + 1, y1))
    return new_around_last_hit_set


def update_dotted_and_hit_sets(
    *,
    fired_block: tuple,
    computer_turn: bool,
    diagonal_only: bool = True,
) -> None:
    global dotted_set, hit_blocks
    x, y = fired_block
    a = 15 * computer_turn
    b = 11 + 15 * computer_turn
    hit_blocks_for_computer_not_to_shoot.add(fired_block)
    hit_blocks.add(fired_block)
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (not diagonal_only or i != 0 and j != 0) and a < x + i < b and 0 < y + j < 11:
                add_missed_block_to_dotted_set(fired_block=(x + i, y + j))
    dotted_set -= hit_blocks


def add_missed_block_to_dotted_set(*, fired_block: tuple) -> None:
    dotted_set.add(fired_block)
    dotted_set_for_computer_not_to_shoot.add(fired_block)


def is_ship_valid(*, ship_set: set, blocks_for_manual_drawing: set) -> bool:
    return ship_set.isdisjoint(blocks_for_manual_drawing)


def validate_ships_numbers(*, ship: list, num_ships_list: list) -> bool:
    return (5 - len(ship)) > num_ships_list[len(ship) - 1]


def update_used_blocks(*, ship: list, method: Callable) -> None:
    for block in ship:
        for i in range(-1, 2):
            for j in range(-1, 2):
                method((block[0] + i, block[1] + j))