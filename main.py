from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os.path
from pathlib import Path
from trie.trie import Trie


test_path = Path.cwd() / 'data/wordlist.10000.rank.txt'
trie = Trie(test_path)

class TrieWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(400,400))
        self.setWindowTitle("Trie Text Prediction")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        #Set up widgets
        layout = QGridLayout(self)
        centralWidget.setLayout(layout)
        self.label = QLabel("Trie Predictive Text")
        self.label.setAlignment(Qt.AlignLeft)
        self.text_box = QLineEdit()
        self.text_box.setAlignment(Qt.AlignLeft)
        #button = QPushButton("Close")

        #Add widgets to dialog box
        layout.addWidget(self.label)
        layout.addWidget(self.text_box)
        #layout.addWidget(button)

        #self.setLayout(layout)

        #button.clicked.connect(self.close)
        self.text_box.textChanged.connect(self.changeTextLabel)
        self.text_box.returnPressed.connect(self.update_rank)

    def changeTextLabel(self, text):
        prediction = trie.predict(text)
        self.label.setText(prediction)

    def update_rank(self):
        trie.update_rank(self.text_box.text())

app = QApplication(sys.argv)
window = TrieWindow()
window.show()
sys.exit(app.exec_())