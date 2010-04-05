##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

from PyQt4 import QtCore, QtGui

class PreviewImgFilter(QtCore.QObject):
    def __init__(self, colorPropertyModifier, commandProcessor):
        QtCore.QObject.__init__(self, None)
        self.colorPropertyModifier = colorPropertyModifier
        self.commandProcessor = commandProcessor
            
    def eventFilter(self, obj, event):
        # check for single click
        if event.type() == QtCore.QEvent.MouseButtonPress:
            redValue = int(self.colorPropertyModifier.colorProperty.value[0] * 255)
            greenValue = int(self.colorPropertyModifier.colorProperty.value[1] * 255)
            blueValue = int(self.colorPropertyModifier.colorProperty.value[2] * 255)
            colorSelected = QtGui.QColorDialog.getColor(QtGui.QColor(redValue, greenValue, blueValue),
                                                        self.colorPropertyModifier.parent().parent())
            if colorSelected.isValid():
                newValue = (colorSelected.redF(),
                            colorSelected.greenF(),
                            colorSelected.blueF())        
                # create edit property command
                from command.command import EditPropertyCommand
                editPropertyCommand = EditPropertyCommand(self.colorPropertyModifier.colorProperty, newValue)   
                self.commandProcessor.executeCommand(editPropertyCommand)
                
            return True
        else:
            return obj.eventFilter(obj, event)
            
class ColorPropertyModifierController(object):
    def __init__(self, colorPropertyModifier, commandProcessor):
        self.colorPropertyModifier = colorPropertyModifier
        self.commandProcessor = commandProcessor
        
        self.previewImgFilter = PreviewImgFilter(self.colorPropertyModifier, 
                                                 self.commandProcessor)

    def onRedSliderValueChanged(self, intValue):
        redValue = float(intValue) / 1000.0
        newValue = (redValue,
                    self.colorPropertyModifier.colorProperty.value[1],
                    self.colorPropertyModifier.colorProperty.value[2])        
        # create edit property command
        from command.command import EditPropertyCommand
        editPropertyCommand = EditPropertyCommand(self.colorPropertyModifier.colorProperty, newValue)   
        self.commandProcessor.executeCommand(editPropertyCommand)

    def onGreenSliderValueChanged(self, intValue):
        greenValue = float(intValue) / 1000.0        
        newValue = (self.colorPropertyModifier.colorProperty.value[0],
                    greenValue,
                    self.colorPropertyModifier.colorProperty.value[2])        
        # create edit property command
        from command.command import EditPropertyCommand
        editPropertyCommand = EditPropertyCommand(self.colorPropertyModifier.colorProperty, newValue)   
        self.commandProcessor.executeCommand(editPropertyCommand)

    def onBlueSliderValueChanged(self, intValue):
        blueValue = float(intValue) / 1000.0        
        newValue = (self.colorPropertyModifier.colorProperty.value[0],
                    self.colorPropertyModifier.colorProperty.value[1],
                    blueValue)        
        # create edit property command
        from command.command import EditPropertyCommand
        editPropertyCommand = EditPropertyCommand(self.colorPropertyModifier.colorProperty, newValue)   
        self.commandProcessor.executeCommand(editPropertyCommand)

    def onRedEditEditingFinished(self):
        redStr = self.colorPropertyModifier.redEdit.text()
        redValue = redStr.toFloat()[0]        
        if redValue == self.colorPropertyModifier.colorProperty.value[0]:
            return
        newValue = (redValue,
                    self.colorPropertyModifier.colorProperty.value[1],
                    self.colorPropertyModifier.colorProperty.value[2])        
        # create edit property command
        from command.command import EditPropertyCommand
        editPropertyCommand = EditPropertyCommand(self.colorPropertyModifier.colorProperty, newValue)   
        self.commandProcessor.executeCommand(editPropertyCommand)
        
    def onGreenEditEditingFinished(self):
        greenStr = self.colorPropertyModifier.greenEdit.text()
        greenValue = greenStr.toFloat()[0]        
        if greenValue == self.colorPropertyModifier.colorProperty.value[1]:
            return
        newValue = (self.colorPropertyModifier.colorProperty.value[0],
                    greenValue,
                    self.colorPropertyModifier.colorProperty.value[2])        
        # create edit property command
        from command.command import EditPropertyCommand
        editPropertyCommand = EditPropertyCommand(self.colorPropertyModifier.colorProperty, newValue)   
        self.commandProcessor.executeCommand(editPropertyCommand)

    def onBlueEditEditingFinished(self):
        blueStr = self.colorPropertyModifier.blueEdit.text()
        blueValue = blueStr.toFloat()[0]
        if blueValue == self.colorPropertyModifier.colorProperty.value[2]:
            return
        newValue = (self.colorPropertyModifier.colorProperty.value[0],
                    self.colorPropertyModifier.colorProperty.value[1],
                    blueValue)        
        # create edit property command
        from command.command import EditPropertyCommand
        editPropertyCommand = EditPropertyCommand(self.colorPropertyModifier.colorProperty, newValue)   
        self.commandProcessor.executeCommand(editPropertyCommand)

class FloatPropertyModifierController(object):
    def __init__(self, floatPropertyModifier, commandProcessor):
        self.floatPropertyModifier = floatPropertyModifier
        self.commandProcessor = commandProcessor

    def onFloatEditEditingFinished(self):
        floatStr = self.floatPropertyModifier.floatEdit.text()
        floatValue = floatStr.toFloat()[0]        
        if floatValue == self.floatPropertyModifier.floatProperty.value:
            return
        newValue = floatValue        
        # create edit property command
        from command.command import EditPropertyCommand
        editPropertyCommand = EditPropertyCommand(self.floatPropertyModifier.floatProperty, newValue)   
        self.commandProcessor.executeCommand(editPropertyCommand)
        
