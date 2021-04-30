import random


class BattleshipAI:
    ai_map = []
    ai_ships = {"destroyer": 2, "submarine": 3, "cruiser": 3, "battleship": 4, "carrier": 5}
    heuristic_map = []

    def __init__(self, game):
        self.game = game
        self.ai_map = game.ai_map
        self.enemy_ship_count = len(self.game.player_ships)
        # Create a map for ai to better guess for occupied player ships cells
        for i in range(10):
            heuristic_row = []
            for j in range(10):
                heuristic_row.append(1)
            self.heuristic_map.append(heuristic_row)

    def placeShips(self):
        # Pick a random location for a ship
        # Pick an orientation
        # If not suits, try again
        complete = False  # Control variable
        while not complete:
            # Selects ships one by one
            ship_item = self.ai_ships.popitem()
            ship_name = ship_item[0]
            ship_length = ship_item[1]
            # Ships direction
            orientation = random.randint(0, 1)
            # Selects random position
            row = random.randint(0, 9)
            column = random.randint(0, 9)
            target = self.ai_map[row][column]

            # Check if target has a valid position
            if orientation == 1:
                # Horizontal
                if column > 10 - ship_length:
                    self.ai_ships[ship_name] = ship_length
                    continue
                # Checks if there is a collision with another ship
                collision = False  # Control variable
                for i in range(ship_length):
                    neighbor = self.ai_map[row][column + i]
                    if neighbor.getOccupiedShip():
                        self.ai_ships[ship_name] = ship_length
                        collision = True

                if collision:
                    continue

            else:
                # Vertical
                if row > 10 - ship_length:
                    self.ai_ships[ship_name] = ship_length
                    continue

                collision = False
                for i in range(ship_length):
                    neighbor = self.ai_map[row + i][column]
                    if neighbor.getOccupiedShip():
                        collision = True
                        self.ai_ships[ship_name] = ship_length

                if collision:
                    continue

            # Ship can be placed
            if orientation == 1:
                # Horizontal
                target.setOccupiedShip(ship_name)

                for length in range(ship_length):
                    neighbor = self.ai_map[row][column + length]
                    neighbor.setOccupiedShip(ship_name)
                print("AI placed (H)", ship_name)

            else:
                # vertical
                target.setOccupiedShip(ship_name)
                for length in range(ship_length):
                    neighbor = self.ai_map[row + length][column]
                    neighbor.setOccupiedShip(ship_name)
                print("AI placed (V)", ship_name)

            if len(self.ai_ships) == 0:  # All the ships are placed to the AI map
                complete = True
                break

    # AI selects a cell
    def guessTarget(self):
        # Check all values on heuristic map and pick the cell that has highest heuristic value.
        # List for the cells that has the same maximum value
        options = []
        max_value = -1
        # Search for the highest value
        for i in range(10):
            for j in range(10):
                var = self.heuristic_map[i][j]
                if var > max_value:
                    # Found a higher value, update maximum value
                    max_value = var
                    # Clear old options
                    options.clear()
                    # Add location to the options
                    options.append((i, j))
                elif var == max_value:
                    # Add other alternatives that has the same value to the options
                    options.append((i, j))

        # Pick a random option
        option_index = random.randint(0, len(options) - 1)
        return options[option_index]

    def aiShot(self):
        # Make a guess, get location
        coordinate = self.guessTarget()
        row = coordinate[0]
        column = coordinate[1]

        print("AI makes shot: ", row, column)
        target_cell = self.game.player_map[row][column]
        check = self.game.shotACell(row, column)
        # Set heuristic value to negative in order to prevent selecting same position at the future
        self.heuristic_map[row][column] = -10

        if check:
            # Shot a ship
            print("AI shot a ", check)
            target_cell.setHit()
            # If enemy ship is not sank, increase heuristic value for neighboring cells,
            # that means the probability of being occupied by a ship for neighboring cells are increased
            if self.enemy_ship_count == len(self.game.player_ships):
                # The value for positions next to the target position by 1 cell are increased by 0.5
                if row < 9:
                    self.heuristic_map[row + 1][column] += 0.5
                if row > 0:
                    self.heuristic_map[row - 1][column] += 0.5
                if column < 9:
                    self.heuristic_map[row][column + 1] += 0.5
                if column > 0:
                    self.heuristic_map[row][column - 1] += 0.5

                # The value for positions next to the target position by 2 cells are increased by 0.25
                if row < 8:
                    self.heuristic_map[row + 2][column] += 0.25
                if row > 1:
                    self.heuristic_map[row - 2][column] += 0.25
                if column < 8:
                    self.heuristic_map[row][column + 2] += 0.25
                if column > 1:
                    self.heuristic_map[row][column - 2] += 0.25

                # The value for positions next to the target position by 3 cells are increased by 0.10
                if row < 7:
                    self.heuristic_map[row + 3][column] += 0.10
                if row > 2:
                    self.heuristic_map[row - 3][column] += 0.10
                if column < 7:
                    self.heuristic_map[row][column + 3] += 0.10
                if column > 2:
                    self.heuristic_map[row][column - 3] += 0.10
            else:
                # Reset heuristic map if an enemy ship is sank
                self.resetHeuristicMap()
                self.enemy_ship_count -= 1

        else:
            print("AI missed")
            target_cell.setMiss()

        if self.game.current_player == "ai":
            self.aiShot()

    # Clear heuristic map
    def resetHeuristicMap(self):
        for i in range(10):
            for j in range(10):
                if self.heuristic_map[i][j] < 0:
                    self.heuristic_map[i][j] = -10
                else:
                    self.heuristic_map[i][j] = 1
