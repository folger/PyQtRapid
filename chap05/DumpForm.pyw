#! /usr/bin/python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import penpropertiesdlg
import numberformatdlg

class DumbForm(QDialog):
  def __init__(self, parent=None):
    super(DumbForm, self).__init__(parent)

    self.setWindowTitle("Dump")

    btn = QPushButton("   Click Me   ")

    layout = QVBoxLayout()
    layout.addWidget(btn)
    self.setLayout(layout)
    
    self.connect(btn, SIGNAL("clicked()"), self.clickme)

  def clickme(self):
    # dlg = penpropertiesdlg.PenPropertiesDlg(self)
    format = dict(thousandsseparator=",",
             decimalmarker=".", decimalplaces=2,
             rednegatives=False)
    dlg = numberformatdlg.NumberFormatDlg(format, self)
    if dlg.exec_():
      print("yeah")
    else:
      print("no...")

app = QApplication(sys.argv)
form = DumbForm()
form.show()
app.exec_()