from PyQt4.QtCore import *
from PyQt4.QtGui import *

class NumberFormatDlg(QDialog):
  def __init__(self, format, parent=None):
    super(NumberFormatDlg, self).__init__(parent)

    self.setWindowTitle("Set Number Format (Modal)")

    thousandsLabel = QLabel("&Thousands separator")
    self.thousandsEdit = QLineEdit(format["thousandsseparator"])
    thousandsLabel.setBuddy(self.thousandsEdit)

    decimalMarkerLabel = QLabel("Decimal &marker")
    self.decimalMarkerEdit = QLineEdit(format["decimalmarker"])
    decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)

    decimalPlacesLabel = QLabel("&Decimal places")
    self.decimalPlacesSpinBox = QSpinBox()
    decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)
    self.decimalPlacesSpinBox.setRange(0, 6)
    self.decimalPlacesSpinBox.setValue(format["decimalplaces"])

    self.redNegativesCheckBox = QCheckBox("&Red negative numbers")
    self.redNegativesCheckBox.setChecked(format["rednegatives"])

    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

    self.format = format.copy()

    grid = QGridLayout()
    grid.addWidget(thousandsLabel, 0, 0)
    grid.addWidget(self.thousandsEdit, 0, 1)
    grid.addWidget(decimalMarkerLabel, 1, 0)
    grid.addWidget(self.decimalMarkerEdit, 1, 1)
    grid.addWidget(decimalPlacesLabel, 2, 0)
    grid.addWidget(self.decimalPlacesSpinBox, 2, 1)
    grid.addWidget(self.redNegativesCheckBox, 3, 0, 1, 2)
    grid.addWidget(buttonBox, 4, 0, 1, 2)
    self.setLayout(grid)

    self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
    self.connect(buttonBox, SIGNAL("rejected()"), self, SLOT("reject()"))

  def accept(self):
    print("Yes yes")
    super(NumberFormatDlg, self).accept()

  def numberFormat(self):
    return self.format

