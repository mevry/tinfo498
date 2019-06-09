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
        #self.setMinimumSize(QSize(400,400))
        self.setWindowTitle("Trie Text Prediction")

        #Set up base widget & layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        layout = QGridLayout(self)
        centralWidget.setLayout(layout)

        #Set up widgets
        font = QFont('SansSerif', 14)

        self.label2 = QLabel("<b>Prediction:</b>")
        self.label2.setFont(font)
        self.label2.setAlignment(Qt.AlignLeft)

        self.label = QLabel()
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignLeft)


        self.rank_label = QLabel("<b>Frequency:</b>")
        self.rank_label.setAlignment(Qt.AlignLeft)
        self.rank_label.setFont(font)

        self.rank = QLabel()
        self.rank.setFont(font)

        self.text_box = QLineEdit()
        self.text_box.setAlignment(Qt.AlignLeft)
        button = QPushButton("Save")

        #Add widgets to dialog box
        layout.addWidget(self.label2, 0, 0)
        layout.addWidget(self.label, 1, 0)
        layout.addWidget(self.rank_label, 2, 0)
        layout.addWidget(self.rank, 3, 0)
        layout.addWidget(self.text_box, 4, 0)
        layout.addWidget(button, 5, 0)

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