import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_first import Ui_FirstDialog

class MyDlg(QDialog, Ui_FirstDialog):
  def __init__(self, parent=None):
    super(MyDlg, self).__init__(parent)

    self.setupUi(self)
    self.connect(self.btnTest, SIGNAL("clicked()"), self.helloClicked)

  def helloClicked(self):
    QMessageBox.information(self, "Hello", "Hello World", QMessageBox.Ok | QMessageBox.Cancel)


app = QApplication(sys.argv)
dlg = MyDlg()
dlg.show()
app.exec_()

