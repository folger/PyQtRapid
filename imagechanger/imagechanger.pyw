#! /usr/bin/python

import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import helpform
import newimagedlg
# import qrc_resources

__version__ = "1.0.0"


class MainWindow(QMainWindow):
  """main window for image changer app"""
  def __init__(self, parent = None):
    super(MainWindow, self).__init__(parent)

    self.image = QImage()
    self.dirty = False
    self.filename = None
    self.mirroredvertically = False
    self.mirroredhorizontally = False

    self.imageLabel = QLabel()
    self.imageLabel.setMinimumSize(200, 200)
    self.imageLabel.setAlignment(Qt.AlignCenter)
    self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
    self.setCentralWidget(self.imageLabel)

    logDockWidget = QDockWidget("Log", self)
    logDockWidget.setObjectName("LogDockWidget")
    logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

    self.listWidget = QListWidget()
    logDockWidget.setWidget(self.listWidget)
    self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)

    self.printer = None

    self.sizeLabel = QLabel()
    self.sizeLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
    status = self.statusBar()
    status.setSizeGripEnabled(False)
    status.addPermanentWidget(self.sizeLabel)
    status.showMessage("Ready", 5000)

    fileNewAction = self.createAction(self.tr("&New..."),
                self.fileNew, QKeySequence.New, None,
                self.tr("Create an image file"))

    fileOpenAction = self.createAction(self.tr("&Open..."),
                self.fileOpen, QKeySequence.Open, None,
                self.tr("Open an existing image file"))

    fileQuitAction = self.createAction(self.tr("&Quit"),
                self.close, QKeySequence.Close, None,
                self.tr("Close the application"))

    self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
    self.fileMenuActions = (fileNewAction, fileOpenAction, fileQuitAction)
    self.connect(self.fileMenu, SIGNAL("aboutToShow()"),
                self.updateFileMenu)

    self.updateFileMenu()

  def createAction(self, text, slot=None, shortcut=None, icon=None,
                   tip=None, checkable=False, signal="triggered()"):
      action = QAction(text, self)
      if icon is not None:
          action.setIcon(QIcon(":/{0}.png".format(icon)))
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

  def updateFileMenu(self):
      self.fileMenu.clear()
      self.fileMenu.addActions(self.fileMenuActions)

  def fileNew(self):
    QMessageBox.about(self, "Hello", "New ...")

  def fileOpen(self):
    QMessageBox.about(self, "Hello", "Open ...")

def main():
    app = QApplication(sys.argv)

    # Linux and Mac Terminal run:
    # $ LANG=fr ./imagechanger.pyw
    # locale = QLocale.system().name()
    # qtTranslator = QTranslator()
    # if qtTranslator.load("qt_" + locale, ":/"):
    #     app.installTranslator(qtTranslator)
    # appTranslator = QTranslator()
    # if appTranslator.load("imagechanger_" + locale, ":/"):
    #     app.installTranslator(appTranslator)

    app.setOrganizationName("FL Ltd.")
    app.setOrganizationDomain("FL.eu")
    app.setApplicationName(app.translate("main", "Image Changer"))
    # app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()


main()


    
