import sys
import urllib2
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):
  def __init__(self, parent=None):
    super(Form, self).__init__(parent)

    date = self.getdata()
    rates = sorted(self.rates.keys)

    dateLabel = QLabel(date)
    self.fromCombobBox = QComboBox()
    self.fromCombobBox.addItems(rates)
    self.fromSpinBox = QDoubleSpinBox()
    self.fromSpinBox.setRange(0.01, 10000000.0)
    self.fromSpinBox.setValue(1.0)
    self.toCombobBox = QComboBox()
    self.toCombobBox.addItems(rates)
    self.toLabel = QLabel("1.00")

    
