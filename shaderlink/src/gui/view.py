##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

from PyQt4 import QtGui, QtCore

class  NodeTreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent = None):
        QtGui.QTreeWidget.__init__(self, parent)
        
        self.setMinimumHeight(250)
        
    def startDrag(self, dropActions):
        item = self.currentItem()
        
        # check parent name and return if top level node
        if item.parent() == None:
            return
        
        # get dir name
        dirName = unicode(item.parent().text(0))
        
        # get node from library
        nodeName = unicode(item.text(0))
        
        # set custom data
        data = QtCore.QByteArray()
        stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
        stream << item.parent().text(0) << item.text(0) 
        mimeData = QtCore.QMimeData()
        mimeData.setData('application/x-text', data)
        
        # set drag
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(QtGui.QPixmap(':/node.png'))
        drag.start(QtCore.Qt.CopyAction)
       
class  NodeTreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent, name, pixmap):
        QtGui.QTreeWidgetItem.__init__(self, parent, [name])
        
        self.pixmap = pixmap

from controller import NodeLibraryViewerController
            
class NodeLibraryViewer(QtGui.QWidget):
    def __init__(self, shaderLink, commandProcessor, parent = None):
        QtGui.QWidget.__init__(self, parent) 

        # build gui
        self.buildGui()
        
        # controller
        self.controller = NodeLibraryViewerController(self, 
                                                      shaderLink,
                                                      commandProcessor)
        self.connect(self.tree, QtCore.SIGNAL('itemSelectionChanged()'), 
                     self.controller.onItemSelectionChanged)   
                
    def buildGui(self):        
        self.setMinimumSize(240, 50)
        self.setMaximumSize(240, 5000)
        
        # tree
        self.tree = NodeTreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setDragEnabled(True)
        self.tree.setHeaderLabel('Available nodes') 

        # node information groupbox
        groupBox = QtGui.QGroupBox('Node information', self)
        layoutGroupBox = QtGui.QGridLayout(groupBox)
        groupBox.setLayout(layoutGroupBox)

#        # node image label
#        self.imageLabel = QtGui.QLabel(groupBox)
#        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
#        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored, 
#                                      QtGui.QSizePolicy.Expanding)
#        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        

        # author label
        self.authorLabel = QtGui.QLabel('Author', groupBox)
        self.authorEdit = QtGui.QLineEdit(groupBox)
        self.authorEdit.setReadOnly(True) 

        # help label
        self.helpLabel = QtGui.QLabel('Help', groupBox)
        self.helpEdit = QtGui.QTextEdit(groupBox)        
        self.helpEdit.setSizePolicy(QtGui.QSizePolicy.Ignored, 
                                    QtGui.QSizePolicy.Expanding)
        self.helpEdit.setReadOnly(True)

#        # preview label
#        self.previewLabel = QtGui.QLabel('Preview', groupBox)
        
        # node information layout        
        layoutGroupBox.addWidget(self.authorLabel, 0, 0)
        layoutGroupBox.addWidget(self.authorEdit, 1, 0)
        layoutGroupBox.addWidget(self.helpLabel,2, 0)
        layoutGroupBox.addWidget(self.helpEdit,3, 0)
#        layoutGroupBox.addWidget(self.previewLabel, 4, 0)
#        layoutGroupBox.addWidget(self.imageLabel, 5, 0)

        # main layout
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.tree, 3)
        vbox.addWidget(groupBox, 1)
                                     
