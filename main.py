from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os.path
from pathlib import Path
from trie.trie import Trie


test_path = Path.cwd() / 'data/wordlist.10000.rank.txt'
trie = Trie(test_path)

class HelloWorldDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        layout = QVBoxLayout()
        self.label = QLabel("Hello World")
        text_box = QLineEdit()
        button = QPushButton("Close")

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