##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_RendererSettings.ui'
#
# Created: Tue Dec 15 00:12:53 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RendererSettings(object):
    def setupUi(self, RendererSettings):
        RendererSettings.setObjectName("RendererSettings")
        RendererSettings.resize(628, 123)
        self.verticalLayout = QtGui.QVBoxLayout(RendererSettings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(RendererSettings)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.rendererCombo = QtGui.QComboBox(RendererSettings)
        self.rendererCombo.setObjectName("rendererCombo")
        self.gridLayout.addWidget(self.rendererCombo, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(RendererSettings)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.compilerPathLE = QtGui.QLineEdit(RendererSettings)
        self.compilerPathLE.setReadOnly(True)
        self.compilerPathLE.setObjectName("compilerPathLE")
        self.gridLayout.addWidget(self.compilerPathLE, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(RendererSettings)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.rendererPathLE = QtGui.QLineEdit(RendererSettings)
        self.rendererPathLE.setReadOnly(True)
        self.rendererPathLE.setObjectName("rendererPathLE")
        self.gridLayout.addWidget(self.rendererPathLE, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(RendererSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RendererSettings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), RendererSettings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), RendererSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(RendererSettings)

    def retranslateUi(self, RendererSettings):
        RendererSettings.setWindowTitle(QtGui.QApplication.translate("RendererSettings", "Renderer Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RendererSettings", "Renderer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RendererSettings", "Compiler Path", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("RendererSettings", "Renderer Path", None, QtGui.QApplication.UnicodeUTF8))