class NodePropertyViewer(QtGui.QWidget):
    def __init__(self, scene, commandProcessor, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        self.scene = scene
        self.commandProcessor = commandProcessor

        # set up property -> modifier
        import core        
        import modifier.view        
        self.modifiers = {core.model.ColorProperty : modifier.view.ColorPropertyModifier,
                          core.model.FloatProperty : modifier.view.FloatPropertyModifier,
                          core.model.MatrixProperty : modifier.view.MatrixPropertyModifier,
                          core.model.PointProperty : modifier.view.Tuple3DPropertyModifier,
                          core.model.VectorProperty : modifier.view.Tuple3DPropertyModifier,
                          core.model.NormalProperty : modifier.view.Tuple3DPropertyModifier,
                          core.model.StringProperty : modifier.view.StringPropertyModifier}
        
        # build the gui
        self.buildGui()
        
    def buildGui(self):
        self.setMinimumSize(280, 200)
        
        self.stackedWidget = QtGui.QStackedWidget(self)
        frame = QtGui.QFrame()
        self.stackedWidget.addWidget(frame)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.stackedWidget)
        
        self.setLayout(mainLayout)

    def updateGui(self, node):
        # remove the current widget
        currentWidget = self.stackedWidget.currentWidget()
        self.stackedWidget.removeWidget(currentWidget)
        
        frame = QtGui.QFrame()
        frameLayout = QtGui.QVBoxLayout()
        frame.setLayout(frameLayout)
        
        if node:
            # build the modifier for the property
            # the property must not be linked
            for inputProp in node.inputProps:
                if not node.isInputPropertyLinked(inputProp):
                    modifier = apply(self.modifiers[type(inputProp)], [inputProp, self.commandProcessor, self])
                    frameLayout.addWidget(modifier)
        
        # build a scroll area
        scrollArea = QtGui.QScrollArea()        
        scrollArea.setWidget(frame)
        
        self.stackedWidget.addWidget(scrollArea)
        
    def onSelectionChanged(self):               
        # collected all selected items
        gfxNodes = []
        selectedItems = self.scene.selectedItems()
        for selectedItem in selectedItems:
            from gfx.view import GfxNode
            if isinstance(selectedItem, GfxNode):
                gfxNodes.append(selectedItem)
        
        # check if a single node is selected        
        if len(gfxNodes) == 1:
            self.updateGui(gfxNodes[0].node)
        else:
            self.updateGui(None)
            
class  MessageTreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent = None):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        # context menu
        self.menu = QtGui.QMenu(self)
        
        # menu action
        self.copyAction = self.menu.addAction('Copy')
        self.connect(self.copyAction, QtCore.SIGNAL('triggered()'), self.onCopy) 
        self.clearAction = self.menu.addAction('Clear all')
        self.connect(self.clearAction, QtCore.SIGNAL('triggered()'), self.onClearAll) 
        
    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        
        if item:                     
            item.setSelected(True)
            self.menu.exec_(event.globalPos())

    def onCopy(self):        
        item = self.currentItem()
        clipboard = QtGui.QApplication.clipboard()
        # copy message
        clipboard.setText(item.text(2))

    def onClearAll(self):
        self.clear()

class MessagePanel(QtGui.QWidget):
    ErrorType = 0
    InformationType = 1
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        # build the gui
        self.buildGui()
        
    def buildGui(self):
        # table
        self.tree = MessageTreeWidget(self)
        headerStr = ['', 'Type', 'Message']
        self.tree.setColumnCount(len(headerStr))
        self.tree.setHeaderLabels(headerStr)
        
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.tree)
        
        self.tree.setSortingEnabled(False)

    def insertMessage(self, type, msg):        
        # position where insert
        rowToInsert = self.tree.topLevelItemCount()
        
        # build right row
        newItem = None
        if type == MessagePanel.ErrorType:
            newItem = QtGui.QTreeWidgetItem([str(rowToInsert + 1), 'Error', msg])
            newItem.setIcon(0, QtGui.QIcon(':/error.png'))
        else:
            newItem = QtGui.QTreeWidgetItem([str(rowToInsert + 1), 'Info', msg])
            newItem.setIcon(0, QtGui.QIcon(':/information.png'))
            
        # insert into tree
        self.tree.insertTopLevelItem(0, newItem)

class ConsoleEdit(QtGui.QTextEdit):
    def __init__(self, parent = None):
        QtGui.QTextEdit.__init__(self, parent)
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu(event.pos())
        clearAction = menu.addAction('Clear')
        self.connect(clearAction, QtCore.SIGNAL('triggered()'), self.clear)         
        menu.exec_(event.globalPos())

class ConsolePanel(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)        
        
        # build the gui
        self.buildGui()
        
    def buildGui(self):
        self.textEdit = ConsoleEdit(self)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
                
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.textEdit)
    
    def insertNormalText(self, s):
        self.textEdit.setFontWeight(QtGui.QFont.Normal)
        self.textEdit.append(s)

    def insertBoldText(self, s):        
        self.textEdit.setFontWeight(QtGui.QFont.Bold)
        self.textEdit.append(s)
    
    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu(event.pos())
        clearAction = menu.addAction('Clear')
        self.connect(clearAction, QtCore.SIGNAL('triggered()'), self.clear())         
        menu.exec_(event.globalPos())

