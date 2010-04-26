##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

from PyQt4 import QtCore
from command.command import *

class MainWindowController(QtCore.QObject):
    def __init__(self, mainWindow):
        QtCore.QObject.__init__(self)
        
        self.mainWindow = mainWindow
        
        self.commandProcessor = mainWindow.commandProcessor

    def okToContinue(self):
        if self.mainWindow.shaderLink.dirtyState:
            reply = QtGui.QMessageBox.question(self.mainWindow,
                                               'ShaderLink - Unsaved Changes',
                                               'Save unsaved changes?',
                                               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return False
            elif reply == QtGui.QMessageBox.Yes:
                self.onSaveProject()
        return True
        
    def onNewProject(self):
        if not self.okToContinue():
            return
        
        # create a new command
        newCommand = NewCommand(self.mainWindow)
        self.commandProcessor.executeCommand(newCommand)

    def onOpenRecentFile(self):
        action = self.sender()
        if isinstance(action, QtGui.QAction):
            fname = unicode(action.data().toString())
            if not fname:
                return 
            
            # create an open command
            openCommand = OpenCommand(self.mainWindow, fname)
            self.commandProcessor.executeCommand(openCommand)
                    
    def onOpenProject(self):
        if not self.okToContinue():
            return
        
        # try to get filename's dir
        import os
        dir = os.path.dirname(self.mainWindow.fileName) if self.mainWindow.fileName != '' else '.'
        
        formats = ['*.shl']
        fileName = unicode(QtGui.QFileDialog.getOpenFileName(self.mainWindow,
                                                             'ShaderLink - Open Project', dir,
                                                             'Project files (%s)' % ' '.join(formats)))
        
        if not fileName:
            return 
        
        # create an open command
        openCommand = OpenCommand(self.mainWindow, fileName)
        self.commandProcessor.executeCommand(openCommand)                
        
    def onSaveProject(self):
        if self.mainWindow.fileName == '':
            self.onSaveAsProject()
            return
        
        # create a save command
        saveCommand = SaveCommand(self.mainWindow, self.mainWindow.fileName)
        self.commandProcessor.executeCommand(saveCommand)       

    def onSaveAsProject(self):
        fileName = self.mainWindow.fileName if self.mainWindow.fileName != '' else '.'
        formats = ['*.shl']
        fileName = unicode(QtGui.QFileDialog.getSaveFileName(self.mainWindow,
                                                             'ShaderLink - Save Project', fileName,
                                                             'Project files (%s)' % ' '.join(formats)))
        if not fileName:
            return 
        
        # create a save command
        saveCommand = SaveCommand(self.mainWindow, fileName)
        self.commandProcessor.executeCommand(saveCommand)       

    def onUndo(self):
        # create an undo command
        undoCommand = UndoCommand(self.commandProcessor)
        self.commandProcessor.executeCommand(undoCommand)

    def onRedo(self):
        # create a redo command
        redoCommand = RedoCommand(self.commandProcessor)
        self.commandProcessor.executeCommand(redoCommand)

    def onCopy(self):
        scene = self.mainWindow.gfxPanel.scene()
        selectedItems = scene.selectedItems()   
        # create a copy command                         
        copyCommand = CopyCommand(selectedItems)   
        self.commandProcessor.executeCommand(copyCommand)
            
        # save the copy command into the command processor for later paste command
        self.commandProcessor.setCopyCommand(copyCommand)

    def onPaste(self):
        # create a paste command                         
        pasteCommand = PasteCommand(self.mainWindow.shaderLink, 
                                    self.mainWindow.gfxPanel,
                                    self.commandProcessor.copyCommand)   
        self.commandProcessor.executeCommand(pasteCommand)
        
    def onDelete(self):
        scene = self.mainWindow.gfxPanel.scene()
        selectedItems = scene.selectedItems()                          
        # create a delete command
        deleteCommand = DeleteCommand(self.mainWindow.shaderLink, 
                                      self.mainWindow.gfxPanel,
                                      selectedItems)
        self.commandProcessor.executeCommand(deleteCommand)

    def onViewAll(self):
        fitInViewCommand = FitInViewCommand(self.mainWindow.gfxPanel)
        self.commandProcessor.executeCommand(fitInViewCommand)     
        
    def onCommandExecuted(self):
        disableUndo = self.commandProcessor.doneCommandsStack == []
        self.mainWindow.undoAction.setDisabled(disableUndo)

        disableRedo = self.commandProcessor.unDoneCommandsStack == []
        self.mainWindow.redoAction.setDisabled(disableRedo)
        
    def onDirtyStateChanged(self, dirtyState):
        self.mainWindow.shaderLink.dirtyState = dirtyState
        
    def onSelectionChanged(self):        
        gfxNodes = []
        gfxLinks = []
        selectedItems = self.mainWindow.gfxPanel.scene().selectedItems()
        for selectedItem in selectedItems:
            from gfx.view import GfxNode, GfxLink
            if isinstance(selectedItem, GfxNode):
                gfxNodes.append(selectedItem)
            if isinstance(selectedItem, GfxLink):
                gfxLinks.append(selectedItem)
        
        # enable copy, delete and hidePreview action
        self.mainWindow.copyAction.setDisabled(gfxNodes == [])
        self.mainWindow.previewAction.setDisabled(gfxNodes == [])
        self.mainWindow.hidePreviewAction.setDisabled(gfxNodes == [])
        self.mainWindow.deleteAction.setDisabled(gfxNodes == [] and gfxLinks == [])
        
    def onCopyCommandChanged(self, copyCommand):
        self.mainWindow.pasteAction.setDisabled(copyCommand == None)

    def onRenderingSettingsChanged(self, renderingSettings):
        # current index of selection in root shaders comboboxes
        shaderIndices = [renderingSettings['Surface'][1],
                         renderingSettings['Displacement'][1],
                         renderingSettings['Atmosphere'][1],
                         renderingSettings['Interior'][1],
                         renderingSettings['Exterior'][1],
                         renderingSettings['Imager'][1]]
        
        someShaderSelectedd = any(index > 0 for index in shaderIndices)
        
        # we can run a RenderCommand only if we selected some root shaders
        self.mainWindow.renderAction.setEnabled(someShaderSelectedd)
    
    def onRendererSettings(self):
        # renderer settings dialog
        from view import RendererSettings
        rendererSettingsDialog = RendererSettings(self.mainWindow.shaderLink, self.mainWindow.commandProcessor, self.mainWindow) 
         
        rendererSettingsDialog.exec_()
        
    def onNodeLoaded(self, node):
        from view import MessagePanel
        self.mainWindow.messagePanel.insertMessage(MessagePanel.InformationType, 'Loaded node %s.' % node.name)
      
    def onNodeAdded(self, node):
        for inputProp in node.inputProps:
            QtCore.QObject.connect(inputProp, QtCore.SIGNAL('propertyChanged()'), 
                                   self.onPropertyChanged)  
    
    def onPropertyChanged(self):
        self.updateGfxNodePreview()

    def updateGfxNodePreview(self):
        selectedItems = self.mainWindow.gfxPanel.scene().selectedItems()
        
        # filter gfx nodes
        from gfx.view import GfxNode
        gfxNodes = filter(lambda selectedItem: isinstance(selectedItem, GfxNode), selectedItems)        
        
        if len(gfxNodes) != 1:
            return

        if not gfxNodes[0].previewPixmapEnabled:
            return
        
        # TODO: refactor
        previewNodeCommand = PreviewNodeCommand(self.mainWindow.shaderLink, gfxNodes, 
                                                self.mainWindow)
        self.commandProcessor.executeCommand(previewNodeCommand)  
   
    def onRender(self):
        # create a render command
        renderCommand = RenderCommand(self.mainWindow.shaderLink, 
                                      self.mainWindow)
        self.commandProcessor.executeCommand(renderCommand)
        
    def onCodeEditor(self):
        codeEditorDialog = self.mainWindow.codeEditorDialog
        codeEditorDialog.setNodes(self.mainWindow.shaderLink.nodes)
        self.mainWindow.codeEditorDialog.exec_()

    def onCodeGenerator(self):
        codeGeneratorDialog = self.mainWindow.codeGeneratorDialog
        codeGeneratorDialog.setNodes(self.mainWindow.shaderLink.nodes)
        codeGeneratorDialog.exec_()
        
    def onCloseEvent(self, event):
        if self.okToContinue():
            self.mainWindow.saveSettings()
        else:
            event.ignore()

    def onHidePreview(self):
        selectedItems = self.mainWindow.gfxPanel.scene().selectedItems()
        
        # filter gfx nodes
        from gfx.view import GfxNode
        gfxNodes = filter(lambda selectedItem: isinstance(selectedItem, GfxNode), selectedItems)
        
        # create hide preview command
        hidePreviewCommand = HidePreviewCommand(gfxNodes)
        self.commandProcessor.executeCommand(hidePreviewCommand)

    def onPreview(self):
        selectedItems = self.mainWindow.gfxPanel.scene().selectedItems()
        
        # filter gfx nodes
        from gfx.view import GfxNode
        gfxNodes = filter(lambda selectedItem: isinstance(selectedItem, GfxNode), selectedItems)

        # create preview node command
        previewNodeCommand = PreviewNodeCommand(self.mainWindow.shaderLink, gfxNodes, 
                                                self.mainWindow)
        self.commandProcessor.executeCommand(previewNodeCommand)
            
    def onAbout(self):        
        from view import AboutDialog
        aboutDialog = AboutDialog(self.mainWindow)
        aboutDialog.exec_() 
                            
class NodeLibraryViewerController(object):
    def __init__(self, nodeLibraryViewer, shaderLink, commandProcessor):
        self.nodeLibraryViewer = nodeLibraryViewer
        self.shaderLink = shaderLink
        self.commandProcessor = commandProcessor

    def onNodeLibraryLoaded(self, nodeLibrary):
        self.nodeLibrary = nodeLibrary
        
        # load tree items 
        # nodeLibrary[dir][nodeName] = node        
        for dirName, nodes in self.nodeLibrary.iteritems():
            # build top level tree item
            from view import NodeTreeWidgetItem
            dirItem = NodeTreeWidgetItem(self.nodeLibraryViewer.tree, 
                                         dirName, 
                                         None)
            
            # set bold font
            font = dirItem.font(0)
            font.setBold(True)
            dirItem.setFont(0, font)
            
            for nodeName, node in nodes.iteritems():
                print 'Creating preview: ', dirName, nodeName
                                                
                # build tree node item
                from view import NodeTreeWidget
                nodeItem = NodeTreeWidgetItem(dirItem, nodeName, node.gfxNode.pixmap)
    
    def onItemSelectionChanged(self):
        itemsSelected = self.nodeLibraryViewer.tree.selectedItems()
        item = itemsSelected[0]
        
        # check parent name and return if top level node
        if item.parent() == None:
            self.nodeLibraryViewer.authorEdit.clear()
            self.nodeLibraryViewer.helpEdit.clear()
#            self.nodeLibraryViewer.imageLabel.clear()            
            return

        # get dir name
        dirName = unicode(item.parent().text(0))
        
        # get node from library
        nodeName = unicode(item.text(0))
              
        # get node information
        node = self.nodeLibrary[dirName][nodeName]
        self.nodeLibraryViewer.authorEdit.setText(node.author)
        self.nodeLibraryViewer.authorEdit.setCursorPosition(0)
        self.nodeLibraryViewer.helpEdit.setText(node.help)
        
#        # get node pixmap for preview
#        self.nodeLibraryViewer.imageLabel.setPixmap(node.gfxNode.scaledPixmap)
        
class RenderingPanelController(QtCore.QObject):
    def __init__(self, renderingPanel, commandProcessor):
        QtCore.QObject.__init__(self)
        
        self.renderingPanel = renderingPanel
        self.commandProcessor = commandProcessor
        
        # map shader type to combo box
        self.shaderType2CB = {'surface' : self.renderingPanel.surfaceCB,
                              'displacement' : self.renderingPanel.displacementCB,
                              'atmosphere' : self.renderingPanel.atmosphereCB,
                              'interior' : self.renderingPanel.interiorCB,
                              'exterior' : self.renderingPanel.exteriorCB,
                              'imager' : self.renderingPanel.imagerCB}
        
    def setComboBox(self, combo, value):
        items = value[0]
        currentIndex = value[1] 
        combo.clear()
        combo.addItems(items)
        combo.setCurrentIndex(currentIndex)
                
    def setValueOnComboBox(self, combo, value):
        index = combo.findText(value)
        if index == -1: 
            combo.setCurrentIndex(0)
        else:
            combo.setCurrentIndex(index)        
        
    def onRenderingSettingsLoaded(self, renderingSettigs):
        # disconnect signals
        self.renderingPanel.disconnectSignals()        
        
        # reload ribCB
        self.renderingPanel.buildRibCB(self.renderingPanel.ribCB)
                        
        # rib
        rib = renderingSettigs['Rib']
        self.setValueOnComboBox(self.renderingPanel.ribCB, rib)
        
        # format
        format = renderingSettigs['Format']
        self.renderingPanel.formatWidthSB.setValue(format[0])
        self.renderingPanel.formatHeightSB.setValue(format[1])
        
        # aspect ratio
        aspectRatio = renderingSettigs['AspectRatio']
        self.renderingPanel.aspectRatioEdit.setText(str(aspectRatio))
        
        # samples
        samples = renderingSettigs['Samples']
        self.renderingPanel.samplesXSB.setValue(samples[0])
        self.renderingPanel.samplesYSB.setValue(samples[1])
        
        # filter
        filter = renderingSettigs['Filter']
        self.setValueOnComboBox(self.renderingPanel.filterCB, filter)
        
        # filter width
        filterWidth = renderingSettigs['FilterWidth']
        self.renderingPanel.filterWidthXSB.setValue(filterWidth[0])
        self.renderingPanel.filterWidthYSB.setValue(filterWidth[1])
        
        # shading rate
        shadingRate = renderingSettigs['ShadingRate']
        self.renderingPanel.shadingRateEdit.setText(str(shadingRate))
        
        # surface
        surface = renderingSettigs['Surface']
        self.setComboBox(self.renderingPanel.surfaceCB, surface)

        # displacement
        displacement = renderingSettigs['Displacement']
        self.setComboBox(self.renderingPanel.displacementCB, displacement)

        # atmosphere
        atmosphere = renderingSettigs['Atmosphere']
        self.setComboBox(self.renderingPanel.atmosphereCB, atmosphere)
        
        # interior
        interior = renderingSettigs['Interior']
        self.setComboBox(self.renderingPanel.interiorCB, interior)
        
        # exterior
        exterior = renderingSettigs['Exterior']
        self.setComboBox(self.renderingPanel.exteriorCB, exterior)

        # imager
        imager = renderingSettigs['Imager']
        self.setComboBox(self.renderingPanel.imagerCB, imager)
                                
        # connect signals
        self.renderingPanel.connectSignals()
        
        # preview (this is set when everything is connected)
        preview = renderingSettigs['Preview']
        self.renderingPanel.previewCB.setChecked(preview)
        
        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)

    def onPreviewStateChanged(self, state):
        checked = False
        if state == QtCore.Qt.Checked:
            checked = True

        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Preview', checked)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
             
    def onRibCurrentIndexChanged(self, index):
        value = str(self.renderingPanel.ribCB.itemText(index))
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Rib', value)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)
        
        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
    
    def onAspectRatioEditingFinished(self):
        value = self.renderingPanel.aspectRatioEdit.text()
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'AspectRatio', 
                                                                    float(value))
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
     
    def onFormatWidthValueChanged(self, value):
        format = self.renderingPanel.shaderLink.renderingSettings['Format']
        newFormat = (int(value), format[1])
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Format', newFormat)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
 
    def onFormatHeightValueChanged(self, value):
        format = self.renderingPanel.shaderLink.renderingSettings['Format']
        newFormat = (format[0], int(value))
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Format', newFormat)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
 
    def onSamplesXValueChanged(self, value):
        samples = self.renderingPanel.shaderLink.renderingSettings['Samples']
        newSamples = (int(value), samples[1])
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Samples', newSamples)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
 
    def onSamplesYValueChanged(self, value):
        samples = self.renderingPanel.shaderLink.renderingSettings['Samples']
        newSamples = (samples[0], int(value))
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Samples', newSamples)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
 
    def onFilterCurrentIndexChanged(self, index):
        value = self.renderingPanel.filterCB.itemText(index)
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Filter', value)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
 
    def onFilterWidthXValueChanged(self, value):
        filterWidth = self.renderingPanel.shaderLink.renderingSettings['FilterWidth']
        newFilterWidth = (int(value), filterWidth[1])
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'FilterWidth', 
                                                                    newFilterWidth)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
 
    def onFilterWidthYValueChanged(self, value):
        filterWidth = self.renderingPanel.shaderLink.renderingSettings['FilterWidth']
        newFilterWidth = (filterWidth[0], int(value))
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'FilterWidth', 
                                                                    newFilterWidth)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
 
    def onShadingRateEditingFinished(self):
        value = self.renderingPanel.shadingRateEdit.text()
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'ShadingRate', 
                                                                    float(value))
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)

    def onSurfaceCurrentIndexChanged(self, index):
        items = self.getComboBoxItems(self.renderingPanel.surfaceCB)
        
        value = [items, index]
        
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Surface', value)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
 
    def onDisplacementCurrentIndexChanged(self, index):
        items = self.getComboBoxItems(self.renderingPanel.displacementCB)
                
        value = [items, index]

        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Displacement', value)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
 
    def onAtmosphereCurrentIndexChanged(self, index):
        items = self.getComboBoxItems(self.renderingPanel.atmosphereCB)
        
        value = [items, index]
        
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Atmosphere', value)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
 
    def onInteriorCurrentIndexChanged(self, index):
        items = self.getComboBoxItems(self.renderingPanel.interiorCB)
        
        value = [items, index]
        
        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Interior', value)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
 
    def onExteriorCurrentIndexChanged(self, index):
        items = self.getComboBoxItems(self.renderingPanel.exteriorCB)        
        
        value = [items, index]

        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Exterior', value)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)

    def onImagerCurrentIndexChanged(self, index):
        items = self.getComboBoxItems(self.renderingPanel.imagerCB)

        value = [items, index]

        editRenderingSettingsCommand = EditRenderingSettingsCommand(self.renderingPanel.shaderLink, 'Imager', value)
        self.commandProcessor.executeCommand(editRenderingSettingsCommand)

        self.emit(QtCore.SIGNAL('renderingSettingsChanged'),
                  self.renderingPanel.shaderLink.renderingSettings)
        
    def getComboBoxItems(self, comboBox):
        items = []
        for i in range(comboBox.count()):
            items.append(comboBox.itemText(i))

        return items

    def onNodeAdded(self, node):
        if node.type != '': 
            shaderComboBox = self.shaderType2CB[node.type]
            shaderComboBox.addItem(node.name)
        
    def onNodeRemoved(self, node):
        if node.type != '':
            shaderComboBox = self.shaderType2CB[node.type]
            items = self.getComboBoxItems(shaderComboBox)
            index = items.index(node.name) 
            shaderComboBox.removeItem(index)

class SLHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, textDocument):
        QtGui.QSyntaxHighlighter.__init__(self, textDocument)
        
        self.highlightingRules = []
        
        self.initialize()

    def initialize(self):        
        # types
        self.typeFormat = QtGui.QTextCharFormat()
        self.typeFormat.setForeground(QtCore.Qt.darkBlue)
        self.typeFormat.setFontWeight(QtGui.QFont.Bold)
        
        typePatterns = ['\\bfloat\\b', '\\bcolor\\b', '\\bmatrix\\b', '\\bvector\\b', '\\bstring\\b',
                        '\\bpoint\\b', '\\bnormal\\b']
        
        for typePattern in typePatterns:
            typeRule = (QtCore.QRegExp(typePattern), self.typeFormat)
            self.highlightingRules.append(typeRule)
        
        # single line comment
        self.singleLineCommentFormat = QtGui.QTextCharFormat()
        self.singleLineCommentFormat.setForeground(QtCore.Qt.red)
        singleLineCommentRule = (QtCore.QRegExp('//[^\n]*'), self.singleLineCommentFormat) 
        self.highlightingRules.append(singleLineCommentRule)

        # multiline comment
        self.multiLineCommentFormat = QtGui.QTextCharFormat() 
        self.multiLineCommentFormat.setForeground(QtCore.Qt.red)
        self.commentStartExpression = QtCore.QRegExp("/\\*");
        self.commentEndExpression = QtCore.QRegExp("\\*/");
        
        # string
        self.stringFormat = QtGui.QTextCharFormat()
        self.stringFormat.setForeground(QtCore.Qt.darkGreen)
        stringRule = (QtCore.QRegExp('\".*\"'), self.stringFormat) 
        self.highlightingRules.append(stringRule)

        # function
        self.functionFormat = QtGui.QTextCharFormat()
        self.functionFormat.setForeground(QtCore.Qt.blue)
        functionRule = (QtCore.QRegExp('\\b[A-Za-z0-9_]+(?=\\()'), self.functionFormat) 
        self.highlightingRules.append(functionRule)
        
    def highlightBlock(self, text):        
        # apply rules
        for rule in self.highlightingRules:
            expression = QtCore.QRegExp(rule[0])
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule[1])
                index = expression.indexIn(text, index + length)
                
        self.setCurrentBlockState(0)

        # multiline comment handling 
        startIndex = 0;
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)
            commentLength = 0
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = text.length() - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength, self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                                      startIndex + commentLength)
		
