import threading
from PyQt5.QtCore import QTimer
from frontend import Ui_MainWindow
from PyQt5 import QtWidgets
from algorithms import *


class CONNECT4(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.blinked = False
        self.state = [['0' for _ in range(7)] for _ in range(6)]
        self.turn = 0
        self.ui.turn.hide()
        self.ui.Winner_label.hide()

        self.timer = QTimer(self)
        self.playTime = QTimer(self)

        self.ui.frame.hide()
        self.ui.user_score.hide()
        self.ui.agent_score.hide()
        self.ui.tree_button.setEnabled(False)

        self.ui.tree_button.clicked.connect(self.show_tree)
        self.ui.reset.clicked.connect(self.reset)
        self.ui.agentStart.clicked.connect(lambda: self.set_turn(2))
        self.ui.userStart.clicked.connect(lambda: self.set_turn(1))

        self.ui.noPruning.toggle()

        self.col0 = [self.ui.button0, self.ui.button7, self.ui.button14, self.ui.button21, self.ui.button28,
                     self.ui.button35]
        self.col1 = [self.ui.button1, self.ui.button8, self.ui.button15, self.ui.button22, self.ui.button29,
                     self.ui.button36]
        self.col2 = [self.ui.button2, self.ui.button9, self.ui.button16, self.ui.button23, self.ui.button30,
                     self.ui.button37]
        self.col3 = [self.ui.button3, self.ui.button10, self.ui.button17, self.ui.button24, self.ui.button31,
                     self.ui.button38]
        self.col4 = [self.ui.button4, self.ui.button11, self.ui.button18, self.ui.button25, self.ui.button32,
                     self.ui.button39]
        self.col5 = [self.ui.button5, self.ui.button12, self.ui.button19, self.ui.button26, self.ui.button33,
                     self.ui.button40]
        self.col6 = [self.ui.button6, self.ui.button13, self.ui.button20, self.ui.button27, self.ui.button34,
                     self.ui.button41]
        self.cols = [self.col0, self.col1, self.col2, self.col3, self.col4, self.col5, self.col6]

        self.timer.timeout.connect(self.blink)
        self.playTime.timeout.connect(self.show_time)

        self.ui.button0.clicked.connect(lambda: self.set_state(0, str(self.turn)))
        self.ui.button1.clicked.connect(lambda: self.set_state(1, str(self.turn)))
        self.ui.button2.clicked.connect(lambda: self.set_state(2, str(self.turn)))
        self.ui.button3.clicked.connect(lambda: self.set_state(3, str(self.turn)))
        self.ui.button4.clicked.connect(lambda: self.set_state(4, str(self.turn)))
        self.ui.button5.clicked.connect(lambda: self.set_state(5, str(self.turn)))
        self.ui.button6.clicked.connect(lambda: self.set_state(6, str(self.turn)))
        self.ui.button7.clicked.connect(lambda: self.set_state(0, str(self.turn)))
        self.ui.button8.clicked.connect(lambda: self.set_state(1, str(self.turn)))
        self.ui.button9.clicked.connect(lambda: self.set_state(2, str(self.turn)))
        self.ui.button10.clicked.connect(lambda: self.set_state(3, str(self.turn)))
        self.ui.button11.clicked.connect(lambda: self.set_state(4, str(self.turn)))
        self.ui.button12.clicked.connect(lambda: self.set_state(5, str(self.turn)))
        self.ui.button13.clicked.connect(lambda: self.set_state(6, str(self.turn)))
        self.ui.button14.clicked.connect(lambda: self.set_state(0, str(self.turn)))
        self.ui.button15.clicked.connect(lambda: self.set_state(1, str(self.turn)))
        self.ui.button16.clicked.connect(lambda: self.set_state(2, str(self.turn)))
        self.ui.button17.clicked.connect(lambda: self.set_state(3, str(self.turn)))
        self.ui.button18.clicked.connect(lambda: self.set_state(4, str(self.turn)))
        self.ui.button19.clicked.connect(lambda: self.set_state(5, str(self.turn)))
        self.ui.button20.clicked.connect(lambda: self.set_state(6, str(self.turn)))
        self.ui.button21.clicked.connect(lambda: self.set_state(0, str(self.turn)))
        self.ui.button22.clicked.connect(lambda: self.set_state(1, str(self.turn)))
        self.ui.button23.clicked.connect(lambda: self.set_state(2, str(self.turn)))
        self.ui.button24.clicked.connect(lambda: self.set_state(3, str(self.turn)))
        self.ui.button25.clicked.connect(lambda: self.set_state(4, str(self.turn)))
        self.ui.button26.clicked.connect(lambda: self.set_state(5, str(self.turn)))
        self.ui.button27.clicked.connect(lambda: self.set_state(6, str(self.turn)))
        self.ui.button28.clicked.connect(lambda: self.set_state(0, str(self.turn)))
        self.ui.button29.clicked.connect(lambda: self.set_state(1, str(self.turn)))
        self.ui.button30.clicked.connect(lambda: self.set_state(2, str(self.turn)))
        self.ui.button31.clicked.connect(lambda: self.set_state(3, str(self.turn)))
        self.ui.button32.clicked.connect(lambda: self.set_state(4, str(self.turn)))
        self.ui.button33.clicked.connect(lambda: self.set_state(5, str(self.turn)))
        self.ui.button34.clicked.connect(lambda: self.set_state(6, str(self.turn)))
        self.ui.button35.clicked.connect(lambda: self.set_state(0, str(self.turn)))
        self.ui.button36.clicked.connect(lambda: self.set_state(1, str(self.turn)))
        self.ui.button37.clicked.connect(lambda: self.set_state(2, str(self.turn)))
        self.ui.button38.clicked.connect(lambda: self.set_state(3, str(self.turn)))
        self.ui.button39.clicked.connect(lambda: self.set_state(4, str(self.turn)))
        self.ui.button40.clicked.connect(lambda: self.set_state(5, str(self.turn)))
        self.ui.button41.clicked.connect(lambda: self.set_state(6, str(self.turn)))

    def show_tree(self):
        file = open("Tree.txt", "r+", encoding='utf-8')
        tree_file = file.read()
        file.close()
        self.ui.customlabel.setText(tree_file)
        self.ui.customlabel.show()

    def show_time(self):
        old = float(self.ui.time.text().split()[0]) if self.ui.time.text() != "" else 0
        new = round(old + 0.1, 3)
        self.ui.time.setText(str(new) + ' sec')

    def set_turn(self, turn):
        self.ui.userStart.hide()
        self.ui.agentStart.hide()
        self.ui.user_score.show()
        self.ui.agent_score.show()
        self.ui.frame.show()

        self.timer.start(500)
        self.turn = turn
        if turn == 2:
            self.ui.frame.setEnabled(False)
            self.ui.turn.setStyleSheet("background-color: rgb(255, 255, 0); border-radius: 50px")
            thread = threading.Thread(target=self.comp_turn)
            thread.start()
        else:
            self.ui.frame.setEnabled(True)
            self.ui.turn.setStyleSheet("background-color: rgb(255, 0, 0); border-radius: 50px")

    def comp_turn(self):
        encoded = encode_state(self.state)
        self.state = minimax(encoded, self.ui.maxDepth.value(), self.ui.pruning.isChecked(),
                             self.ui.searchTree.isChecked())
        explored = self.state[1]
        self.state = self.state[0][0]
        self.ui.explored.setText(str(explored) + ' nodes')

        self.display_state()
        self.ui.frame.setEnabled(True)
        self.ui.turn.setStyleSheet("background-color: rgb(255, 0, 0); border-radius: 50px")
        self.turn = 1
        self.disable()
        self.ui.reset.setEnabled(True)
        self.playTime.stop()
        self.ui.groupBox.setEnabled(True)
        if self.ui.searchTree.isChecked():
            self.ui.tree_button.setEnabled(True)

    def set_state(self, j, char):
        if char == '1':
            self.ui.frame.setEnabled(False)
            for i in range(6):
                if self.state[i][j] == '0':
                    self.state[i][j] = char
                    self.ui.turn.setStyleSheet("background-color: rgb(255, 255, 0); border-radius: 50px")
                    self.display_state()
                    self.ui.frame.setEnabled(False)
                    self.turn = 2
                    self.disable()
                    self.ui.time.setText("0 sec")
                    self.ui.reset.setEnabled(False)
                    self.ui.groupBox.setEnabled(False)
                    self.ui.tree_button.setEnabled(False)
                    self.playTime.start(100)
                    thread = threading.Thread(target=self.comp_turn)
                    thread.start()
                    return

    def disable(self):
        for j, col in enumerate(self.cols):
            if self.state[-1][j] != '0':
                for button in col:
                    button.setEnabled(False)

        if is_full(self.state):
            self.timer.stop()
            self.ui.turn.hide()

            score = getScore(self.state)

            if score[0] > score[1]:
                self.ui.Winner_label.show()
                self.ui.Winner_label.setText("Agent won!")

            elif score[0] < score[1]:
                self.ui.Winner_label.show()
                self.ui.Winner_label.setText("User won!")

            else:
                self.ui.Winner_label.show()
                self.ui.Winner_label.setText("Tie!")

    def display_state(self):
        for j, col in enumerate([self.col0, self.col1, self.col2, self.col3, self.col4, self.col5, self.col6]):
            for i, button in enumerate(col):
                if self.state[i][j] == '0':
                    button.setStyleSheet("background-color: rgb(206, 206, 206); border-radius: 50px")
                elif self.state[i][j] == '1':
                    button.setStyleSheet("background-color: rgb(255, 0, 0); border-radius: 50px")
                else:
                    button.setStyleSheet("background-color: rgb(255, 255, 0); border-radius: 50px")
        agent, user = getScore(self.state)
        self.ui.agent_score.setText('Agent Score:    ' + str(agent))
        self.ui.user_score.setText('Your Score:    ' + str(user))

    def blink(self):
        if self.blinked:
            self.ui.turn.show()
            self.blinked = not self.blinked
        else:
            self.ui.turn.hide()
            self.blinked = not self.blinked

    def reset(self):
        self.state = [['0' for _ in range(7)] for _ in range(6)]
        self.timer.stop()
        self.ui.turn.hide()
        self.ui.frame.hide()
        self.ui.user_score.hide()
        self.ui.agent_score.hide()
        self.ui.Winner_label.hide()
        self.ui.userStart.show()
        self.ui.agentStart.show()
        self.ui.tree_button.setEnabled(False)
        self.ui.time.setText("")

        row = [self.ui.button35, self.ui.button36, self.ui.button37, self.ui.button38, self.ui.button39,
               self.ui.button40, self.ui.button41]

        for button, col in zip(row, self.cols):
            if not button.isEnabled():
                for disabled_button in col:
                    disabled_button.setEnabled(True)

        self.display_state()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = CONNECT4()
    gui.show()
    sys.exit(app.exec())
