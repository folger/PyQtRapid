#! /usr/bin/python

import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import helpform
import newimagedlg
import qrc_resources

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

        logDockWidget = QDockWidget(self.tr("Log"), self)
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
        status.showMessage(self.tr("Ready"), 5000)

        self.recentFiles = []
        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.connect(self.fileMenu, SIGNAL("aboutToShow()"),
                    self.updateFileMenu)
        self.updateFileMenu()

        self.editMenu = self.menuBar().addMenu(self.tr("&Edit"))
        self.updateEditMenu()

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.updateHelpMenu()

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolbar")
        fileToolbar.addActions((self.fileNewAction, self.fileOpenAction, self.fileSaveAction))

        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolbar")
        editToolbar.addActions((self.editInvertAction, self.editSwapRedAndBlueAction, self.separator(),
                            self.editUnMirrorAction, self.editMirrorHorizontalAction, self.editMirrorVerticalAction))

        self.zoomSpinBox = QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(" %")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip("Zoom the image")
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)
        self.connect(self.zoomSpinBox, SIGNAL("valueChanged(int)"), self.showImage)
        editToolbar.addWidget(self.zoomSpinBox)

        self.imageLabel.addActions((self.editInvertAction, self.editSwapRedAndBlueAction,
                                self.editUnMirrorAction, self.editMirrorHorizontalAction, self.editMirrorVerticalAction))

        self.resetableActions = ((self.editInvertAction, False),
                                (self.editSwapRedAndBlueAction, False),
                                (self.editUnMirrorAction, True))

        settings = QSettings()
        recentFilesSetting = settings.value("RecentFiles")
        geometrySetting = settings.value("MainWindow/Geometry")
        self.restoreGeometry(settings.value("MainWindow/Geometry"))
        self.restoreState(settings.value("MainWindow/State"))
        
        self.setWindowTitle(self.tr("Image Changer"))
        QTimer.singleShot(0, self.loadInitialFile)

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

    def updateFileMenu(self):
            self.fileMenu.clear()

            self.fileNewAction = self.createAction(self.tr("&New..."),
                                    self.fileNew, QKeySequence.New, "filenew",
                                    self.tr("Create an image file"))
            self.fileOpenAction = self.createAction(self.tr("&Open..."),
                                    self.fileOpen, QKeySequence.Open, "fileopen",
                                    self.tr("Open an existing image file"))
            self.fileSaveAction = self.createAction(self.tr("&Save"),
                                    self.fileSave, QKeySequence.Save, "filesave",
                                    self.tr("Save the image"))
            fileSaveAsAction = self.createAction(self.tr("Save &As..."),
                                    self.fileSaveAs, icon="filesaveas",
                                    tip=self.tr("Save the image using a new name"))

            self.fileMenu.addActions((self.fileNewAction, self.fileOpenAction, self.fileSaveAction, fileSaveAsAction))

            self.fileMenu.addSeparator()

            filePrint = self.createAction(self.tr("&Print..."),
                                    self.filePrint, QKeySequence.Print, "fileprint",
                                    self.tr("Print the image"))

            self.fileMenu.addAction(filePrint)

            recentFiles = []
            for fname in self.recentFiles:
                if fname != self.filename and QFile.exists(fname):
                    recentFiles.append(fname)
            if recentFiles:
                self.fileMenu.addSeparator()
                for i, fname in enumerate(recentFiles):
                    action = QAction(QIcon(":/icon.png"),
                            "&{0} {1}".format(i + 1,
                            QFileInfo(fname).fileName()), self)
                    action.setData(fname)
                    self.connect(action, SIGNAL("triggered()"), self.loadFile)
                    self.fileMenu.addAction(action)

            self.fileMenu.addSeparator()

            fileQuitAction = self.createAction(self.tr("&Quit"),
                                    self.close, QKeySequence.Close, "filequit",
                                    self.tr("Close the application"))

            self.fileMenu.addAction(fileQuitAction)

    def updateEditMenu(self):
        self.editMenu.clear()

        self.editInvertAction = self.createAction(self.tr("&Invert"),
                                    self.editInvert, self.tr("Ctrl+I"), "editinvert",
                                    self.tr("Invert the image's colors"), True,
                                    "toggled(bool)")
        self.editSwapRedAndBlueAction = self.createAction(
                                    self.tr("Sw&ap Red and Blue"),
                                    self.editSwapRedAndBlue, self.tr("Ctrl+A"), "editswap",
                                    self.tr("Swap the image's red and blue "
                                                    "color components"), True, "toggled(bool)")

        editZoomAction = self.createAction(self.tr("&Zoom..."),
                                    self.editZoom, self.tr("Alt+Z"), "editzoom",
                                    self.tr("Zoom the image"))

        self.editMenu.addActions((self.editInvertAction, self.editSwapRedAndBlueAction, editZoomAction))
        
        mirrorGroup = QActionGroup(self)
        self.editUnMirrorAction = self.createAction(self.tr("&Unmirror"),
                                    self.editUnMirror, "Ctrl+U", "editunmirror",
                                    self.tr("Unmirror the image"), True, "toggled(bool)")
        mirrorGroup.addAction(self.editUnMirrorAction)
        self.editMirrorHorizontalAction = self.createAction(
                                    self.tr("Mirror &Horizontally"),
                                    self.editMirrorHorizontal, self.tr("Ctrl+H"),
                                    "editmirrorhoriz",
                                    self.tr("Horizontally mirror the image"), True,
                                    "toggled(bool)")
        mirrorGroup.addAction(self.editMirrorHorizontalAction)
        self.editMirrorVerticalAction = self.createAction(
                                    self.tr("Mirror &Vertically"), self.editMirrorVertical,
                                    self.tr("Ctrl+V"), "editmirrorvert",
                                    self.tr("Vertically mirror the image"), True,
                                    "toggled(bool)")
        mirrorGroup.addAction(self.editMirrorVerticalAction)

        self.editUnMirrorAction.setChecked(True)

        mirrorMenu = self.editMenu.addMenu(QIcon(":/editmirror.png"),
                                    self.tr("&Mirror"))

        mirrorMenu.addActions((self.editUnMirrorAction, self.editMirrorHorizontalAction, self.editMirrorVerticalAction))

    def updateHelpMenu(self):
        self.helpMenu.clear()

        helpAboutAction = self.createAction(
                                    self.tr("&About Image Changer"), self.helpAbout)
        helpHelpAction = self.createAction(self.tr("&Help"),
                                    self.helpHelp, QKeySequence.HelpContents)

        self.helpMenu.addActions((helpAboutAction, helpHelpAction))

    def fileNew(self):
        QMessageBox.about(self, "Hello", "New ...")

    def fileOpen(self):
        QMessageBox.about(self, "Hello", "Open ...")

    def fileSave(self):
        QMessageBox.about(self, "Hello", "Save ...")

    def fileSaveAs(self):
        QMessageBox.about(self, "Hello", "Save As ...")

    def filePrint(self):
        QMessageBox.about(self, "Hello", "Print ...")

    def editInvert(self):
        QMessageBox.about(self, "Hello", "editInvert ...")

    def editSwapRedAndBlue(self):
        QMessageBox.about(self, "Hello", "editSwapRedAndBlue ...")

    def editZoom(self):
        QMessageBox.about(self, "Hello", "editZoom ...")

    def editUnMirror(self):
        pass

    def editMirrorHorizontal(self):
        pass

    def editMirrorVertical(self):
        pass

    def helpAbout(self):
        pass

    def helpHelp(self):
        pass

    def showImage(self):
        pass

    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            settings.setValue("LastFile", self.filename)
            settings.setValue("RecentFiles", self.recentFiles)
            settings.setValue("MainWindow/Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())
        else:
            event.ignore()

    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self,
                            self.tr("Image Changer - Unsaved Changes"),
                            self.tr("Save unsaved changes?"),
                            QMessageBox.Yes|QMessageBox.No|
                            QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True

    def loadInitialFile(self):
        pass

    def separator(self):
        separator = QAction(self)
        separator.setSeparator(True)
        return separator

def main():
        app = QApplication(sys.argv)

        # Linux and Mac Terminal run:
        # $ LANG=fr ./imagechanger.pyw
        # locale = QLocale.system().name()
        # qtTranslator = QTranslator()
        # if qtTranslator.load("qt_" + locale, ":/"):
        #         app.installTranslator(qtTranslator)
        # appTranslator = QTranslator()
        # if appTranslator.load("imagechanger_" + locale, ":/"):
        #         app.installTranslator(appTranslator)

        app.setOrganizationName("FL Ltd.")
        app.setOrganizationDomain("FL.cn")
        app.setApplicationName(app.translate("main", "Image Changer"))
        app.setWindowIcon(QIcon(":/icon.png"))
        form = MainWindow()
        form.show()
        app.exec_()


main()


        
