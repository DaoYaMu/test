import sys
import random
from PySide2.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel,
                               QVBoxLayout, QHBoxLayout, QWidget, QMessageBox)
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont


class DiceGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dice Game")
        self.setFixedSize(400, 500)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create title label
        title_label = QLabel("Big or Small Dice Game")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # Create dice display
        self.dice_label = QLabel("Dice: ")
        self.dice_label.setAlignment(Qt.AlignCenter)
        dice_font = QFont()
        dice_font.setPointSize(16)
        self.dice_label.setFont(dice_font)
        main_layout.addWidget(self.dice_label)

        # Create total display
        self.total_label = QLabel("Total: ")
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setFont(dice_font)
        main_layout.addWidget(self.total_label)

        # Create result display
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        result_font = QFont()
        result_font.setPointSize(18)
        result_font.setBold(True)
        self.result_label.setFont(result_font)
        main_layout.addWidget(self.result_label)

        # Create buttons layout
        button_layout = QHBoxLayout()

        # Create Big and Small buttons
        self.big_button = QPushButton("Big")
        self.small_button = QPushButton("Small")

        # Style buttons
        button_style = """
        QPushButton {
            font-size: 16px;
            padding: 10px;
            min-width: 100px;
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """
        self.big_button.setStyleSheet(button_style)
        self.small_button.setStyleSheet(button_style)

        # Add buttons to layout
        button_layout.addWidget(self.big_button)
        button_layout.addWidget(self.small_button)
        main_layout.addLayout(button_layout)

        # Connect buttons to slots
        self.big_button.clicked.connect(lambda: self.play_game("Big"))
        self.small_button.clicked.connect(lambda: self.play_game("Small"))

        # Add quit button
        self.quit_button = QPushButton("Quit")
        quit_style = """
        QPushButton {
            font-size: 14px;
            padding: 8px;
            min-width: 80px;
            background-color: #f44336;
            color: white;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #da190b;
        }
        """
        self.quit_button.setStyleSheet(quit_style)
        self.quit_button.clicked.connect(self.close)
        main_layout.addWidget(self.quit_button)

        # Add some spacing
        main_layout.addSpacing(20)

    def roll_dice(self, numbers=3):
        points = []
        for _ in range(numbers):
            point = random.randrange(1, 7)
            points.append(point)
        return points

    def roll_result(self, total):
        is_big = 11 <= total <= 18
        is_small = 3 <= total <= 10
        if is_big:
            return 'Big'
        elif is_small:
            return 'Small'

    def play_game(self, choice):
        # Roll the dice
        points = self.roll_dice()
        total = sum(points)
        result = self.roll_result(total)

        # Update display
        self.dice_label.setText(f"Dice: {points}")
        self.total_label.setText(f"Total: {total}")

        # Check result
        if choice == result:
            self.result_label.setText("You Win! 🎉")
            self.result_label.setStyleSheet("color: green;")
        else:
            self.result_label.setText("You Lose! 😢")
            self.result_label.setStyleSheet("color: red;")


def main():
    app = QApplication(sys.argv)
    game = DiceGame()
    game.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()