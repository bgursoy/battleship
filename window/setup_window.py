from PyQt5.QtWidgets import QMainWindow, QMessageBox
from game.cell import Cell
from layout.setup_layout import Ui_SetupWindow
from window.game_window import GameWindow


class SetupWindow:
    setup_ui = Ui_SetupWindow()
    placement_mode = None
    player_map = []
    ships = {"carrier": 5, "battleship": 4, "cruiser": 3, "submarine": 3, "destroyer": 2}
    rotate = "Horizontal"
    remained_ships = 5

    def __init__(self):
        self.win = QMainWindow()
        self.setup_ui.setupUi(self.win)
        self.win.setWindowTitle("Battleship Game")
        self.setup_ui.readyButton.clicked.connect(self.actionReadyButton)
        self.setup_ui.carrierButton.clicked.connect(self.actionCarrierButton)
        self.setup_ui.battleshipButton.clicked.connect(self.actionBattleshipButton)
        self.setup_ui.cruiserButton.clicked.connect(self.actionCruiserButton)
        self.setup_ui.submarineButton.clicked.connect(self.actionSubmarineButton)
        self.setup_ui.destroyerButton.clicked.connect(self.actionDestroyerButton)
        self.setup_ui.rotateButton.clicked.connect(self.actionRotateButton)

        # Fill setup grid with cells
        for row in range(10):
            cells_row = []
            for column in range(10):
                setup_cell = Cell(row, column, self)
                cells_row.append(setup_cell)
                self.setup_ui.setupGrid.addWidget(setup_cell, row, column)
            self.player_map.append(cells_row)

    # Show window
    def show(self):
        self.win.show()

    # Triggered when a cell clicked
    def actionCellClick(self, target):
        # If a ship is selected for placement, place ship to the target cell.
        if self.placement_mode:
            self.placeShips(self.placement_mode, target)
        print(self.placement_mode)

    def actionReadyButton(self):
        # Create a new game window
        self.game_window = GameWindow(self.player_map)
        self.game_window.show()

        # Close this window
        self.win.close()

    # Set placement mode to carrier, which indicates the carrier ship is going to be placed.
    def actionCarrierButton(self):
        self.placement_mode = "carrier"
        self.ship_button = self.setup_ui.carrierButton

    def actionBattleshipButton(self):
        self.placement_mode = "battleship"
        self.ship_button = self.setup_ui.battleshipButton

    def actionCruiserButton(self):
        self.placement_mode = "cruiser"
        self.ship_button = self.setup_ui.cruiserButton

    def actionSubmarineButton(self):
        self.placement_mode = "submarine"
        self.ship_button = self.setup_ui.submarineButton

    def actionDestroyerButton(self):
        self.placement_mode = "destroyer"
        self.ship_button = self.setup_ui.destroyerButton

    def buttonDisabled(self):
        self.ship_button.setEnabled(False)
        self.ship_button.setStyleSheet("background-color : white")
        self.remained_ships += -1

    def actionRotateButton(self):
        if self.rotate == "Horizontal":
            self.rotate = "Vertical"
            self.setup_ui.directionLabel.setText("Vertical")
        else:
            self.rotate = "Horizontal"
            self.setup_ui.directionLabel.setText("Horizontal")

    def placeShips(self, ship_name, target):
        # Get target cell location
        row = target.row
        column = target.column
        # Get length of the ship
        ship_length = self.ships[ship_name]

        # Check if target has a valid position
        if self.rotate == "Horizontal":
            if column > 10 - ship_length:
                QMessageBox.warning(self.win, "Error", "Can't place this ship here", QMessageBox.Ok)
                return

            for i in range(ship_length):
                neighbor = self.player_map[row][column + i]
                if not neighbor.isEnabled():
                    # Collides with another ship
                    QMessageBox.warning(self.win, "Error", "Colliding with another ship", QMessageBox.Ok)
                    return
        else:
            if row > 10 - ship_length:
                QMessageBox.warning(self.win, "Error", "Can't place this ship here", QMessageBox.Ok)
                return

            for i in range(ship_length):
                neighbor = self.player_map[row + i][column]
                if not neighbor.isEnabled():
                    # Collides with another ship
                    QMessageBox.warning(self.win, "Error", "Colliding with another ship", QMessageBox.Ok)
                    return

        # The position is valid, place ship
        if self.rotate == "Horizontal":
            # Set cells occupied according to the size of the selected ship.
            for length in range(ship_length):
                neighbor = self.player_map[row][column + length]
                neighbor.setHit()
                neighbor.setOccupiedShip(ship_name)
            self.buttonDisabled()
            print("Player placed" + ship_name + " (H): ", row, column)

        else:
            # Set cells occupied according to the size of the selected ship.
            for length in range(ship_length):
                neighbor = self.player_map[row + length][column]
                neighbor.setHit()
                neighbor.setOccupiedShip(ship_name)
            self.buttonDisabled()
            print("Player placed" + ship_name + " (V): ", row, column)

        print(self.remained_ships)

        # If all ships are placed, activate ready button
        if self.remained_ships == 0:
            self.setup_ui.readyButton.setEnabled(True)
            self.setup_ui.readyButton.setStyleSheet("background-color: green")
            self.setup_ui.titleLabel.setText("Your ships are ready!")

        # When a ship is placed clear placement mode for another ship
        self.placement_mode = None
