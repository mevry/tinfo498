from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os.path
from pathlib import Path
from trie.trie import Trie


test_path = Path.cwd() / 'data/words_alpha_rank.txt'
trie = Trie(test_path)

class TrieWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(400,400))
        self.setWindowTitle("Trie Text Prediction")

        #Set up base widget & layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QGridLayout(self)
        centralWidget.setLayout(layout)

        #Set up widgets
        self.label = QLabel("Trie Predictive Text")
        self.label.setAlignment(Qt.AlignLeft)
        self.rank = QLabel()
        self.text_box = QLineEdit()
        self.text_box.setAlignment(Qt.AlignLeft)
        button = QPushButton("Save")

        #Add widgets to dialog box
        layout.addWidget(self.label)
        layout.addWidget(self.rank)
        layout.addWidget(self.text_box)
        layout.addWidget(button)

        #Events
        button.clicked.connect(trie.save_custom)
        self.text_box.textChanged.connect(self.changeTextLabel)
        self.text_box.returnPressed.connect(self.update_rank)

    def changeTextLabel(self, text):
        prediction = trie.predict(text)
        self.label.setText(prediction[0])
        self.rank.setText(str(prediction[1]))

    def update_rank(self):
        trie.update_rank(self.text_box.text())

app = QApplication(sys.argv)
window = TrieWindow()
window.show()
sys.exit(app.exec_())