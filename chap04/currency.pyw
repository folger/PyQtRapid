#! /usr/bin/python

import sys
from urllib.request import urlopen
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):
  def __init__(self, parent=None):
    super(Form, self).__init__(parent)

    self.setWindowTitle("Currency")

    date = self.getdata()
    rates = sorted(self.rates.keys())

    dateLabel = QLabel(date)
    self.fromCombobBox = QComboBox()
    self.fromCombobBox.addItems(rates)
    self.fromSpinBox = QDoubleSpinBox()
    self.fromSpinBox.setRange(0.01, 10000000.0)
    self.fromSpinBox.setValue(1.0)
    self.toCombobBox = QComboBox()
    self.toCombobBox.addItems(rates)
    self.toLabel = QLabel("1.00")

    grid = QGridLayout()
    grid.addWidget(dateLabel, 0, 0)        
    grid.addWidget(self.fromCombobBox, 1, 0)
    grid.addWidget(self.fromSpinBox, 1, 1)
    grid.addWidget(self.toCombobBox, 2, 0)
    grid.addWidget(self.toLabel, 2, 1)
    self.setLayout(grid)

    self.connect(self.fromCombobBox, SIGNAL("currentIndexChanged(int)"), self.updateUi)
    self.connect(self.toCombobBox, SIGNAL("currentIndexChanged(int)"), self.updateUi)
    self.connect(self.fromSpinBox, SIGNAL("valueChanged(double)"), self.updateUi)

  def updateUi(self):
    to = self.toCombobBox.currentText()
    from_ = self.fromCombobBox.currentText()
    amount = (self.rates[from_] / self.rates[to]) * self.fromSpinBox.value()
    self.toLabel.setText("%0.2f" % amount)

  def getdata(self):
    self.rates = {}
    try:
      date = "Unknown"
      response = urlopen("http://www.bankofcanada.ca"
                          "/en/markets/csv/exchange_eng.csv")
      for line in response.read().decode().split('\n'):
        if not line or line.startswith(("#", "Closing ")):
          continue
        fields = line.split(",")
        if line.startswith("Date "):
          date = fields[-1]
        else:
          try:
            value = float(fields[-1])
            self.rates[fields[0]] = value
          except ValueError:
            pass
      return "Exchange Rates Date: " + date
    except Exception as e:
      return "Failed to download:\n%s" % e

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