import ui_RenderingPanel
class RenderingPanel(QtGui.QWidget,
                     ui_RenderingPanel.Ui_RenderingPanel):
        def __init__(self, shaderLink, commandProcessor, parent = None):
            QtGui.QWidget.__init__(self, parent)
            
            self.shaderLink = shaderLink
            self.commandProcessor = commandProcessor       
            
            # build the gui
            self.buildGui()
        
        def setupEdit(self, edit, min, max):
            validator = QtGui.QDoubleValidator(min, max, 3, self) 
            edit.setValidator(validator)

        def setupSpinBox(self, spinBox, min, max):
            spinBox.setMinimum(min)
            spinBox.setMaximum(max)

        def buildRibCB(self, ribCB):            
            # clear old data
            self.ribCB.clear()
            
            # node library path
            import os
            pathRib = self.shaderLink.paths['rib']
            for (thisDir, subsHere, filesHere) in os.walk(pathRib):
                for filename in filesHere:
                    if filename.endswith('.rib'):
                        self.ribCB.addItem(filename)
            
        def buildGui(self):
            # build the gui created with QtDesigner
            self.setupUi(self)
            
            # build controller
            from controller import RenderingPanelController
            self.controller = RenderingPanelController(self, self.commandProcessor)
            
            # set up combo boxes
            #rib templates
            #self.buildRibCB(self.ribCB)

            # this is OK, always use these filters
            self.filterCB.addItem('box')
            self.filterCB.addItem('triangle')
            self.filterCB.addItem('catmull-rom')
            self.filterCB.addItem('sinc')
            self.filterCB.addItem('gaussian')
            
            # set up edits
            self.setupEdit(self.aspectRatioEdit, 0.1, 10.0)
            self.setupEdit(self.shadingRateEdit, 0.1, 3.0)
            
            # set up spin boxes
            self.setupSpinBox(self.formatWidthSB, 1, 10000)
            self.setupSpinBox(self.formatHeightSB, 1, 10000)
            self.setupSpinBox(self.samplesXSB, 1, 10)
            self.setupSpinBox(self.samplesYSB, 1, 10)
            self.setupSpinBox(self.filterWidthXSB, 1, 10)
            self.setupSpinBox(self.filterWidthYSB, 1, 10)
            
            # connect signals
            self.connectSignals()
        
        def connectSignals(self):
            self.connect(self.previewCB, QtCore.SIGNAL('stateChanged(int)'), 
                         self.controller.onPreviewStateChanged)
            self.connect(self.ribCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                         self.controller.onRibCurrentIndexChanged)
            self.connect(self.aspectRatioEdit, QtCore.SIGNAL('editingFinished()'), 
                         self.controller.onAspectRatioEditingFinished)
            self.connect(self.formatWidthSB, QtCore.SIGNAL('valueChanged(int)'), 
                         self.controller.onFormatWidthValueChanged)
            self.connect(self.formatHeightSB, QtCore.SIGNAL('valueChanged(int)'), 
                         self.controller.onFormatHeightValueChanged)
            self.connect(self.samplesXSB, QtCore.SIGNAL('valueChanged(int)'), 
                         self.controller.onSamplesXValueChanged)
            self.connect(self.samplesYSB, QtCore.SIGNAL('valueChanged(int)'), 
                         self.controller.onSamplesYValueChanged)
            self.connect(self.filterCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                         self.controller.onFilterCurrentIndexChanged)
            self.connect(self.filterWidthXSB, QtCore.SIGNAL('valueChanged(int)'), 
                         self.controller.onFilterWidthXValueChanged)
            self.connect(self.filterWidthYSB, QtCore.SIGNAL('valueChanged(int)'), 
                         self.controller.onFilterWidthYValueChanged)
            self.connect(self.shadingRateEdit, QtCore.SIGNAL('editingFinished()'), 
                         self.controller.onShadingRateEditingFinished)
            
            self.connect(self.surfaceCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                         self.controller.onSurfaceCurrentIndexChanged)
            self.connect(self.displacementCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                         self.controller.onDisplacementCurrentIndexChanged)
            self.connect(self.atmosphereCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                         self.controller.onAtmosphereCurrentIndexChanged)
            self.connect(self.interiorCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                         self.controller.onInteriorCurrentIndexChanged)
            self.connect(self.exteriorCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                         self.controller.onExteriorCurrentIndexChanged)
            self.connect(self.imagerCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                         self.controller.onImagerCurrentIndexChanged)

        def disconnectSignals(self):
            self.disconnect(self.previewCB, QtCore.SIGNAL('stateChanged(int)'), 
                            self.controller.onPreviewStateChanged)
            self.disconnect(self.ribCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                            self.controller.onRibCurrentIndexChanged)
            self.disconnect(self.aspectRatioEdit, QtCore.SIGNAL('editingFinished()'), 
                         self.controller.onAspectRatioEditingFinished)
            self.disconnect(self.formatWidthSB, QtCore.SIGNAL('valueChanged(int)'), 
                            self.controller.onFormatWidthValueChanged)
            self.disconnect(self.formatHeightSB, QtCore.SIGNAL('valueChanged(int)'), 
                            self.controller.onFormatHeightValueChanged)
            self.disconnect(self.samplesXSB, QtCore.SIGNAL('valueChanged(int)'), 
                            self.controller.onSamplesXValueChanged)
            self.disconnect(self.samplesYSB, QtCore.SIGNAL('valueChanged(int)'), 
                            self.controller.onSamplesYValueChanged)
            self.disconnect(self.filterCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                            self.controller.onFilterCurrentIndexChanged)
            self.disconnect(self.filterWidthXSB, QtCore.SIGNAL('valueChanged(int)'), 
                            self.controller.onFilterWidthXValueChanged)
            self.disconnect(self.filterWidthYSB, QtCore.SIGNAL('valueChanged(int)'), 
                            self.controller.onFilterWidthYValueChanged)
            self.disconnect(self.shadingRateEdit, QtCore.SIGNAL('editingFinished()'), 
                            self.controller.onShadingRateEditingFinished)
            
            self.disconnect(self.surfaceCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                            self.controller.onSurfaceCurrentIndexChanged)
            self.disconnect(self.displacementCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                            self.controller.onDisplacementCurrentIndexChanged)
            self.disconnect(self.atmosphereCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                            self.controller.onAtmosphereCurrentIndexChanged)
            self.disconnect(self.interiorCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                            self.controller.onInteriorCurrentIndexChanged)
            self.disconnect(self.exteriorCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                            self.controller.onExteriorCurrentIndexChanged)
            self.disconnect(self.imagerCB, QtCore.SIGNAL('currentIndexChanged(int)'), 
                            self.controller.onImagerCurrentIndexChanged)            

class RenderImageDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        
        self.buildGui()
    
    def buildGui(self):
        # image
        self.imageLabel = QtGui.QLabel(self)
        
        # layout
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.imageLabel)
        
        # title
        self.setWindowTitle('Render')
        
    def setPixmap(self, image):
        w = image.width()
        h = image.height()
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)
   
        self.imageLabel.setPixmap(image)

import ui_CodeEditor
class CodeEditorDialog(QtGui.QDialog,
                       ui_CodeEditor.Ui_CodeEditor):
    def __init__(self, commandProcessor, parent = None):
        QtGui.QDialog.__init__(self, parent)
        
        self.commandProcessor = commandProcessor    

        self.nodes = None
                
        # build the gui
        self.buildGui()
        
        # create a controller
        from controller import CodeEditorDialogController
        self.controller = CodeEditorDialogController(self, commandProcessor)
        
        # install filter
        self.tabWidget.installEventFilter(self.controller.tabWidgetFilter)
        
        # connect signals
        self.connectSignals()
    
    def buildGui(self):
        # build the gui created with QtDesigner
        self.setupUi(self)            
        
        self.splitter.setStretchFactor(0, 1) 
        self.splitter.setStretchFactor(1, 7)
        self.tabWidget.clear()
                
        # min size
        self.setMinimumSize(800, 600)

    def setNodes(self, nodes):
        self.controller.onSetNodes(nodes)
        
        for editor in self.editors.values():
            self.connect(editor, QtCore.SIGNAL('textChanged()'), 
                         self.controller.onEditorTextChanged)
        
    def closeEvent(self, event):
        self.closeAllEditors()
        event.accept()
        
    def closeAllEditors(self):
        self.controller.closeAllEditors()
        
    def connectSignals(self):
        self.connect(self.nodesLW, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'), 
                     self.controller.onNodesLWItemDoubleClicked)
        self.connect(self.tabWidget, QtCore.SIGNAL('tabCloseRequested'), 
                     self.controller.onTabCloseRequested)
        self.connect(self.tabWidget, QtCore.SIGNAL('saveRequested'), 
                     self.controller.onSaveRequested)  
                 
