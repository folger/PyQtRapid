import sys
from functools import partial
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Connections(QDialog):
  def __init__(self, parent=None):
    super(Connections, self).__init__(parent)

    self.setWindowTitle("Connections")

    self.label = QLabel("You clicked button 'xxxxx'")

    self.btn1 = QPushButton("One")
    self.btn2 = QPushButton("Two")
    self.btn3 = QPushButton("Three")
    self.btn4 = QPushButton("Four")
    self.btn5 = QPushButton("Five")

    layout = QHBoxLayout()
    layout.addWidget(self.btn1)
    layout.addWidget(self.btn2)
    layout.addWidget(self.btn3)
    layout.addWidget(self.btn4)
    layout.addWidget(self.btn5)
    layout.addWidget(self.label)
    self.setLayout(layout)

    self.connect(self.btn1, SIGNAL("clicked()"), partial(self.anyButton, "One"))
    self.connect(self.btn2, SIGNAL("clicked()"), partial(self.anyButton, "Two"))
    self.connect(self.btn3, SIGNAL("clicked()"), partial(self.anyButton, "Three"))
    self.connect(self.btn4, SIGNAL("clicked()"), partial(self.anyButton, "Four"))
    self.connect(self.btn5, SIGNAL("clicked()"), partial(self.anyButton, "Five"))

  def anyButton(self, who):
    self.label.setText("You clicked button '%s'" % who)

app = QApplication(sys.argv)
connections = Connections()
connections.show()
app.exec_()