class TabWidgetFilter(QtCore.QObject):
    def __init__(self, tabWidget):
        QtCore.QObject.__init__(self, None)
        self.tabWidget = tabWidget            
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            # hack to understand mouse press on tab page
            tabBar = self.tabWidget.tabBar()
            index = tabBar.tabAt(event.pos())
    
            if index != -1:
                if event.button() == QtCore.Qt.MidButton:
                    self.tabWidget.emit(QtCore.SIGNAL('tabCloseRequested'), index)
                    return True                        
        elif event.type() == QtCore.QEvent.KeyPress:
            index  = self.tabWidget.currentIndex()
            if index != -1:            
                if event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_S:
                     self.tabWidget.emit(QtCore.SIGNAL('saveRequested'))
                     return True
            
        return obj.eventFilter(obj, event)

class CodeEditorDialogController(QtCore.QObject):
    def __init__(self, codeEditorDialog, commandProcessor):
        QtCore.QObject.__init__(self)
        self.codeEditorDialog = codeEditorDialog
        self.commandProcessor = commandProcessor
        
        self.tabWidgetFilter = TabWidgetFilter(self.codeEditorDialog.tabWidget)
    
    def populateNodeLW(self):
        for node in self.codeEditorDialog.nodes.values():
             self.codeEditorDialog.nodesLW.addItem(node.name) 

    def populateEditors(self):
        for node in self.codeEditorDialog.nodes.values():
             editor = QtGui.QTextEdit()
             # add code to editor
             editor.setText(node.code)
             
             editor.setLineWrapMode(QtGui.QTextEdit.NoWrap)
             
             # add syntax highlighting
             highlighter = SLHighlighter(editor.document())
             self.codeEditorDialog.editors[node.name] = editor
    
    def onSetNodes(self, nodes):
        # editors
        self.codeEditorDialog.editors = {}
        
        # set nodes
        self.codeEditorDialog.nodes = nodes  
        
        # clear list view
        self.codeEditorDialog.nodesLW.clear()
        
        # clear tabs
        self.codeEditorDialog.tabWidget.clear()
        
        # populate node list
        self.populateNodeLW()
        
        # populate editors
        self.populateEditors()
                
    def onNodesLWItemDoubleClicked(self, item):
        # get node name
        nodeName = str(item.text())
        
        # get the editor
        editor = self.codeEditorDialog.editors[nodeName]
        
        index = self.codeEditorDialog.tabWidget.indexOf(editor) 
        if  index == -1:
            # add it to tab widget
            self.codeEditorDialog.tabWidget.addTab(editor, nodeName)
            # select the tab
            count = self.codeEditorDialog.tabWidget.count()
            self.codeEditorDialog.tabWidget.setCurrentIndex(count - 1)        
        else:
            # select the tab
            self.codeEditorDialog.tabWidget.setCurrentIndex(index)

    def okToContinue(self, index, cancelButton = False):
        editor = self.codeEditorDialog.tabWidget.widget(index)
        
        document = editor.document()
        
        # if editor was not modified
        if not document.isModified():
            return True
        else:
            # get tab name
            tabName = str(self.codeEditorDialog.tabWidget.tabText(index))
            
            # get rid of *
            nodeName = tabName.rstrip('*')
            buttons = None
            if cancelButton:
                buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel
            else:
                buttons = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
             
            reply = QtGui.QMessageBox.question(self.codeEditorDialog.tabWidget, 'Shaderlink - Unsaved changes',
                                               'Do you want to save code of node %s?' % nodeName,
                                               buttons)
            if (reply == QtGui.QMessageBox.Yes):
                # save node code
                code = str(editor.toPlainText())
                self.saveNodeCode(nodeName, code)
                return True
            elif (reply == QtGui.QMessageBox.No):
                return True
            else:
                return False

    def closeAllEditors(self):
        for index in range(self.codeEditorDialog.tabWidget.count()):
            self.okToContinue(index)
            
    def onTabCloseRequested(self, index):
        if self.okToContinue(index, True):
            # remove tab
            self.codeEditorDialog.tabWidget.removeTab(index)
        
    def onEditorTextChanged(self):
        editor = self.sender()
        
        index = self.codeEditorDialog.tabWidget.indexOf(editor)
        if index == -1:
            return
         
        tabName = str(self.codeEditorDialog.tabWidget.tabText(index))
        if tabName.endswith('*'):
            return
        
        self.codeEditorDialog.tabWidget.setTabText(index, tabName + '*')
        
    def onSaveRequested(self):        
        editor = self.codeEditorDialog.tabWidget.currentWidget()
        document = editor.document()
        
        # if editor was not modified no need to save code
        if not document.isModified():
            return
        
        # OK, editor modified, reset in order to get new notifications
        document.setModified(False)
        
        # get tab index
        index = self.codeEditorDialog.tabWidget.currentIndex()         
        
        # get tab name
        tabName = str(self.codeEditorDialog.tabWidget.tabText(index))
        
        # get rid of *
        nodeName = tabName.rstrip('*')
        
        # update tab name text
        self.codeEditorDialog.tabWidget.setTabText(index, 
                                             nodeName)
        
        # save node code
        code = str(editor.toPlainText())
        self.saveNodeCode(nodeName, code)
        
    def saveNodeCode(self, nodeName, code):        
        for node in self.codeEditorDialog.nodes.values():
            if node.name == nodeName:
                editNodeCodeCommand = EditNodeCodeCommand(node, code)
                self.commandProcessor.executeCommand(editNodeCodeCommand)
                break 