import ui_CodeGenerator
class CodeGeneratorDialog(QtGui.QDialog,
                          ui_CodeGenerator.Ui_CodeGenerator):
    def __init__(self, shaderLink, commandProcessor, parent = None):
        QtGui.QDialog.__init__(self, parent)        
        
        # create controller
        from controller import CodeGeneratorDialogController
        self.controller = CodeGeneratorDialogController(self, shaderLink, commandProcessor)
        
        # build the gui
        self.buildGui()
        
        # connect signals
        self.connectSignals()
        
    def buildGui(self):
        # build the gui created with QtDesigner
        self.setupUi(self)
        
        # wrap mode
        self.codeEdit.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        
        # min size
        self.setMinimumSize(800, 600)

        # set up splitter
        self.splitter.setStretchFactor(0, 1) 
        self.splitter.setStretchFactor(1, 3)
        
        headerStr = ['Parameter', 'Value']
        self.parametersTW.setColumnCount(len(headerStr))
        self.parametersTW.setHeaderLabels(headerStr)
        
        # add syntax highlighting
        self.codeEdit.setReadOnly(True)
        from controller import SLHighlighter
        #highlighter = SLHighlighter(self.codeEdit.document())

    def connectSignals(self):
        self.connect(self.shadersLW, QtCore.SIGNAL('currentRowChanged(int)'), 
                     self.controller.onShadersLWCurrentRowChanged)
        self.connect(self.parametersTW, QtCore.SIGNAL('itemChanged(QTreeWidgetItem*, int)'), 
                     self.controller.onParametersTWItemChanged)
        self.connect(self.exportB, QtCore.SIGNAL('clicked()'), 
                     self.controller.onExport)            

    def disconnectSignals(self):
        self.disconnect(self.shadersLW, QtCore.SIGNAL('currentRowChanged(int)'), 
                        self.controller.onShadersLWCurrentRowChanged)
        self.disconnect(self.parametersTW, QtCore.SIGNAL('itemChanged(QTreeWidgetItem*, int)'), 
                        self.controller.onParametersTWItemChanged)
        self.disconnect(self.exportB, QtCore.SIGNAL('clicked()'), 
                        self.controller.onExport)    

    def setNodes(self, nodes):
        self.controller.onSetNodes(nodes)
        
class AboutDialog(QtGui.QDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        
        self.buildGui()
    
    def buildGui(self):
        # image
        self.imageLabel = QtGui.QLabel(self)
        self.imageLabel.setPixmap(QtGui.QPixmap(':/logo.png'))
        self.imageLabel.setScaledContents(True)
        
        # edit
        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml(QtGui.QApplication.translate("About", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><span style=\" font-size:12pt; font-weight:600; font-style:italic;\">Shaderlink</span><span style=\" font-size:12pt;\"> </span><span style=\" font-size:11pt;\">v 0.5</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; font-style:italic;\"><span style=\" font-size:10pt; font-style:normal;\">A RenderMan shader authoring tool.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\">Developed by<span style=\" font-weight:600;\"> Libero Spagnolini</span>.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><span style=\" font-size:10pt;\">Logo by </span><span style=\" font-size:10pt; font-weight:600;\">Alberto Cerutti</span><span style=\" font-size:10pt;\">.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><span style=\" font-size:10pt;\">Thanxs to the guys who created Sler, ShaderMan, Rat and mental mill for the inspiration!</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        
        # layout
        vbox = QtGui.QVBoxLayout()
        self.setLayout(vbox)
        vbox.addWidget(self.imageLabel)
        vbox.addWidget(self.textEdit)
        
        # title
        self.setWindowTitle('About Shaderlink')

import ui_RendererSettings
class RendererSettings(QtGui.QDialog,
                       ui_RendererSettings.Ui_RendererSettings):
    def __init__(self, shaderlink, commandProcessor, parent = None):
        QtGui.QDialog.__init__(self, parent)
        
        self.shaderlink = shaderlink;
        self.commandProcessor = commandProcessor    

        # build the gui
        self.buildGui()
        
        # create a controller
        from controller import RendererSettingsController
        self.controller = RendererSettingsController(self, shaderlink, commandProcessor)
        
        # connect signals
        self.connectSignals()
    
    def buildGui(self):
        # build the gui created with QtDesigner
        self.setupUi(self)
        
        for renderer in self.shaderlink.renderers:
            self.rendererCombo.addItem(renderer['name'])   
        
        self.rendererCombo.setCurrentIndex(self.shaderlink.currentRendererIndex)
        
        self.compilerPathLE.setText(self.shaderlink.renderers[self.shaderlink.currentRendererIndex]['compileTool'])
        self.rendererPathLE.setText(self.shaderlink.renderers[self.shaderlink.currentRendererIndex]['renderTool'])
                
    def connectSignals(self):
        self.connect(self.rendererCombo, QtCore.SIGNAL('currentIndexChanged(int)'), 
                     self.controller.onCurrentIndexChanged)         
        self.connect(self, QtCore.SIGNAL('accepted()'), 
                     self.controller.onOKPressed)                     
