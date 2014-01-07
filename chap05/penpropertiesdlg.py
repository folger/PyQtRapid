import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PenPropertiesDlg(QDialog):
  def __init__(self, parent):
    super(PenPropertiesDlg, self).__init__(parent)

    self.setWindowTitle("Pen Properties")

    widthLabel = QLabel("&Width:")
    self.widthSpinBox = QSpinBox()
    widthLabel.setBuddy(self.widthSpinBox)
    self.widthSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
    self.widthSpinBox.setRange(0, 24)
    self.beveledCheckBox = QCheckBox("&Beveled edges")
    styleLabel = QLabel("&Style:")
    self.styleComboBox = QComboBox()
    styleLabel.setBuddy(self.styleComboBox)
    self.styleComboBox.addItems(["Solid", "Dashed", "Dotted",
                                "DashDotted", "DashDotDotted"])
    okButton = QPushButton("&OK")
    cancelButton = QPushButton("Cancel")

    buttonLayout = QHBoxLayout()
    buttonLayout.addStretch()
    buttonLayout.addWidget(okButton)
    buttonLayout.addWidget(cancelButton)

    layout = QGridLayout()
    layout.addWidget(widthLabel, 0, 0)
    layout.addWidget(self.widthSpinBox, 0, 1)
    layout.addWidget(self.beveledCheckBox, 0, 2)
    layout.addWidget(styleLabel, 1, 0)
    layout.addWidget(self.styleComboBox, 1, 1, 1, -1)
    layout.addLayout(buttonLayout, 2, 0, 1, -1)
    self.setLayout(layout)

    self.connect(okButton, SIGNAL("clicked()"), self.accept)
    self.connect(cancelButton, SIGNAL("clicked()"), self.reject)




