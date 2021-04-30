from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ai.battleship_ai import BattleshipAI
from game.battleship import BattleShipGame
from game.cell import Cell
from layout.game_layout import Ui_MainWindow


class GameWindow:
    game_ui = Ui_MainWindow()
    player_map = []
    ai_map = []

    def __init__(self, player_map):
        self.win = QMainWindow()
        self.game_ui.setupUi(self.win)
        self.win.setWindowTitle("Battleship Game")

        # Set player map
        self.player_map = player_map

        # Generate AI Map and add cells to the grid pane
        for row in range(10):
            ai_map_row = []
            for column in range(10):
                # Create AI cell
                aiButton = Cell(row, column, self)
                ai_map_row.append(aiButton)
                self.game_ui.aiGrid.addWidget(aiButton, row, column)

                # Get player cell from player map
                playerButton = player_map[row][column]
                playerButton.setNeutral()
                self.game_ui.playerGrid.addWidget(playerButton, row, column)

            self.ai_map.append(ai_map_row)

        # Init game
        self.game = BattleShipGame(self.player_map, self.ai_map)

        # Init AI
        self.ai = BattleshipAI(self.game)
        self.ai.placeShips()

    # Triggered when a cell on a AI Map clicked by player
    def actionCellClick(self, target_cell):
        # Get target location
        row = target_cell.row
        column = target_cell.column
        print(self.game.current_player, " makes a shot to: ", row, column)

        # Shot a cell on game object
        hit_ship = self.game.shotACell(row, column)

        if hit_ship:
            # Hit a ship
            print("Player shot a ", hit_ship)
            # Change cell color style
            target_cell.setHit()
            # Update remaining ships panel
            self.updateShipPanel()
            # Check if game is over
            self.isGameOver()

        else:
            print("Player missed")
            target_cell.setMiss()

        # If player missed shot, current player is set to the ai
        # AI makes shot
        if self.game.current_player == "ai":
            self.ai.aiShot()
            self.updateShipPanel()
            self.isGameOver()

    def isGameOver(self):
        # Check if all ships are sank for any player
        if len(self.game.player_ships) == 0:
            reply = QMessageBox.warning(self.win, "Error", "AI Won the game!", QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.win.close()
        elif len(self.game.ai_ships) == 0:
            reply = QMessageBox.warning(self.win, "Error", "Player Won the game!", QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.win.close()

    # Disable the sank ship images
    def updateShipPanel(self):
        p_ships = self.game.player_ships.keys()
        a_ships = self.game.ai_ships.keys()

        if "carrier" not in p_ships:
            self.game_ui.playerCarrier.setEnabled(False)
        if "battleship" not in p_ships:
            self.game_ui.playerBattleship.setEnabled(False)
        if "cruiser" not in p_ships:
            self.game_ui.playerCruiser.setEnabled(False)
        if "submarine" not in p_ships:
            self.game_ui.playerSubmarine.setEnabled(False)
        if "destroyer" not in p_ships:
            self.game_ui.playerDestroyer.setEnabled(False)

        if "carrier" not in a_ships:
            self.game_ui.aiCarrier.setEnabled(False)
        if "battleship" not in a_ships:
            self.game_ui.aiBattleship.setEnabled(False)
        if "cruiser" not in a_ships:
            self.game_ui.aiCruiser.setEnabled(False)
        if "submarine" not in a_ships:
            self.game_ui.aiSubmarine.setEnabled(False)
        if "destroyer" not in a_ships:
            self.game_ui.aiDestroyer.setEnabled(False)

    def show(self):
        self.win.show()
