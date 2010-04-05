##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

from PyQt4 import QtGui, QtCore

import ui_ColorPropertyModifier
import ui_FloatPropertyModifier
import ui_MatrixPropertyModifier
import ui_PointPropertyModifier
import ui_StringPropertyModifier
import ui_VectorPropertyModifier
import ui_NormalPropertyModifier

class ColorPropertyModifier(QtGui.QWidget,
                            ui_ColorPropertyModifier.Ui_ColorPropertyModifier):
        
    def __init__(self, colorProperty, commandProcessor, parent = None):
        super(QtGui.QWidget, self).__init__(parent)        
        self.colorProperty = colorProperty
        self.commandProcessor = commandProcessor

        # build the gui
        self.buildGui()

        # update the gui
        self.updateGui(self.colorProperty.value[0],
                       self.colorProperty.value[1],
                       self.colorProperty.value[2])

        # create controller
        from controller import ColorPropertyModifierController        
        self.colorPropertyModifierController = ColorPropertyModifierController(self, commandProcessor)
        
        # install a custom filter in order to avoid subclassing
        self.previewImg.installEventFilter(self.colorPropertyModifierController.previewImgFilter)
        
        # connect signals
        self.connectSignals()
        
        # register signal propertyChanged for updating the gui
        self.connect(self.colorProperty, QtCore.SIGNAL('propertyChanged()'), 
                     self.onPropertyChanged)

    def connectSignals(self):
        self.connect(self.redSlider, QtCore.SIGNAL('valueChanged(int)'), 
                     self.colorPropertyModifierController.onRedSliderValueChanged)
        self.connect(self.greenSlider, QtCore.SIGNAL('valueChanged(int)'), 
                     self.colorPropertyModifierController.onGreenSliderValueChanged)
        self.connect(self.blueSlider, QtCore.SIGNAL('valueChanged(int)'), 
                     self.colorPropertyModifierController.onBlueSliderValueChanged)

        self.connect(self.redSlider, QtCore.SIGNAL('sliderMoved(int)'),
                     self.onRedSliderMoved)
        self.connect(self.blueSlider, QtCore.SIGNAL('sliderMoved(int)'),
                     self.onBlueSliderMoved)
        self.connect(self.greenSlider, QtCore.SIGNAL('sliderMoved(int)'),
                     self.onGreenSliderMoved)
        
        self.connect(self.redEdit, QtCore.SIGNAL('editingFinished()'),
                     self.colorPropertyModifierController.onRedEditEditingFinished)

        self.connect(self.blueEdit, QtCore.SIGNAL('editingFinished()'),
                     self.colorPropertyModifierController.onBlueEditEditingFinished)

        self.connect(self.greenEdit, QtCore.SIGNAL('editingFinished()'),
                     self.colorPropertyModifierController.onGreenEditEditingFinished)

    def disconnectSignals(self):
        self.disconnect(self.redSlider, QtCore.SIGNAL('valueChanged(int)'), 
                        self.colorPropertyModifierController.onRedSliderValueChanged)
        self.disconnect(self.greenSlider, QtCore.SIGNAL('valueChanged(int)'), 
                        self.colorPropertyModifierController.onGreenSliderValueChanged)
        self.disconnect(self.blueSlider, QtCore.SIGNAL('valueChanged(int)'), 
                        self.colorPropertyModifierController.onBlueSliderValueChanged)

        self.disconnect(self.redSlider, QtCore.SIGNAL('sliderMoved(int)'),
                        self.onRedSliderMoved)
        self.disconnect(self.blueSlider, QtCore.SIGNAL('sliderMoved(int)'),
                        self.onBlueSliderMoved)
        self.disconnect(self.greenSlider, QtCore.SIGNAL('sliderMoved(int)'),
                        self.onGreenSliderMoved)   

        self.disconnect(self.redEdit, QtCore.SIGNAL('editingFinished()'),
                        self.colorPropertyModifierController.onRedEditEditingFinished)

        self.disconnect(self.blueEdit, QtCore.SIGNAL('editingFinished()'),
                        self.colorPropertyModifierController.onBlueEditEditingFinished)

        self.disconnect(self.greenEdit, QtCore.SIGNAL('editingFinished()'),
                        self.colorPropertyModifierController.onGreenEditEditingFinished)                                     
    
    def onPropertyChanged(self):
        self.disconnectSignals()
        
        self.updateGui(self.colorProperty.value[0],
                       self.colorProperty.value[1],
                       self.colorProperty.value[2])
        
        self.connectSignals()

    def onRedSliderMoved(self, value):
        r = value / 1000.0
        b = self.colorProperty.value[1]
        g = self.colorProperty.value[2]
        
        self.updatePreview(r, b, g)
        self.updateEdits(r, b, g)

    def onGreenSliderMoved(self, value):
        r = self.colorProperty.value[0]
        b = value / 1000.0
        g = self.colorProperty.value[2]
        
        self.updatePreview(r, b, g)
        self.updateEdits(r, b, g)

    def onBlueSliderMoved(self, value):
        r = self.colorProperty.value[0]
        b = self.colorProperty.value[1]
        g = value / 1000.0
        
        self.updatePreview(r, b, g)
        self.updateEdits(r, b, g)
        
    def setupSlider(self, slider):
        slider.setTracking(False)
        slider.setMinimum(0)
        slider.setMaximum(1000)
        slider.setTickInterval(100)    
        
    def setupEdit(self, edit):
        validator = QtGui.QDoubleValidator(0.0, 1.0, 3, self) 
        edit.setValidator(validator)
            
    def buildGui(self):
        # build the gui created with QtDesigner
        self.setupUi(self)
        
        # set up gui
        self.propGroupBox.setTitle('%s %s' % (self.colorProperty.typeToStr(), self.colorProperty.name))
        self.setupSlider(self.redSlider)
        self.setupSlider(self.greenSlider)
        self.setupSlider(self.blueSlider)
        
        self.setupEdit(self.redEdit)
        self.setupEdit(self.blueEdit)
        self.setupEdit(self.greenEdit)

    def updateGui(self, r, g, b):
        self.updatePreview(r, g, b)
        self.updateSliders(r, g, b)
        self.updateEdits(r, g, b)
        
    def updatePreview(self, r, g, b):
        pixmap = QtGui.QPixmap(60, 80)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter()
        painter.begin(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        
        color = QtGui.QColor(r * 255,
                             g * 255,
                             b * 255)
        
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(color)  
        rect = QtCore.QRectF(0.0, 0.0, 60.0, 80.0)
        painter.drawRoundRect(rect, 20.0, 15.0)
        painter.end()
        
        self.previewImg.setPixmap(pixmap)
        
    def updateSliders(self, r, g, b):
        redSliderValue = int(r * 1000.0)
        greenSliderValue = int(g * 1000.0)
        blueSliderValue = int(b * 1000.0)
        
        self.redSlider.setValue(redSliderValue)
        self.greenSlider.setValue(greenSliderValue)
        self.blueSlider.setValue(blueSliderValue)
        
    def updateEdits(self, r, g, b):        
        self.redEdit.setText(QtCore.QString.number(r, 'f', 3))
        self.greenEdit.setText(QtCore.QString.number(g, 'f', 3))
        self.blueEdit.setText(QtCore.QString.number(b, 'f', 3))
                
class FloatPropertyModifier(QtGui.QWidget,
                            ui_FloatPropertyModifier.Ui_FloatPropertyModifier):
    def __init__(self, floatProperty, commandProcessor, parent = None):
        super(QtGui.QWidget, self).__init__(None)        
        self.floatProperty = floatProperty

        # build the gui
        self.buildGui()
        
        # update the gui
        self.updateGui(self.floatProperty.value)

        # create controller
        from controller import FloatPropertyModifierController        
        self.floatPropertyModifierController = FloatPropertyModifierController(self, commandProcessor)
                
        # connect signals
        self.connectSignals()
        
        # register signal propertyChanged for updating the gui
        self.connect(self.floatProperty, QtCore.SIGNAL('propertyChanged()'), 
                     self.onPropertyChanged)

    def connectSignals(self):
        self.connect(self.floatEdit, QtCore.SIGNAL('editingFinished()'),
                     self.floatPropertyModifierController.onFloatEditEditingFinished)

    def disconnectSignals(self):
        self.disconnect(self.floatEdit, QtCore.SIGNAL('editingFinished()'),
                        self.floatPropertyModifierController.onFloatEditEditingFinished)
    
    def onPropertyChanged(self):
        self.disconnectSignals()
        
        self.updateGui(self.floatProperty.value)
        
        self.connectSignals()
                    
    def buildGui(self):
        # build the gui created with QtDesigner
        self.setupUi(self)
        
        # set up gui
        self.propGroupBox.setTitle('%s %s' % (self.floatProperty.typeToStr(), self.floatProperty.name))
    
        self.setupEdit(self.floatEdit)
        
    def setupEdit(self, edit):
        # TODO: min and max value handling
        validator = QtGui.QDoubleValidator(self) 
        validator.setDecimals(3)
        edit.setValidator(validator)
    
    def updateGui(self, value):
        self.updateEdit(value)
                
    def updateEdit(self, value):        
        self.floatEdit.setText(QtCore.QString.number(value, 'f', 3))
        
class MatrixPropertyModifier(QtGui.QWidget,
                             ui_MatrixPropertyModifier.Ui_MatrixPropertyModifier):
    def __init__(self, matrixProperty, commandProcessor, parent = None):
        super(QtGui.QWidget, self).__init__(None)        
        self.matrixProperty = matrixProperty

        # build the gui
        self.buildGui()
        
        # update the gui
        self.updateGui(self.matrixProperty.value)

        # create controller
        from controller import MatrixPropertyModifierController        
        self.matrixPropertyModifierController = MatrixPropertyModifierController(self, commandProcessor)
                
        # connect signals
        self.connectSignals()
        
        # register signal propertyChanged for updating the gui
        self.connect(self.matrixProperty, QtCore.SIGNAL('propertyChanged()'), 
                     self.onPropertyChanged)

    def connectSignals(self):
        for r in range(4):
            for c in range(4):        
                self.connect(self.matEdits[r][c], QtCore.SIGNAL('editingFinished()'),
                             self.matrixPropertyModifierController.slots[r][c])

    def disconnectSignals(self):
        for r in range(4):
            for c in range(4):        
                self.disconnect(self.matEdits[r][c], QtCore.SIGNAL('editingFinished()'),
                                self.matrixPropertyModifierController.slots[r][c])
    
    def onPropertyChanged(self):
        self.disconnectSignals()
        
        self.updateGui(self.matrixProperty.value)
        
        self.connectSignals()
                    
    def buildGui(self):
        # build the gui created with QtDesigner
        self.setupUi(self)

        # set up gui
        self.propGroupBox.setTitle('%s %s' % (self.matrixProperty.typeToStr(), self.matrixProperty.name))

        # store edit references in matrix
        self.matEdits = [[self.matEdit_0_0, self.matEdit_0_1, self.matEdit_0_2, self.matEdit_0_3],
                         [self.matEdit_1_0, self.matEdit_1_1, self.matEdit_1_2, self.matEdit_1_3],
                         [self.matEdit_2_0, self.matEdit_2_1, self.matEdit_2_2, self.matEdit_2_3],
                         [self.matEdit_3_0, self.matEdit_3_1, self.matEdit_3_2, self.matEdit_3_3]]
        
    def updateGui(self, value):
        for r in range(4):
            for c in range(4):        
                self.matEdits[r][c].setText(QtCore.QString.number(value[r][c], 'f', 3))

class Tuple3DPropertyModifier(QtGui.QWidget,
                              ui_PointPropertyModifier.Ui_PointPropertyModifier):
    def __init__(self, tuple3DProperty, commandProcessor, parent = None):
        super(QtGui.QWidget, self).__init__(None)        
        self.tuple3DProperty = tuple3DProperty

         # build the gui
        self.buildGui()
        
        # update the gui
        self.updateGui(self.tuple3DProperty.value[0],
                       self.tuple3DProperty.value[1],
                       self.tuple3DProperty.value[2],
                       self.tuple3DProperty.spaces[self.tuple3DProperty.spaceIndex])

        # create controller
        from controller import Tuple3DPropertyModifierController        
        self.tuple3DModifierController = Tuple3DPropertyModifierController(self, commandProcessor)
        
        # connect signals
        self.connectSignals()
        
        # register signal propertyChanged for updating the gui
        self.connect(self.tuple3DProperty, QtCore.SIGNAL('propertyChanged()'), 
                     self.onPropertyChanged)
            
    def buildGui(self):
        # build the gui created with QtDesigner
        self.setupUi(self)
        
        # set up gui
        self.propGroupBox.setTitle('%s %s' % (self.tuple3DProperty.typeToStr(), self.tuple3DProperty.name))
        
        self.setupEdit(self.xEdit)        
        self.setupEdit(self.yEdit)
        self.setupEdit(self.zEdit)
        
        self.setupCombo(self.spaceCombo)

    def onPropertyChanged(self):
        self.disconnectSignals()
        
        self.updateGui(self.tuple3DProperty.value[0],
                       self.tuple3DProperty.value[1],
                       self.tuple3DProperty.value[2],
                       self.tuple3DProperty.spaces[self.tuple3DProperty.spaceIndex])
        
        self.connectSignals()
    
    def connectSignals(self):
        self.connect(self.spaceCombo, QtCore.SIGNAL('activated(const QString &)'),
                     self.tuple3DModifierController.onSpaceComboActivated)
                
        self.connect(self.xEdit, QtCore.SIGNAL('editingFinished()'),
                     self.tuple3DModifierController.onXEditEditingFinished)

        self.connect(self.yEdit, QtCore.SIGNAL('editingFinished()'),
                     self.tuple3DModifierController.onYEditEditingFinished)

        self.connect(self.zEdit, QtCore.SIGNAL('editingFinished()'),
                     self.tuple3DModifierController.onZEditEditingFinished)        

    def disconnectSignals(self):
        self.disconnect(self.spaceCombo, QtCore.SIGNAL('activated(const QString &)'),
                        self.tuple3DModifierController.onSpaceComboActivated)
                
        self.disconnect(self.xEdit, QtCore.SIGNAL('editingFinished()'),
                        self.tuple3DModifierController.onXEditEditingFinished)

        self.disconnect(self.yEdit, QtCore.SIGNAL('editingFinished()'),
                        self.tuple3DModifierController.onYEditEditingFinished)

        self.disconnect(self.zEdit, QtCore.SIGNAL('editingFinished()'),
                        self.tuple3DModifierController.onZEditEditingFinished)        
    
    def updateGui(self, r, g, b, space):
        self.updateEdits(r, g, b)
        self.updateCombo(space)

    def updateEdits(self, r, g, b):        
        self.xEdit.setText(QtCore.QString.number(r, 'f', 3))
        self.yEdit.setText(QtCore.QString.number(g, 'f', 3))
        self.zEdit.setText(QtCore.QString.number(b, 'f', 3))
        
    def updateCombo(self, space):
        index = self.tuple3DProperty.spaces.index(space)
        self.spaceCombo.setCurrentIndex(index)
        
    def setupEdit(self, edit):
        validator = QtGui.QDoubleValidator(self)
        validator.setDecimals(3)
        edit.setValidator(validator)
        
    def setupCombo(self, combo):
        for space in self.tuple3DProperty.spaces:
            combo.addItem(space)

class StringPropertyModifier(QtGui.QWidget,
                             ui_StringPropertyModifier.Ui_StringPropertyModifier):
    def __init__(self, stringProperty, commandProcessor, parent = None):
        super(QtGui.QWidget, self).__init__(None)        
        self.stringProperty = stringProperty

        # build the gui
        self.buildGui()
        
        # update the gui
        self.updateGui(self.stringProperty.value)

        # create controller
        from controller import StringPropertyModifierController        
        self.stringPropertyModifierController = StringPropertyModifierController(self, commandProcessor)
                
        # connect signals
        self.connectSignals()
        
        # register signal propertyChanged for updating the gui
        self.connect(self.stringProperty, QtCore.SIGNAL('propertyChanged()'), 
                     self.onPropertyChanged)
                
    def buildGui(self):
        # build the gui created with QtDesigner
        self.setupUi(self)
        
        # set up gui
        self.propGroupBox.setTitle('%s %s' % (self.stringProperty.typeToStr(), self.stringProperty.name))    
        
    def connectSignals(self):
        self.connect(self.stringEdit, QtCore.SIGNAL('editingFinished()'),
                     self.stringPropertyModifierController.onStringEditEditingFinished)

    def disconnectSignals(self):
        self.disconnect(self.stringEdit, QtCore.SIGNAL('editingFinished()'),
                        self.stringPropertyModifierController.onStringEditEditingFinished)
    
    def onPropertyChanged(self):
        self.disconnectSignals()
        
        self.updateGui(self.stringProperty.value)
        
        self.connectSignals()
                               
    def updateGui(self, value):
        self.updateEdit(value)
                
    def updateEdit(self, value):        
        self.stringEdit.setText(value)
             
                
