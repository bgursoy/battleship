from layout.game_layout import Ui_MainWindow


class BattleShipGame:
    game_ui = Ui_MainWindow()
    ai_map = []
    player_map = []
    ai_ships = {"carrier": 5, "battleship": 4, "cruiser": 3, "submarine": 3, "destroyer": 2}
    player_ships = {"carrier": 5, "battleship": 4, "cruiser": 3, "submarine": 3, "destroyer": 2}
    current_player = "player"

    def __init__(self, player_map, ai_map):
        self.player_map = player_map
        self.ai_map = ai_map

    def shotACell(self, row, column):
        # Player attacks
        if self.current_player == "player":
            target = self.ai_map[row][column]
            # Checks if player hit a ship
            if target.occupied_ship:
                # Decrease of the number of cells of hit ships
                self.ai_ships[target.occupied_ship] -= 1
                # Checks if a ship sank
                if self.ai_ships[target.occupied_ship] == 0:
                    # Delete the ship in the ai_ships
                    self.ai_ships.pop(target.occupied_ship)
                return target.occupied_ship
            # If player missed current player changes
            else:
                self.current_player = "ai"
                return None

        # AI attacks
        elif self.current_player == "ai":
            target = self.player_map[row][column]
            # Checks if ai hit a ship
            if target.occupied_ship:
                # Decrease of the number of cells of hit ships
                self.player_ships[target.occupied_ship] -= 1
                # Checks if a ship sank
                if self.player_ships[target.occupied_ship] == 0:
                    # Delete the ship in the ai_ships
                    self.player_ships.pop(target.occupied_ship)
                return target.occupied_ship
            # If ai missed current player changes
            else:
                self.current_player = "player"
                return None
        else:
            print("Invalid player! Needs to be 'ai' or 'player'")
            return None
