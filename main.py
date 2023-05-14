import copy
import sys
import pygame.mixer
import pygame

from autocomplete import AutoShips
from constants import (
    AUTO_BUTTON_PLACE,
    BLACK,
    BLOCK_SIZE,
    HOW_TO_CREATE_SHIPS_MESSAGE,
    LEFT_MARGIN,
    LETTERS,
    LIGHT_GRAY,
    MANUAL_BUTTON_PLACE,
    SETTINGS_BUTTON_PLACE,
    WINDSETT_BUTTON_PLACE,
    MESSAGE_RECT_COMPUTER,
    MESSAGE_RECT_HUMAN,
    PLAY_AGAIN_BUTTON_PLACE,
    PLAY_AGAIN_MESSAGE,
    RECT_FOR_COMPUTER_SHIPS_COUNT,
    RECT_FOR_GRIDS,
    RECT_FOR_HUMAN_SHIPS_COUNT,
    RECT_FOR_MESSAGES_AND_BUTTONS,
    SIZE,
    UNDO_BUTTON_PLACE,
    UPPER_MARGIN,
    WHITE,
    X_OFFSET_FOR_COMPUTER_SHIPS_COUNT,
    X_OFFSET_FOR_HUMAN_SHIPS_COUNT,
    Y_OFFSET_FOR_SHIPS_COUNT,
)
from lg import (
    around_last_computer_hit_set,
    check_hit_or_miss,
    computer_destroyed_ships_count,
    computer_shoots,
    destroyed_computer_ships,
    dotted_set,
    dotted_set_for_computer_not_to_shoot,
    hit_blocks,
    hit_blocks_for_computer_not_to_shoot,
    human_destroyed_ships_count,
    last_hits_list,
    update_used_blocks,
)
from grid import Grid
from button import Button
from slider import Slider
from drawing import (
    draw_from_dotted_set,
    draw_hit_blocks,
    draw_ships,
    font,
    game_over_font,
    print_destroyed_ships_count,
    screen,
    show_message_at_rect_center,
)
from manual_ships import manually_create_new_ship

pygame.init()
background_music = pygame.mixer.Sound("background_music.mp3")

def main():
    background_music.set_volume(0.5)
    background_music.play(-1)
    color_wind = WHITE
    color_text = BLACK
    game(color_wind, color_text)

