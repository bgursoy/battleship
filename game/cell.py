from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton, QSizePolicy


class Cell(QPushButton):
    def __init__(self, row, column, parent_window, ai_player="", occupied_ship=None):
        super().__init__()
        self.parent_window = parent_window
        self.row = row
        self.column = column
        self.ai_player = ai_player
        self.occupied_ship = occupied_ship
        # Customize styles
        self.setStyleSheet("background-color : blue")
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.setCursor(QCursor(QtCore.Qt.CrossCursor))

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        # Call parent windows action method
        self.parent_window.actionCellClick(self)

    def setNeutral(self):
        # Change color of AI's cells
        self.setStyleSheet("background-color : darkblue")
        self.setEnabled(False)

    def setHit(self):
        # Change color of hit cells
        self.setStyleSheet("background-color : crimson")
        self.setEnabled(False)

    def setMiss(self):
        # Change color of missed cells
        self.setStyleSheet("background-color : aqua")
        self.setEnabled(False)

    def setOccupiedShip(self, occupied_ship):
        # Set the ship that occupies this cell
        self.occupied_ship = occupied_ship

    def getOccupiedShip(self):
        # Get the ship that occupies this cell
        return self.occupied_ship
