from random import choice, randint


class AutoShips:
    def __init__(self, offset: int) -> None:
        self.offset = offset
        self.available_blocks = {(x, y) for x in range(
            1 + self.offset, 11 + self.offset) for y in range(1, 11)}
        self.ships_set = set()
        self.ships = self.__populate_grid()
        self.orientation = None
        self.direction = None

    def __create_start_block(self, available_blocks: set[tuple]) -> tuple:
        self.orientation = randint(0, 1)
        # -1 is left or down, 1 is right or up
        self.direction = choice((-1, 1))
        x, y = choice(tuple(available_blocks))
        return x, y, self.orientation, self.direction

    def __create_ship(
            self,
            number_of_blocks: int,
            available_blocks: set[tuple]) -> list:
        ship_coordinates = []
        x, y, self.orientation, self.direction = self.__create_start_block(
            available_blocks)
        for _ in range(number_of_blocks):
            ship_coordinates.append((x, y))
            if not self.orientation:
                self.direction, x = self.__get_new_block_for_ship(
                    x, self.direction, self.orientation, ship_coordinates)
            else:
                self.direction, y = self.__get_new_block_for_ship(
                    y, self.direction, self.orientation, ship_coordinates)
        if self.__is_ship_valid(ship_coordinates):
            return ship_coordinates
        return self.__create_ship(number_of_blocks, available_blocks)

    def __get_new_block_for_ship(
            self,
            coor: int,
            direction: int,
            orientation: int,
            ship_coordinates: list) -> tuple:
        self.direction = direction
        self.orientation = orientation
        if (coor <= 1 -
            self.offset *
            (self.orientation -
             1) and self.direction == -
            1) or (coor >= 10 -
                   self.offset *
                   (self.orientation -
                    1) and self.direction == 1):
            self.direction *= -1
            return self.direction, ship_coordinates[0][self.orientation] + \
                self.direction
        return self.direction, ship_coordinates[-1][self.orientation] + \
            self.direction

    def __is_ship_valid(self, new_ship: list) -> bool:
        ship = set(new_ship)
        return ship.issubset(self.available_blocks)

    def __add_new_ship_to_set(self, new_ship: list) -> None:
        self.ships_set.update(new_ship)

    def __update_available_blocks_for_creating_ships(
            self, new_ship: list) -> None:
        for elem in new_ship:
            for k in range(-1, 2):
                for m in range(-1, 2):
                    if self.offset < (elem[0] + k) < 11 + \
                            self.offset and 0 < (elem[1] + m) < 11:
                        self.available_blocks.discard(
                            (elem[0] + k, elem[1] + m))

    def __populate_grid(self) -> list:
        ships_coordinates_list = []
        for number_of_blocks in range(4, 0, -1):
            for _ in range(5 - number_of_blocks):
                new_ship = self.__create_ship(
                    number_of_blocks, self.available_blocks)
                ships_coordinates_list.append(new_ship)
                self.__add_new_ship_to_set(new_ship)
                self.__update_available_blocks_for_creating_ships(new_ship)
        return ships_coordinates_list
