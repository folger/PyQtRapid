import sys
import os
from functools import partial
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_MakePyQt import Ui_MakePyQtDlg

class MakePyQtDlg(QDialog, Ui_MakePyQtDlg):
    def __init__(self, parent=None):
        super(MakePyQtDlg, self).__init__(parent)

        self.setupUi(self)

        self.connect(self.btnBrowsePath, SIGNAL("clicked()"), self.browsePath)
        self.connect(self.btnBuild, SIGNAL("clicked()"),
            partial(self.process, self.build))
        self.connect(self.btnClean, SIGNAL("clicked()"),
            partial(self.process, self.clean))

        self.loadSettings()

    def browsePath(self):
        dialog = QFileDialog(None)
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec():
            dirs = dialog.selectedFiles()
            if len(dirs):
                self.edPath.setText(dirs[0])

    def relativePath(self, path):
        return path[len(self.edPath.text())+1:]

    def build(self, f):
        if f.endswith('.ui'):
            pathname = os.path.dirname(f)
            filename = os.path.basename(f)

            fdest = os.path.join(pathname, 'ui_%s.py' % filename[:-3])

            if not self.isDryRun():
                os.system('pyuic4 %s -o %s' % (f, fdest))
            
            self.outmsg("<font color=blue>Convert %s into %s</font>" %
                (self.relativePath(f), self.relativePath(fdest)))

    def clean(self, f):
        if os.path.basename(f).startswith('ui_') and f.endswith('.py'):
            if not self.isDryRun():
                os.remove(f)
            self.outmsg("<font color=green>%s is removed</font>" % self.relativePath(f))

    def process(self, dotask):
        path = self.edPath.text()
        if not os.path.isdir(path):
            self.outmsg("<font color=red>%s is not a path!</font>" % path)
            return

        if self.isRecursive():
            for dirpath, dirnames, files in os.walk(path):
                for f in files:
                    dotask(os.path.join(dirpath, f))
        else:
            for f in os.listdir(path):
                fname = os.path.join(path, f)
                if os.path.isfile(fname):
                    dotask(fname)

        self.outmsg('-'*50)

    def outmsg(self, msg):
        self.output.append(msg)

    def isRecursive(self):  return self.chkRecursive.isChecked()
    def isDryRun(self):     return self.chkDryRun.isChecked()

    def closeEvent(self, event):
        self.saveSettings()

    def loadSettings(self):
        self.loadOneSetting(self.geometrySettingKey, lambda x: self.restoreGeometry(x) if x else None)
        self.loadOneSetting(self.pathSettingKey, lambda x: self.edPath.setText(x if x else ''))
        self.loadOneSetting(self.recursiveSettingKey, lambda x: self.chkRecursive.setChecked(x if x else True))
        self.loadOneSetting(self.dryRunSettingKey, lambda x: self.chkDryRun.setChecked(x if x else False))

    def loadOneSetting(self, keyFunc, setFunc):
        settings = QSettings()
        setting = settings.value(keyFunc())
        setFunc(setting)

    def saveSettings(self):
        settings = QSettings()
        settings.setValue(self.geometrySettingKey(), self.saveGeometry())
        settings.setValue(self.pathSettingKey(), self.edPath.text())
        settings.setValue(self.recursiveSettingKey(), self.chkRecursive.isChecked())
        settings.setValue(self.dryRunSettingKey(), self.chkDryRun.isChecked())

    def settingsMainKey(self):      return "MainWindow"
    def geometrySettingKey(self):   return self.settingsMainKey() + '/Geometry'
    def pathSettingKey(self):       return self.settingsMainKey() + '/Path'
    def recursiveSettingKey(self):  return self.settingsMainKey() + '/Recursive'
    def dryRunSettingKey(self):     return self.settingsMainKey() + '/DryRun'


app = QApplication(sys.argv)
app.setOrganizationName("FL Ltd.")
app.setOrganizationDomain("FL.cn")
app.setApplicationName(app.translate("main", "Make PyQt"))

dlg = MakePyQtDlg()
dlg.show()
app.exec_()


