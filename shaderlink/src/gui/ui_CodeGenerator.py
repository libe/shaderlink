##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_CodeGenerator.ui'
#
# Created: Mon Dec 14 23:13:48 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_CodeGenerator(object):
    def setupUi(self, CodeGenerator):
        CodeGenerator.setObjectName("CodeGenerator")
        CodeGenerator.resize(825, 675)
        self.verticalLayout_6 = QtGui.QVBoxLayout(CodeGenerator)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.splitter = QtGui.QSplitter(CodeGenerator)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtGui.QGroupBox(self.layoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.shadersLW = QtGui.QListWidget(self.groupBox)
        self.shadersLW.setObjectName("shadersLW")
        self.verticalLayout.addWidget(self.shadersLW)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.layoutWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.parametersTW = QtGui.QTreeWidget(self.groupBox_2)
        self.parametersTW.setObjectName("parametersTW")
        self.verticalLayout_2.addWidget(self.parametersTW)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_3 = QtGui.QGroupBox(self.layoutWidget1)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.codeEdit = QtGui.QTextEdit(self.groupBox_3)
        self.codeEdit.setObjectName("codeEdit")
        self.verticalLayout_4.addWidget(self.codeEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.exportB = QtGui.QPushButton(self.groupBox_3)
        self.exportB.setObjectName("exportB")
        self.horizontalLayout.addWidget(self.exportB)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addWidget(self.groupBox_3)
        self.verticalLayout_6.addWidget(self.splitter)

        self.retranslateUi(CodeGenerator)
        QtCore.QMetaObject.connectSlotsByName(CodeGenerator)

    def retranslateUi(self, CodeGenerator):
        CodeGenerator.setWindowTitle(QtGui.QApplication.translate("CodeGenerator", "Code Generator", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("CodeGenerator", "Shaders", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("CodeGenerator", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.parametersTW.headerItem().setText(0, QtGui.QApplication.translate("CodeGenerator", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("CodeGenerator", "Code", None, QtGui.QApplication.UnicodeUTF8))
        self.exportB.setText(QtGui.QApplication.translate("CodeGenerator", "Export...", None, QtGui.QApplication.UnicodeUTF8))

