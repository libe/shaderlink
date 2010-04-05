##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

import sys

import resources.resources
    
from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
                        
        # model
        from core.model import ShaderLink
        self.shaderLink = ShaderLink()
        
        # command processor
        from command.processor import CommandProcessor
        self.commandProcessor = CommandProcessor()
        
        # gfxPanel
        from gfx.view import GfxPanel
        self.gfxPanel = GfxPanel(self.shaderLink, self.commandProcessor)                
        self.setCentralWidget(self.gfxPanel)
        
        # main window controller
        from controller import MainWindowController
        self.controller = MainWindowController(self)
                
        # node library view
        from view import NodeLibraryViewer
        self.nodeLibraryViewer = NodeLibraryViewer(self.shaderLink, self.commandProcessor, self)
        
        # node property viewer
        from view import NodePropertyViewer
        self.nodePropertyViewer = NodePropertyViewer(self.gfxPanel.scene(), self.commandProcessor, self)

        # message panel
        from view import MessagePanel
        self.messagePanel = MessagePanel(self)
        
        # console panel
        from view import ConsolePanel
        self.consolePanel = ConsolePanel(self)        
        
        # rendering panel
        from view import RenderingPanel
        self.renderingPanel = RenderingPanel(self.shaderLink, self.commandProcessor, self)
        
        # render image dialog
        from view import RenderImageDialog
        self.renderImageDialog = RenderImageDialog(self)

        # code editor dialog
        from view import CodeEditorDialog
        self.codeEditorDialog = CodeEditorDialog(self.commandProcessor, self)
 
        # code generator dialog
        from view import CodeGeneratorDialog
        self.codeGeneratorDialog = CodeGeneratorDialog(self.shaderLink, self.commandProcessor, self)
                         
        # initialize docks
        self.initilizeDocks()
        
        # create actions
        self.createActions()
        
        # create menus
        self.createMenus()
        
        # create toolbars
        self.createToolbars()
        
        # attach views to model
        self.attachViewsToModel()
        
        # filename
        self.setFileName('')
                
        # load settings
        self.loadSettings()
        
        # initialize model after everything is set up
        self.shaderLink.initialize()

    def loadSettings(self):
        settings = QtCore.QSettings()
        self.recentFiles = settings.value('RecentFiles').toStringList()
        self.updateFileMenu()
        
    def saveSettings(self):
        settings = QtCore.QSettings()
        recentFiles = QtCore.QVariant(self.recentFiles) if self.recentFiles else QtCore.QVariant()
        settings.setValue("RecentFiles", recentFiles)
                
    def updateFileMenu(self):
        self.fileMenu.clear()
        self.addActions(self.fileMenu, self.fileMenuActions[:-1])
        
        recentFiles = []
        for fname in self.recentFiles:
            if QtCore.QFile.exists(fname):
                recentFiles.append(fname)
        
        if recentFiles:
            self.fileMenu.addSeparator()
            for i, fname in enumerate(recentFiles):
                action = QtGui.QAction(QtGui.QIcon(':/recentFile.png'), 
                                       '&%d %s' % (i + 1, QtCore.QFileInfo(fname).fileName()), self)
                action.setData(QtCore.QVariant(fname))
                self.connect(action, QtCore.SIGNAL('triggered()'),
                             self.controller.onOpenRecentFile)
                self.fileMenu.addAction(action)
        
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileMenuActions[-1])

    def addRecentFile(self, fname):
        if fname is None:
            return
        
        if not self.recentFiles.contains(fname):
            self.recentFiles.prepend(QtCore.QString(fname))
        
        while self.recentFiles.count() > 9:
            self.recentFiles.takeLast()

    def initilizeDocks(self):                
        # rendering panel dock
        self.renderingPanelDock = QtGui.QDockWidget('Rendering', self)
        self.renderingPanelDock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        scrollAreaRP = QtGui.QScrollArea()
        scrollAreaRP.setWidget(self.renderingPanel)
        self.renderingPanelDock.setWidget(scrollAreaRP)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                           self.renderingPanelDock)
        self.renderingPanelDock.close()
        
        # node library dock
        self.nodeLibraryDock = QtGui.QDockWidget('Library', self)
        self.nodeLibraryDock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        scrollAreaNLV = QtGui.QScrollArea()
        scrollAreaNLV.setWidget(self.nodeLibraryViewer)
        self.nodeLibraryDock.setWidget(scrollAreaNLV)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                           self.nodeLibraryDock)

        # node property dock
        self.nodePropertiesDock = QtGui.QDockWidget('Properties', self)
        self.nodePropertiesDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.nodePropertiesDock.setWidget(self.nodePropertyViewer)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                           self.nodePropertiesDock)
        self.nodePropertiesDock.close()
                        
        # message panel dock
        self.messagePanelDock = QtGui.QDockWidget('Messages', self)
        self.messagePanelDock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.messagePanelDock.setWidget(self.messagePanel)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,
                           self.messagePanelDock)

        # console panel dock
        self.consolePanelDock = QtGui.QDockWidget('Console', self)
        self.consolePanelDock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.consolePanelDock.setWidget(self.consolePanel)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea,
                           self.consolePanelDock)
                    
    def createActions(self):
        self.newProjectAction = self.createAction('&New', self.onNewProject,
                                                  QtGui.QKeySequence.New, 'newProject',
                                                  'Create a new project')
        self.openProjectAction = self.createAction('&Open...', self.onOpenProject,
                                                   QtGui.QKeySequence.Open, 'openProject',
                                                   'Open an existing project')
        self.saveProjectAction = self.createAction('&Save', self.onSaveProject,
                                                   QtGui.QKeySequence.Save, 'saveProject',
                                                   'Save the project')
        self.savaAsProjectAction = self.createAction('Save &As...', self.onSaveAsProject,
                                                     icon='saveAsProject',
                                                     tip='Save the project using a new name')
        self.exitAction = self.createAction('E&xit', self.close,
                                             icon='exit',
                                             tip='Close ShaderLink')    

        self.undoAction = self.createAction('&Undo', self.onUndo,
                                            QtGui.QKeySequence.Undo, 'undo',
                                            'Undo last command')
        self.undoAction.setDisabled(True)
        self.redoAction = self.createAction('&Redo', self.onRedo,
                                            QtGui.QKeySequence.Redo, 'redo',
                                            'Redo last command')   
        self.redoAction.setDisabled(True)

        self.copyAction = self.createAction('&Copy', self.onCopy,
                                            QtGui.QKeySequence.Copy, 'copy',
                                            'Copy current selection')
        self.copyAction.setDisabled(True)                                        
        self.pasteAction = self.createAction('&Paste', self.onPaste,
                                            QtGui.QKeySequence.Paste, 'paste',
                                            'Paste last copied selection')        
        self.pasteAction.setDisabled(True)
        self.deleteAction = self.createAction('&Delete', self.onDelete,
                                              QtGui.QKeySequence.Delete, 'delete',
                                              'Delete current selection')                                        
        self.deleteAction.setDisabled(True)

        self.previewAction = self.createAction('&Preview', self.onPreview,
                                               'Shift+F5', 'preview',
                                               'Preview')                                        
        self.previewAction.setDisabled(True)
        
        self.hidePreviewAction = self.createAction('&HidePreview', self.onHidePreview,
                                                   'Ctrl+H', 'hidePreview',
                                                   'Hide preview')
        self.hidePreviewAction.setDisabled(True)                             
                
        self.viewAllAction = self.createAction('&ViewAll', self.onViewAll,
                                               'Ctrl+A', 'viewAll',
                                               'View all')   
        
        self.renderAction = self.createAction('&Render', self.onRender,
                                              'F5', 'render',
                                              'Render') 
        
        self.codeEditorAction = self.createAction('&Code Editor', self.onCodeEditor,
                                                  'F6', 'codeEditor',
                                                  'Code Editor') 

        self.codeGeneratorAction = self.createAction('Code &Generator', self.onCodeGenerator,
                                                     'F7', 'codeGenerator',
                                                     'Code Generator') 
        
        self.rendererSettings = self.createAction('Renderer &Settings', self.onRendererSettings,
                                                     'F8', 'rendererSettings',
                                                     'Renderer Settings') 
                       
        self.nodePropertiesDockAction = self.nodePropertiesDock.toggleViewAction()
        self.nodePropertiesDockAction.setText('&Properties')
        self.nodePropertiesDockAction.setShortcut('CTRL+P')
        self.nodePropertiesDockAction.setIcon(QtGui.QIcon(':/properties.png'))
        self.nodeLibraryDockAction = self.nodeLibraryDock.toggleViewAction()
        self.nodeLibraryDockAction.setText('&Library')
        self.nodeLibraryDockAction.setShortcut('CTRL+L')
        self.nodeLibraryDockAction.setIcon(QtGui.QIcon(':/library.png'))
        self.messagePanelDockAction = self.messagePanelDock.toggleViewAction()
        self.messagePanelDockAction.setText('&Messages')
        self.messagePanelDockAction.setShortcut('CTRL+M')
        self.messagePanelDockAction.setIcon(QtGui.QIcon(':/messages.png'))
        self.renderingPanelDockAction = self.renderingPanelDock.toggleViewAction()
        self.renderingPanelDockAction.setText('&Rendering')
        self.renderingPanelDockAction.setShortcut('CTRL+R')
        self.renderingPanelDockAction.setIcon(QtGui.QIcon(':/rendering.png'))
        self.consolePanelDockAction = self.consolePanelDock.toggleViewAction()
        self.consolePanelDockAction.setText('&Console')
        self.consolePanelDockAction.setShortcut('CTRL+I')
        self.consolePanelDockAction.setIcon(QtGui.QIcon(':/console.png'))
        
        self.aboutAction = self.createAction('&About', self.onAbout, None, 'about') 
                
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenuActions = (self.newProjectAction,
                                self.openProjectAction,
                                self.saveProjectAction, self.savaAsProjectAction,
                                self.exitAction)    
        
        self.connect(self.fileMenu, QtCore.SIGNAL("aboutToShow()"),
                     self.updateFileMenu)
        
        self.editMenu = self.menuBar().addMenu('&Edit')
        self.addActions(self.editMenu, (self.undoAction, self.redoAction,
                                        None,
                                        self.copyAction, self.pasteAction, self.deleteAction,
                                        None,
                                        self.hidePreviewAction,
                                        self.previewAction))    
    
        self.buildMenu = self.menuBar().addMenu('&Build')
        self.addActions(self.buildMenu, (self.renderAction, None, self.codeEditorAction, self.codeGeneratorAction))

        
        self.windowMenu = self.menuBar().addMenu('&Window')
        self.addActions(self.windowMenu, (self.nodePropertiesDockAction,
                                          self.nodeLibraryDockAction,
                                          self.renderingPanelDockAction,
                                          None,
                                          self.messagePanelDockAction,
                                          self.consolePanelDockAction,
                                          None,
                                          self.rendererSettings))
        
        self.helpMenu = self.menuBar().addMenu('&Help')
        self.addActions(self.helpMenu, (self.aboutAction,))  
        
    
    def createToolbars(self):    
        self.mainToolbar = self.addToolBar('Main')
        self.mainToolbar.setObjectName('Main')
        self.addActions(self.mainToolbar, (self.newProjectAction,
                                           self.openProjectAction,
                                           self.saveProjectAction,
                                           None,
                                           self.undoAction, self.redoAction,
                                           None,
                                           self.copyAction, self.pasteAction, self.deleteAction,
                                           None,
                                           self.hidePreviewAction,
                                           self.previewAction,
                                           None,
                                           self.viewAllAction,
                                           None,
                                           self.renderAction,
                                           None,
                                           self.codeEditorAction, self.codeGeneratorAction))

        self.windowToolbar = self.addToolBar('Window')
        self.windowToolbar.setObjectName('Window')
        self.addActions(self.windowToolbar, (self.nodePropertiesDockAction,
                                             self.nodeLibraryDockAction,
                                             self.renderingPanelDockAction,
                                             None,
                                             self.messagePanelDockAction,                                             
                                             self.consolePanelDockAction))
                                                    
    def attachViewsToModel(self):
        self.connect(self.shaderLink, QtCore.SIGNAL('nodeLibraryLoaded'),
                     self.nodeLibraryViewer.controller.onNodeLibraryLoaded) 
        
        self.connect(self.shaderLink, QtCore.SIGNAL('renderingSettingsLoaded'),
                     self.renderingPanel.controller.onRenderingSettingsLoaded)         

        self.connect(self.renderingPanel.controller, QtCore.SIGNAL('renderingSettingsChanged'),
                     self.controller.onRenderingSettingsChanged)     

        self.connect(self.shaderLink, QtCore.SIGNAL('nodeAdded'),
                     self.renderingPanel.controller.onNodeAdded) 
                
        self.connect(self.shaderLink, QtCore.SIGNAL('nodeAdded'),
                     self.controller.onNodeAdded)  

        self.connect(self.shaderLink, QtCore.SIGNAL('nodeRemoved'),
                     self.renderingPanel.controller.onNodeRemoved)         

        self.connect(self.shaderLink, QtCore.SIGNAL('nodeLoaded'),
                     self.controller.onNodeLoaded) 
        
        self.connect(self.commandProcessor, QtCore.SIGNAL('commandExecuted'),
                     self.controller.onCommandExecuted)     

        self.connect(self.commandProcessor, QtCore.SIGNAL('copyCommandChanged'),
                     self.controller.onCopyCommandChanged)     

        scene = self.gfxPanel.scene()
        self.connect(scene, QtCore.SIGNAL('selectionChanged()'),
                     self.controller.onSelectionChanged)     
        self.connect(scene, QtCore.SIGNAL('selectionChanged()'),
                     self.nodePropertyViewer.onSelectionChanged)
        
        self.connect(self.commandProcessor, QtCore.SIGNAL('dirtyStateChanged'),
                     self.controller.onDirtyStateChanged)             
    
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal='triggered()'):
        # create a base action
        action = QtGui.QAction(text, self)
        
        # fill it with useful stuff
        if icon is not None:
            action.setIcon(QtGui.QIcon(':/%s.png' % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, QtCore.SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action
    
    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)        

    def setFileName(self, fileName):
        self.fileName = fileName
        
        if self.fileName == '':
            self.setWindowTitle('Shaderlink')
        else:
            self.setWindowTitle('Shaderlink - %s' % self.fileName)
            # add to recently files
            self.addRecentFile(self.fileName)

    def onNewProject(self):
        self.controller.onNewProject()

    def onOpenProject(self):
        self.controller.onOpenProject()

    def onSaveProject(self):
        self.controller.onSaveProject()

    def onSaveAsProject(self):
        self.controller.onSaveAsProject()

    def onUndo(self):
        self.controller.onUndo()
        
    def onRedo(self):
        self.controller.onRedo()
        
    def onCopy(self):
        self.controller.onCopy()
        
    def onPaste(self):
        self.controller.onPaste()
        
    def onDelete(self):
        self.controller.onDelete()
        
    def onViewAll(self):
        self.controller.onViewAll()
        
    def onRender(self):
        self.controller.onRender()

    def onCodeEditor(self):
        self.controller.onCodeEditor()

    def onCodeGenerator(self):
        self.controller.onCodeGenerator()

    def onPreview(self):
        self.controller.onPreview()

    def onHidePreview(self):
        self.controller.onHidePreview()
        
    def onRendererSettings(self):
        self.controller.onRendererSettings()
        
    def onAbout(self):
        self.controller.onAbout()
        
    def closeEvent(self, event):
        self.controller.onCloseEvent(event)
                  