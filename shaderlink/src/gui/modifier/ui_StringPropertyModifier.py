##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui\modifier\ui_StringPropertyModifier.ui'
#
# Created: Fri Oct 03 09:15:40 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_StringPropertyModifier(object):
    def setupUi(self, StringPropertyModifier):
        StringPropertyModifier.setObjectName("StringPropertyModifier")
        StringPropertyModifier.resize(QtCore.QSize(QtCore.QRect(0,0,232,54).size()).expandedTo(StringPropertyModifier.minimumSizeHint()))
        StringPropertyModifier.setMinimumSize(QtCore.QSize(232,54))
        StringPropertyModifier.setMaximumSize(QtCore.QSize(232,54))

        self.vboxlayout = QtGui.QVBoxLayout(StringPropertyModifier)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setObjectName("vboxlayout")

        self.propGroupBox = QtGui.QGroupBox(StringPropertyModifier)
        self.propGroupBox.setObjectName("propGroupBox")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.propGroupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.stringEdit = QtGui.QLineEdit(self.propGroupBox)
        self.stringEdit.setObjectName("stringEdit")
        self.vboxlayout1.addWidget(self.stringEdit)
        self.vboxlayout.addWidget(self.propGroupBox)

        self.retranslateUi(StringPropertyModifier)
        QtCore.QMetaObject.connectSlotsByName(StringPropertyModifier)

    def retranslateUi(self, StringPropertyModifier):
        StringPropertyModifier.setWindowTitle(QtGui.QApplication.translate("StringPropertyModifier", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.propGroupBox.setTitle(QtGui.QApplication.translate("StringPropertyModifier", "String", None, QtGui.QApplication.UnicodeUTF8))

