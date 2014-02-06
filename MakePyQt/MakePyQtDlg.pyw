import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_MakePyQt import Ui_MakePyQtDlg

class MakePyQtDlg(QDialog, Ui_MakePyQtDlg):
    def __init__(self, parent=None):
        super(MakePyQtDlg, self).__init__(parent)

        self.setupUi(self)

        self.connect(self.btnBrowsePath, SIGNAL("clicked()"), self.browsePath)

        self.loadSettings()

    def browsePath(self):
        dialog = QFileDialog(None)
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec():
            dirs = dialog.selectedFiles()
            if len(dirs):
                self.edPath.setText(dirs[0])

    def closeEvent(self, event):
        self.saveSettings()



    def loadSettings(self):
        self.loadOneSetting(self.geometrySettingKey, lambda x: self.restoreGeometry(x))
        self.loadOneSetting(self.pathSettingKey, lambda x: self.edPath.setText(x))
        self.loadOneSetting(self.recursiveSettingKey, lambda x: self.chkRecursive.setChecked(x))

    def loadOneSetting(self, keyFunc, setFunc):
        settings = QSettings()
        setting = settings.value(keyFunc())
        if setting:
            setFunc(setting)

    def saveSettings(self):
        settings = QSettings()
        settings.setValue(self.geometrySettingKey(), self.saveGeometry())
        settings.setValue(self.pathSettingKey(), self.edPath.text())
        settings.setValue(self.recursiveSettingKey(), self.chkRecursive.isChecked())

    def settingsMainKey(self):      return "MainWindow"
    def geometrySettingKey(self):   return self.settingsMainKey() + '/Geometry'
    def pathSettingKey(self):       return self.settingsMainKey() + '/Path'
    def recursiveSettingKey(self):  return self.settingsMainKey() + '/Recursive'


app = QApplication(sys.argv)
app.setOrganizationName("FL Ltd.")
app.setOrganizationDomain("FL.cn")
app.setApplicationName(app.translate("main", "Make PyQt"))

dlg = MakePyQtDlg()
dlg.show()
app.exec_()


