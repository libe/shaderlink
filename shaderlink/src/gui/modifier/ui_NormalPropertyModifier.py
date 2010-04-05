##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui\modifier\ui_NormalPropertyModifier.ui'
#
# Created: Sat Nov 01 11:06:12 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NormalPropertyModifier(object):
    def setupUi(self, NormalPropertyModifier):
        NormalPropertyModifier.setObjectName("NormalPropertyModifier")
        NormalPropertyModifier.resize(232, 114)
        NormalPropertyModifier.setMinimumSize(QtCore.QSize(232, 114))
        NormalPropertyModifier.setMaximumSize(QtCore.QSize(232, 114))
        self.verticalLayout_2 = QtGui.QVBoxLayout(NormalPropertyModifier)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.propGroupBox = QtGui.QGroupBox(NormalPropertyModifier)
        self.propGroupBox.setObjectName("propGroupBox")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.propGroupBox)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.xLabel = QtGui.QLabel(self.propGroupBox)
        self.xLabel.setMinimumSize(QtCore.QSize(7, 15))
        self.xLabel.setMaximumSize(QtCore.QSize(7, 15))
        self.xLabel.setObjectName("xLabel")
        self.horizontalLayout.addWidget(self.xLabel)
        self.xEdit = QtGui.QLineEdit(self.propGroupBox)
        self.xEdit.setMinimumSize(QtCore.QSize(50, 20))
        self.xEdit.setMaximumSize(QtCore.QSize(50, 20))
        self.xEdit.setObjectName("xEdit")
        self.horizontalLayout.addWidget(self.xEdit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.yLabel = QtGui.QLabel(self.propGroupBox)
        self.yLabel.setMinimumSize(QtCore.QSize(7, 15))
        self.yLabel.setMaximumSize(QtCore.QSize(7, 15))
        self.yLabel.setObjectName("yLabel")
        self.horizontalLayout_2.addWidget(self.yLabel)
        self.yEdit = QtGui.QLineEdit(self.propGroupBox)
        self.yEdit.setMinimumSize(QtCore.QSize(50, 20))
        self.yEdit.setMaximumSize(QtCore.QSize(50, 20))
        self.yEdit.setObjectName("yEdit")
        self.horizontalLayout_2.addWidget(self.yEdit)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.zLabel = QtGui.QLabel(self.propGroupBox)
        self.zLabel.setMinimumSize(QtCore.QSize(7, 15))
        self.zLabel.setMaximumSize(QtCore.QSize(7, 15))
        self.zLabel.setObjectName("zLabel")
        self.horizontalLayout_3.addWidget(self.zLabel)
        self.zEdit = QtGui.QLineEdit(self.propGroupBox)
        self.zEdit.setMinimumSize(QtCore.QSize(50, 20))
        self.zEdit.setMaximumSize(QtCore.QSize(60, 20))
        self.zEdit.setObjectName("zEdit")
        self.horizontalLayout_3.addWidget(self.zEdit)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        spacerItem3 = QtGui.QSpacerItem(77, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.spaceLabel = QtGui.QLabel(self.propGroupBox)
        self.spaceLabel.setObjectName("spaceLabel")
        self.hboxlayout.addWidget(self.spaceLabel)
        self.spaceCombo = QtGui.QComboBox(self.propGroupBox)
        self.spaceCombo.setMinimumSize(QtCore.QSize(0, 0))
        self.spaceCombo.setMaximumSize(QtCore.QSize(100, 16777215))
        self.spaceCombo.setObjectName("spaceCombo")
        self.hboxlayout.addWidget(self.spaceCombo)
        self.vboxlayout.addLayout(self.hboxlayout)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem4)
        self.horizontalLayout_5.addLayout(self.vboxlayout)
        self.verticalLayout_2.addWidget(self.propGroupBox)

        self.retranslateUi(NormalPropertyModifier)
        QtCore.QMetaObject.connectSlotsByName(NormalPropertyModifier)

    def retranslateUi(self, NormalPropertyModifier):
        NormalPropertyModifier.setWindowTitle(QtGui.QApplication.translate("NormalPropertyModifier", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.propGroupBox.setTitle(QtGui.QApplication.translate("NormalPropertyModifier", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.xLabel.setText(QtGui.QApplication.translate("NormalPropertyModifier", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.yLabel.setText(QtGui.QApplication.translate("NormalPropertyModifier", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.zLabel.setText(QtGui.QApplication.translate("NormalPropertyModifier", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.spaceLabel.setText(QtGui.QApplication.translate("NormalPropertyModifier", "Space", None, QtGui.QApplication.UnicodeUTF8))