class MatrixPropertyModifierController(object):
    def __init__(self, matrixPropertyModifier, commandProcessor):
        self.matrixPropertyModifier = matrixPropertyModifier
        self.commandProcessor = commandProcessor

        # build slots
        self.buildSlots()
        
    def buildSlots(self):
        self.slots = []
        
        # use python automagic partial functions
        import functools
        for r in range(4):
            row = []
            for c in range(4):                        
                row.append(functools.partial(self.onMatrixEditEditingFinished, r, c))
            self.slots.append(row)
                
    def onMatrixEditEditingFinished(self, r, c):
        floatStr = self.matrixPropertyModifier.matEdits[r][c].text()
        floatValue = floatStr.toFloat()[0]        
        if floatValue == self.matrixPropertyModifier.matrixProperty.value[r][c]:
            return
        import copy
        newValue = copy.deepcopy(self.matrixPropertyModifier.matrixProperty.value)
        newValue[r][c] = floatValue
        # create edit property command
        from command.command import EditPropertyCommand
        editPropertyCommand = EditPropertyCommand(self.matrixPropertyModifier.matrixProperty, newValue)   
        self.commandProcessor.executeCommand(editPropertyCommand)

class Tuple3DPropertyModifierController(object):
    def __init__(self, tuple3DPropertyModifier, commandProcessor):
        self.tuple3DPropertyModifier = tuple3DPropertyModifier
        self.commandProcessor = commandProcessor

    def onSpaceComboActivated(self, text):
        spaceIndex = self.tuple3DPropertyModifier.spaceCombo.currentIndex()
        
        # create edit property command
        from command.command import EditTuple3DPropertyCommand
        editPropertyCommand = EditTuple3DPropertyCommand(self.tuple3DPropertyModifier.tuple3DProperty, 
                                                         self.tuple3DPropertyModifier.tuple3DProperty.value,
                                                         spaceIndex)   
        self.commandProcessor.executeCommand(editPropertyCommand)
                
    def onXEditEditingFinished(self):
        xStr = self.tuple3DPropertyModifier.xEdit.text()
        xValue = xStr.toFloat()[0]        
        if xValue == self.tuple3DPropertyModifier.tuple3DProperty.value[0]:
            return
        newValue = (xValue,
                    self.tuple3DPropertyModifier.tuple3DProperty.value[1],
                    self.tuple3DPropertyModifier.tuple3DProperty.value[2])
                
        # create edit property command
        from command.command import EditTuple3DPropertyCommand
        editPropertyCommand = EditTuple3DPropertyCommand(self.tuple3DPropertyModifier.tuple3DProperty, 
                                                         newValue,
                                                         self.tuple3DPropertyModifier.tuple3DProperty.spaceIndex)   
        self.commandProcessor.executeCommand(editPropertyCommand)
        
    def onYEditEditingFinished(self):
        yStr = self.tuple3DPropertyModifier.yEdit.text()
        yValue = yStr.toFloat()[0]        
        if yValue == self.tuple3DPropertyModifier.tuple3DProperty.value[1]:
            return
        newValue = (self.tuple3DPropertyModifier.tuple3DProperty.value[0],
                    yValue,
                    self.tuple3DPropertyModifier.tuple3DProperty.value[2])
        
        # create edit property command
        from command.command import EditTuple3DPropertyCommand
        editPropertyCommand = EditTuple3DPropertyCommand(self.tuple3DPropertyModifier.tuple3DProperty, 
                                                         newValue,
                                                         self.tuple3DPropertyModifier.tuple3DProperty.spaceIndex)   
        self.commandProcessor.executeCommand(editPropertyCommand)

    def onZEditEditingFinished(self):
        zStr = self.tuple3DPropertyModifier.zEdit.text()
        zValue = zStr.toFloat()[0]        
        if zValue == self.tuple3DPropertyModifier.tuple3DProperty.value[2]:
            return
        newValue = (self.tuple3DPropertyModifier.tuple3DProperty.value[0],
                    self.tuple3DPropertyModifier.tuple3DProperty.value[1],
                    zValue)
                
        # create edit property command
        from command.command import EditTuple3DPropertyCommand
        editPropertyCommand = EditTuple3DPropertyCommand(self.tuple3DPropertyModifier.tuple3DProperty, 
                                                         newValue,
                                                         self.tuple3DPropertyModifier.tuple3DProperty.spaceIndex)   
        self.commandProcessor.executeCommand(editPropertyCommand)

class StringPropertyModifierController(object):
    def __init__(self, stringPropertyModifier, commandProcessor):
        self.stringPropertyModifier = stringPropertyModifier
        self.commandProcessor = commandProcessor

    def onStringEditEditingFinished(self):
        stringStr = self.stringPropertyModifier.stringEdit.text()
        stringValue = stringStr        
        if stringValue == self.stringPropertyModifier.stringProperty.value:
            return
        newValue = stringValue        
        # create edit property command
        from command.command import EditPropertyCommand
        editPropertyCommand = EditPropertyCommand(self.stringPropertyModifier.stringProperty, newValue)   
        self.commandProcessor.executeCommand(editPropertyCommand)
        