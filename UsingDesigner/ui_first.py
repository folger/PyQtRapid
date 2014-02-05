# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'First.ui'
#
# Created: Tue Feb  4 20:55:43 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FirstDialog(object):
    def setupUi(self, FirstDialog):
        FirstDialog.setObjectName(_fromUtf8("FirstDialog"))
        FirstDialog.resize(400, 300)
        self.btnTest = QtGui.QPushButton(FirstDialog)
        self.btnTest.setGeometry(QtCore.QRect(250, 250, 114, 32))
        self.btnTest.setObjectName(_fromUtf8("btnTest"))

        self.retranslateUi(FirstDialog)
        QtCore.QMetaObject.connectSlotsByName(FirstDialog)

    def retranslateUi(self, FirstDialog):
        FirstDialog.setWindowTitle(_translate("FirstDialog", "First Dialog using Designer", None))
        self.btnTest.setText(_translate("FirstDialog", "Hello", None))

