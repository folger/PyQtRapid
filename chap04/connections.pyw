#! /usr/bin/python

import sys
from functools import partial
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Connections(QDialog):
  def __init__(self, parent=None):
    super(Connections, self).__init__(parent)

    self.setWindowTitle("Connections")

    self.label = QLabel("You clicked button 'xxxxx'")

    btns = []
    for who in ("One", "Two", "Three", "Four", "Five"):
      btns.append(QPushButton(who))

    layout = QHBoxLayout()
    for btn in btns:
      layout.addWidget(btn)

    layout.addWidget(self.label)
    self.setLayout(layout)

    for btn in btns:
      self.connect(btn, SIGNAL("clicked()"), partial(self.anyButton, btn.text()))

  def anyButton(self, who):
    self.label.setText("You clicked button '%s'" % who)

app = QApplication(sys.argv)
connections = Connections()
connections.show()
app.exec_()

