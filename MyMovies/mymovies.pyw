import sys
import os
from functools import partial
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qrc_resources

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.movies = moviedata.MovieContainer()
        self.table = QTableWidget()
        self.setCentralWidget(self.table)

        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        fileNewAction = self.createAction(self.tr("&New"),
                                    self.fileNew, QKeySequence.New, "filenew",
                                    self.tr("Create a Movies file"))
        fileOpenAction = self.createAction(self.tr("&Open..."),
                                    self.fileOpen, QKeySequence.Open, "fileopen",
                                    self.tr("Open a Movie file"))
        fileSaveAction = self.createAction(self.tr("&Save"),
                                    self.fileSave, QKeySequence.Save, "filesave",
                                    self.tr("Save a Movie file"))
        fileSaveAsAction = self.createAction(self.tr("&Save As..."),
                                    self.fileSaveAs, None, "filesaveas",
                                    self.tr("Save as a Movie file"))
        fileQuitAction = self.createAction(self.tr("&Quit"),
                                    self.close, QKeySequence.Close, "filequit",
                                    self.tr("Close the application"))
        self.fileMenu.addActions((fileNewAction,fileOpenAction, fileSaveAction, fileSaveAsAction, fileQuitAction))

        self.editMenu = self.menuBar().addMenu(self.tr("&Edit"))

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                    tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def fileNew(self):
        QMessageBox.information(self, 'yy', 'New')
    def fileOpen(self):
        QMessageBox.information(self, 'yy', 'Open')
    def fileSave(self):
        QMessageBox.information(self, 'yy', 'Save')
    def fileSaveAs(self):
        QMessageBox.information(self, 'yy', 'Save As')

    def closeEvent(self, event):
        QMessageBox.information(self, 'yy', 'Quit')


app = QApplication(sys.argv)
app.setOrganizationName("FL Ltd.")
app.setOrganizationDomain("FL.cn")
app.setApplicationName(app.translate("main", "My Movies"))

dlg = MainWindow()
dlg.show()
app.exec_()