class CodeGeneratorDialogController(QtCore.QObject):
    def __init__(self, codeGeneratorDialog, shaderLink, commandProcessor):
        QtCore.QObject.__init__(self)
        
        self.nodes = None                
        
        self.codeGeneratorDialog = codeGeneratorDialog
        
        self.shaderLink = shaderLink
        
        self.commandProcessor = commandProcessor
        
        self.nodeParams = {}
        
        self.currentParams = {}
        
    def onSetNodes(self, nodes):
        self.nodes = nodes
                                        
        # clear widget
        self.codeGeneratorDialog.shadersLW.clear()
        self.codeGeneratorDialog.parametersTW.clear()
        self.codeGeneratorDialog.codeEdit.clear()
        self.nodeParams = {}
        self.currentParams = {}        
        
        # loop on root nodes and collect shader parameters
        for node in self.nodes.values():
            if node.type != '':
                params = []
                node.getAvailableShaderParameters(params)
                self.nodeParams[node.name] = params
                
        # populate shadersLW
        for nodeName in self.nodeParams.keys():
            self.codeGeneratorDialog.shadersLW.addItem(nodeName) 
            
    def onShadersLWCurrentRowChanged(self, index):                
        if index == -1:
            return
        
        # clear list widget
        self.currentParams = {}        
        self.codeGeneratorDialog.parametersTW.clear()
        
        item = self.codeGeneratorDialog.shadersLW.item(index)
        
        # get node name
        nodeName = str(item.text())
        
        # get parameters
        params = self.nodeParams[nodeName]
        
        # disconnect signals
        self.codeGeneratorDialog.disconnectSignals()
        
        # fill tree widget parameters
        for param in params:
            node = param['node']
            property = param['property']
            
            self.currentParams[node.name + '_' + property.name] = param
            
            item = QtGui.QTreeWidgetItem(None)
            
            item.setText(0,  node.name + '_' + property.name)
            item.setText(1, property.valueToStr())
            
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            
            if property.isShaderParameter:
                item.setCheckState(0, QtCore.Qt.Checked)
            else:
                item.setCheckState(0, QtCore.Qt.Unchecked)
            
            self.codeGeneratorDialog.parametersTW.addTopLevelItem(item)
        
        # connect signals
        self.codeGeneratorDialog.connectSignals()
        
        # build code
        self.buildCode()                  
        
    def onParametersTWItemChanged(self, item, column):
        paramName = str(item.text(column))
        
        # get property
        property = self.currentParams[paramName]['property']
        
        # get value
        value = False
        if item.checkState(column) == QtCore.Qt.Checked:
            value = True
        
        # create command
        editPropertyShaderParameterCommand = EditPropertyShaderParameterCommand(property, value)
        self.commandProcessor.executeCommand(editPropertyShaderParameterCommand)
        
        # build code
        self.buildCode()                
        
    def buildCode(self):
        index = self.codeGeneratorDialog.shadersLW.currentRow()
        
        if index == -1:
            return
        
        # get current selected root node
        nodeName = str(self.codeGeneratorDialog.shadersLW.currentItem().text())
        
        rootNode = None
        for node in self.nodes.values():
            if node.type != '' and node.name == nodeName:
                rootNode = node
                break
        
        # create shader builder        
        from core.generator import ShaderBuilder
        shaderBuilder = ShaderBuilder(self.shaderLink, [rootNode], None)
        
        # build shaders
        shaderBuilder.buildShaders()
        
        # read code
        path = shaderBuilder.shaders.values()[0]['path']
        f = open(path, 'r')
        code = f.read()
        f.close()
        
        # add code to editor
        self.codeGeneratorDialog.codeEdit.setText(code)
                 
    def onExport(self):
        formats = ['*.sl']
        fileName = unicode(QtGui.QFileDialog.getSaveFileName(self.codeGeneratorDialog,
                                                             'Shaderlink - Export shader', '.',
                                                             'Renderman Shading Language files (%s)' % ' '.join(formats)))
        if not fileName:
            return 
        
        f = open(fileName, 'w')
        code = f.write(str(self.codeGeneratorDialog.codeEdit.toPlainText()))
        f.close()
      
class RendererSettingsController(QtCore.QObject):
    def __init__(self, rendererSettings, shaderLink, commandProcessor):
        QtCore.QObject.__init__(self)
        
        self.nodes = None                
        
        self.rendererSettings = rendererSettings
        
        self.shaderLink = shaderLink
        
        self.commandProcessor = commandProcessor
                
    def onCurrentIndexChanged(self, index):
        self.rendererSettings.compilerPathLE.setText(self.shaderLink.renderers[index]['compileTool'])
        self.rendererSettings.rendererPathLE.setText(self.shaderLink.renderers[index]['renderTool'])
    
    def onOKPressed(self):
        # get value
        rendererIndex = self.rendererSettings.rendererCombo.currentIndex()
        
        # create command
        rendererSettingsCommand = RendererSettingsCommand(self.shaderLink, rendererIndex)
        self.commandProcessor.executeCommand(rendererSettingsCommand)
                
