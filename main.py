from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os.path
from pathlib import Path
from trie.trie import Trie


test_path = Path.cwd() / 'data/words_alpha_rank.txt'
trie = Trie(test_path)

class HelloWorldDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        #Set up widgets
        layout = QVBoxLayout()
        self.label = QLabel("Trie Predictive Text")
        text_box = QLineEdit()
        button = QPushButton("Close")

        #Add widgets to dialog box
        layout.addWidget(self.label)
        layout.addWidget(text_box)
        layout.addWidget(button)

        self.setLayout(layout)

        button.clicked.connect(self.close)
        text_box.textChanged.connect(self.changeTextLabel)

    def changeTextLabel(self, text):
        prediction = trie.predict(text)
        self.label.setText(prediction)

app = QApplication(sys.argv)
window = HelloWorldDialog()
window.show()
sys.exit(app.exec_())