def game(color_wind, color_text):
    background_music_value = background_music.get_volume()
    ships_creation_not_decided = True
    ships_not_created = True
    setting_wind_draw =True
    drawing = False
    game_over = False
    computer_turn = False
    start = (0, 0)
    ship_size = (0, 0)
    old_color_wind = color_wind
    old_color_text = color_text

    human_ships_to_draw = []
    human_ships_set = set()
    used_blocks_for_manual_drawing = set()
    num_ships_list = [0, 0, 0, 0]
    volume_slider = Slider(x_offset=100, y_offset=250, width=200, height=20, color=LIGHT_GRAY, handle_color=color_text, value = background_music_value)
    auto_button = Button(AUTO_BUTTON_PLACE, "AUTO", HOW_TO_CREATE_SHIPS_MESSAGE, font, color_text)
    manual_button = Button(MANUAL_BUTTON_PLACE, "MANUAL", HOW_TO_CREATE_SHIPS_MESSAGE, font, color_text)
    aplly_button = Button(AUTO_BUTTON_PLACE, "APLLY", "", font, color_text)
    back_button = Button(MANUAL_BUTTON_PLACE, "BACK","", font, color_text)
    settings_button = Button(SETTINGS_BUTTON_PLACE, "SETTINGS", HOW_TO_CREATE_SHIPS_MESSAGE, font, color_text)
    undo_button = Button(UNDO_BUTTON_PLACE, "UNDO LAST SHIP", "", font, color_text)
    play_again_button = Button(PLAY_AGAIN_BUTTON_PLACE, "PLAY AGAIN", PLAY_AGAIN_MESSAGE, font, color_text)
    quit_game_button = Button(MANUAL_BUTTON_PLACE, "QUIT", PLAY_AGAIN_MESSAGE, font, color_text)
    color_windset_button = Button(WINDSETT_BUTTON_PLACE, "DARK MODE","", font, color_text)
    screen.fill(color_wind)
    Grid(title="COMPUTER", offset=0, font=font, letters=LETTERS, line_color=color_text, text_color=color_text) 
    Grid(title="HUMAN", offset=15, font=font, letters=LETTERS, line_color=color_text, text_color=color_text) 
    computer = AutoShips(0)
    computer_ships_working = copy.deepcopy(computer.ships)
    old_background_music_value = background_music_value
    while ships_creation_not_decided:
        auto_button.draw(color_wind)
        manual_button.draw(color_wind)
        settings_button.draw(color_wind)
        auto_button.change_color_on_hover()
        settings_button.change_color_on_hover()
        manual_button.change_color_on_hover()
        auto_button.print_message(color_text)

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and auto_button.rect.collidepoint(mouse):
                human = AutoShips(15)
                human_ships_to_draw = human.ships
                human_ships_working = copy.deepcopy(human.ships)
                human_ships_set = human.ships_set
                setting_wind_draw = False
                ships_creation_not_decided = False
                ships_not_created = False
            elif event.type == pygame.MOUSEBUTTONDOWN and manual_button.rect.collidepoint(mouse):
                setting_wind_draw = False
                ships_creation_not_decided = False
            elif event.type == pygame.MOUSEBUTTONDOWN and settings_button.rect.collidepoint(mouse):
                ships_not_created = False
                around_last_computer_hit_set.clear()
                dotted_set_for_computer_not_to_shoot.clear()
                hit_blocks_for_computer_not_to_shoot.clear()
                last_hits_list.clear()
                hit_blocks.clear()
                dotted_set.clear()
                destroyed_computer_ships.clear()
                dotted_set.clear()
                hit_blocks.clear()
                ships_creation_not_decided = False
        pygame.display.update()
        screen.fill(color_wind, RECT_FOR_MESSAGES_AND_BUTTONS)

    while setting_wind_draw:
        color_windset_button.draw(color_wind)
        color_windset_button.change_color_on_hover()
        aplly_button.draw(color_wind)
        back_button.draw(color_wind)
        volume_slider.draw()
        aplly_button.change_color_on_hover()
        back_button.change_color_on_hover()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and color_windset_button.rect.collidepoint(mouse):
                if(color_wind == WHITE):
                   color_wind = BLACK
                   color_text = WHITE
                else:
                   color_wind = WHITE
                   color_text = BLACK
                aplly_button = Button(AUTO_BUTTON_PLACE, "APLLY", "", font, color_text)
                back_button = Button(MANUAL_BUTTON_PLACE, "BACK","", font, color_text)
                color_windset_button = Button(WINDSETT_BUTTON_PLACE, "DARK MODE","", font, color_text)
                volume_slider = Slider(x_offset=100, y_offset=250, width=200, height=20, color=LIGHT_GRAY, handle_color=color_text,  value = volume_slider.value)
            elif event.type == pygame.MOUSEBUTTONDOWN and volume_slider.rect.collidepoint(mouse):
                volume_slider.handle_event(event)
                volume_slider.dragging = True  # Установите флаг dragging в True при нажатии на ползунок
            elif event.type == pygame.MOUSEBUTTONUP and volume_slider.dragging:
                volume_slider.dragging = False
            elif event.type == pygame.MOUSEBUTTONDOWN and aplly_button.rect.collidepoint(mouse):
                ships_creation_not_decided = False
                game(color_wind, color_text)
            elif event.type == pygame.MOUSEBUTTONDOWN and back_button.rect.collidepoint(mouse):
                color_wind = old_color_wind
                color_text = old_color_text
                background_music.set_volume(old_background_music_value)
                ships_creation_not_decided = False
                game(color_wind, color_text)
            if volume_slider.dragging:
                mouse_x, _ = pygame.mouse.get_pos()
                volume_slider.update_value(mouse_x)
                background_music.set_volume(volume_slider.value)
        if volume_slider.dragging:
            mouse_x, _ = pygame.mouse.get_pos()
            volume_slider.move(mouse_x)
        pygame.display.update()
        screen.fill(color_wind)
        #if event.type == pygame.MOUSEBUTTONDOWN and settings_button_cancel.rect.collidepoint(mouse) or 
        #    event.type == pygame.MOUSEBUTTONDOWN and settings_button_save.rect.collidepoint(mouse):
        """
        buttons whith sett?? mb take 3 but 1. Color window 2. SOUNDS?????? 3.solo take colors!!!!! 
        """
         
    while ships_not_created:
        screen.fill(color_wind, RECT_FOR_GRIDS)
        Grid(title="COMPUTER", offset=0, font=font, letters=LETTERS, line_color=color_text, text_color=color_text)  # type: ignore
        Grid(title="HUMAN", offset=15, font=font, letters=LETTERS, line_color=color_text, text_color=color_text)
        undo_button.draw(color_wind)
        undo_button.print_message(color_wind)
        undo_button.change_color_on_hover()
        mouse = pygame.mouse.get_pos()
        if not human_ships_to_draw:
            undo_button.draw(color_wind,LIGHT_GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif undo_button.rect.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
                if human_ships_to_draw:
                    screen.fill(color_wind, RECT_FOR_MESSAGES_AND_BUTTONS)
                    deleted_ship = human_ships_to_draw.pop()
                    num_ships_list[len(deleted_ship) - 1] -= 1
                    update_used_blocks(ship=deleted_ship, method=used_blocks_for_manual_drawing.discard)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                x_start, y_start = event.pos
                start = x_start, y_start
                ship_size = (0, 0)
            elif drawing and event.type == pygame.MOUSEMOTION:
                x_end, y_end = event.pos
                ship_size = x_end - x_start, y_end - y_start
            elif drawing and event.type == pygame.MOUSEBUTTONUP:
                x_end, y_end = event.pos
                drawing = False
                ship_size = (0, 0)
                manually_create_new_ship(
                    human_ships_to_draw=human_ships_to_draw,
                    human_ships_set=human_ships_set,
                    used_blocks_for_manual_drawing=used_blocks_for_manual_drawing,
                    num_ships_list=num_ships_list,
                    x_start=x_start,
                    y_start=y_start,
                    x_end=x_end,
                    y_end=y_end,
                    background_color = color_wind,
                )
            if len(human_ships_to_draw) == 10:
                ships_not_created = False
                human_ships_working = copy.deepcopy(human_ships_to_draw)
                screen.fill(color_wind, RECT_FOR_MESSAGES_AND_BUTTONS)
        pygame.draw.rect(screen, color_text, (start, ship_size), 3)
        draw_ships(human_ships_to_draw,color_text)
        pygame.display.update()
    fired_blocks = set()

    while not game_over:
        screen.fill(color_wind, RECT_FOR_HUMAN_SHIPS_COUNT)
        screen.fill(color_wind, RECT_FOR_COMPUTER_SHIPS_COUNT)
        if not dotted_set | hit_blocks:
            show_message_at_rect_center("GAME STARTED! YOUR MOVE!", MESSAGE_RECT_COMPUTER,color_wind)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif not computer_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (LEFT_MARGIN < x < LEFT_MARGIN + 10 * BLOCK_SIZE) and (
                    UPPER_MARGIN < y < UPPER_MARGIN + 10 * BLOCK_SIZE
                ):
                    fired_block = ((x - LEFT_MARGIN) // BLOCK_SIZE + 1, (y - UPPER_MARGIN) // BLOCK_SIZE + 1)
                    if fired_block not in fired_blocks:
                        fired_blocks.add(fired_block)
                        computer_turn = not check_hit_or_miss(
                            fired_block=fired_block,
                            opponents_ships_list=computer_ships_working,
                            computer_turn=False,
                            opponents_ships_list_original_copy=computer.ships,
                            opponents_ships_set=computer.ships_set,
                            computer=computer,
                        )
                        draw_from_dotted_set(dotted_set, color_text)
                        draw_hit_blocks(hit_blocks, color_text)
                        screen.fill(color_wind, MESSAGE_RECT_COMPUTER)
                        show_message_at_rect_center(
                            f"Your last shot: {LETTERS[fired_block[0] - 1] + str(fired_block[1])}",
                            MESSAGE_RECT_COMPUTER, color_wind,
                        )
                    else:
                        screen.fill(color_wind, MESSAGE_RECT_COMPUTER)
                        show_message_at_rect_center("You already shoot in this block! Try again", MESSAGE_RECT_COMPUTER,color_wind)

                else:
                    show_message_at_rect_center("Your shot is outside of grid! Try again", MESSAGE_RECT_COMPUTER, color_wind)
        if computer_turn:
            fired_block = computer_shoots()
            computer_turn = check_hit_or_miss(
                fired_block=fired_block,
                opponents_ships_list=human_ships_working,
                computer_turn=True,
                opponents_ships_list_original_copy=human_ships_to_draw,
                opponents_ships_set=human_ships_set,
                computer=computer,
            )

            draw_from_dotted_set(dotted_set,color_text)
            draw_hit_blocks(hit_blocks,color_text)
            screen.fill(color_wind, MESSAGE_RECT_HUMAN)
            show_message_at_rect_center(
                f"Computer's last shot: {LETTERS[fired_block[0] - 16] + str(fired_block[1])}",
                MESSAGE_RECT_HUMAN, color_wind
            )
        draw_ships(destroyed_computer_ships,color_text)
        draw_ships(human_ships_to_draw,color_text)

        if not computer.ships_set:
            show_message_at_rect_center("YOU WIN!", (0, 0, SIZE[0], SIZE[1]),color_wind, game_over_font)
            game_over = True
        if not human_ships_set:
            show_message_at_rect_center("YOU LOSE!", (0, 0, SIZE[0], SIZE[1]),color_wind, game_over_font)
            game_over = True

        print_destroyed_ships_count(
            X_OFFSET_FOR_HUMAN_SHIPS_COUNT, Y_OFFSET_FOR_SHIPS_COUNT, human_destroyed_ships_count, font
        )
        print_destroyed_ships_count(
            X_OFFSET_FOR_COMPUTER_SHIPS_COUNT, Y_OFFSET_FOR_SHIPS_COUNT, computer_destroyed_ships_count, font
        )
        pygame.display.update()

    while game_over:
        screen.fill(color_wind,RECT_FOR_MESSAGES_AND_BUTTONS)
        play_again_button.draw(color_wind)
        play_again_button.print_message(color_text)
        play_again_button.change_color_on_hover()
        quit_game_button.draw(color_wind)
        quit_game_button.change_color_on_hover()

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and play_again_button.rect.collidepoint(mouse):
                around_last_computer_hit_set.clear()
                dotted_set_for_computer_not_to_shoot.clear()
                hit_blocks_for_computer_not_to_shoot.clear()
                last_hits_list.clear()
                hit_blocks.clear()
                dotted_set.clear()
                destroyed_computer_ships.clear()
                dotted_set.clear()
                hit_blocks.clear()
                game(color_wind, color_text)
            elif event.type == pygame.MOUSEBUTTONDOWN and quit_game_button.rect.collidepoint(mouse):
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    main()