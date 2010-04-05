##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

from PyQt4 import QtGui, QtCore

import copy

class Command(object):
    Normal = 0
    NoUndo = 1
    ResetUndoRedo = 2
    ResetRedo = 3
    
    def __init__(self, name, type):
        self.name = name
        self.type = type
      
    def do(self):
        assert 0, 'do needs to be implemented!'
        
    def undo(self):
        assert 0, 'undo needs to be implemented!'

    def redo(self):
        assert 0, 'redo needs to be implemented!'

    def invalidateDirtyState(self):
        assert 0, 'redo needs to be implemented!'

# TODO: commands must handle selection state

class UndoCommand(Command):
    def __init__(self, commandProcessor):
        Command.__init__(self, 'Undo', Command.NoUndo)
        
        self.commandProcessor = commandProcessor
        
    def do(self):
        self.commandProcessor.undoLastCommand()
        
    def invalidateDirtyState(self):
        return False, None        
        
class RedoCommand(Command):
    def __init__(self, commandProcessor):
        Command.__init__(self, 'Redo', Command.NoUndo)
        
        self.commandProcessor = commandProcessor
        
    def do(self):
        self.commandProcessor.redoLastUndoneCommand()

    def invalidateDirtyState(self):
        return False, None        
        
class FitInViewCommand(Command):
    def __init__(self, gfxPanel):
        Command.__init__(self, 'FitInView', Command.NoUndo)
        
        self.gfxPanel = gfxPanel 

    def do(self):        
        # fit in view
        items = self.gfxPanel.items()       
        if items == []:
            return        
        
        unionRect = items[0].sceneBoundingRect()
        for i in range(1, len(items)):
            rect = items[i].sceneBoundingRect()
            unionRect = unionRect.united(rect)
        
        self.gfxPanel.fitInView(unionRect, QtCore.Qt.KeepAspectRatio)   

    def invalidateDirtyState(self):
        return False, False        
                     
class AddNodeCommand(Command):
    def __init__(self, shaderLink, gfxPanel, dirName, nodeName, dropPoint):
        Command.__init__(self, 'AddNode', Command.Normal)
        
        self.shaderLink = shaderLink
        self.gfxPanel = gfxPanel
        
        # to look up a node into the node library
        self.dirName = dirName
        self.nodeName = nodeName
        
        # where we dropped the node
        self.dropPoint = dropPoint

    def do(self):
        # add node from library at drop position        
        self.node = self.shaderLink.addNodeFromLibrary(self.dirName, self.nodeName, self.dropPoint)
    
    def undo(self):      
        # remove node
        self.shaderLink.removeNode(self.node)
        
    def redo(self):
        # add node
        self.shaderLink.addNode(self.node)

    def invalidateDirtyState(self):
        return True, True        
        
class AddLinkCommand(Command):
    def __init__(self, shaderLink, gfxPanel, sourceNode, destNode, sourceProp, destProp):
        Command.__init__(self, 'AddLink', Command.Normal)
        
        self.shaderLink = shaderLink                
        self.gfxPanel = gfxPanel

        # nodes to create the link from
        self.sourceNode = sourceNode
        self.destNode = destNode
        
        # link properties to create the link from
        self.sourceProp = sourceProp
        self.destProp = destProp    

    def do(self):
        # modify model and view and save node for later undo/redo        
        self.link = self.shaderLink.addLinkFromNodes(self.sourceNode, 
                                                     self.destNode, 
                                                     self.sourceProp, 
                                                     self.destProp)
                    
    def undo(self):
        self.shaderLink.removeLink(self.link)
        
    def redo(self):
        self.shaderLink.addLink(self.link)

    def invalidateDirtyState(self):
        return True, True        
        
class MoveCommand(Command):
    def __init__(self, gfxPanel, startPositions, endPositions):
        Command.__init__(self, 'Move', Command.Normal)
        
        self.gfxPanel = gfxPanel
        
        # gfx items positions
        self.startPositions = {}
        self.endPositions = {}
        
        # copy start and end positions
        for item, startPosition in startPositions.iteritems():            
            self.startPositions[item] = QtCore.QPointF(startPosition)
        for item, endPosition in endPositions.iteritems():
            self.endPositions[item] = QtCore.QPointF(endPosition)
        
    def do(self):
        # qt Graphics View Framework handles the updating of position 
        pass
    
    def undo(self):
        # undo to start position
        for item, startPosition in self.startPositions.iteritems():            
            item.setPos(startPosition)

    def redo(self):
        # redo to end position
        for item, endPosition in self.endPositions.iteritems():
            item.setPos(endPosition)

    def invalidateDirtyState(self):
        return True, True        

class DeleteCommand(Command):
    def __init__(self, shaderLink, gfxPanel, gfxItems):
        Command.__init__(self, 'Delete', Command.ResetRedo)
        
        self.shaderLink = shaderLink
        self.gfxPanel = gfxPanel
        
        self.gfxNodes = []
        self.gfxLinks = []
                
        # save nodes and links for undo/redo       
        from gfx.view import GfxNode, GfxLink         
        for gfxItem in gfxItems:
            if isinstance(gfxItem, GfxLink):
                self.gfxLinks.append(gfxItem)            
            if isinstance(gfxItem, GfxNode):
                self.gfxNodes.append(gfxItem)

        # find dependent links to delete
        for gfxNode in self.gfxNodes:                
            # find dependent output links
            outputGfxLinks = gfxNode.allOutputGfxLinks()
            for outputGfxLink in outputGfxLinks:
                if outputGfxLink not in self.gfxLinks:
                    self.gfxLinks.append(outputGfxLink)
    
            # find dependent input links
            inputGfxLinks = gfxNode.allInputGfxLinks()
            for inputGfxLink in inputGfxLinks:
                if inputGfxLink not in self.gfxLinks:
                    self.gfxLinks.append(inputGfxLink)
                        
    def do(self):
        # remove links
        for gfxLink in self.gfxLinks:
            self.shaderLink.removeLink(gfxLink.link)

        # remove nodes
        for gfxNode in self.gfxNodes:
            self.shaderLink.removeNode(gfxNode.node)
    
    def undo(self):
        # restore links
        for gfxLink in self.gfxLinks:
            link = gfxLink.link            
                        
            # add link
            self.shaderLink.addLink(link)
    
        # restore nodes
        for gfxNode in self.gfxNodes:
            node = gfxNode.node
            self.shaderLink.addNode(node)
                
    def redo(self):
        # we're lucky redo is the same as do
        self.do()
        
    def invalidateDirtyState(self):
        return True, True        
        
class CopyCommand(Command):
    def __init__(self, gfxItems):
        Command.__init__(self, 'Copy', Command.NoUndo)
        
        self.gfxItems = gfxItems
        
        self.nodesToBeCopied = []
        self.positions = {}
                
    def do(self):
        for gfxItem in self.gfxItems:
            from gfx.view import GfxNode
            if isinstance(gfxItem, GfxNode):                
                self.nodesToBeCopied.append(gfxItem.node)
                self.positions[gfxItem.node] = QtCore.QPointF(gfxItem.pos())         

    def invalidateDirtyState(self):
        return False, None
                
class PasteCommand(Command):
    def __init__(self, shaderLink, gfxPanel, copyCommand):
        Command.__init__(self, 'Paste', Command.Normal)
        
        self.copyCommand = copyCommand
        self.shaderLink = shaderLink
        self.gfxPanel = gfxPanel
        
        # TODO: handle links too
        self.copiedNodes = []
        
    def do(self):        
        for nodeToBeCopied in self.copyCommand.nodesToBeCopied: 
            # create a new node            
            from core.model import Node
            copiedNode = nodeToBeCopied.copy()
            
            # fix name redefinitions
            self.shaderLink.fixNodeNameRedefinitions(copiedNode)
            
            # save it
            self.copiedNodes.append(copiedNode)
                                                
            # update position
            newPos = self.copyCommand.positions[nodeToBeCopied] + QtCore.QPointF(20.0, 20.0)
            self.copyCommand.positions[nodeToBeCopied] = newPos
            copiedNode.gfxNode.setPos(newPos)
            
            # add node
            self.shaderLink.addNode(copiedNode)
            
    def undo(self):
        for copiedNode in self.copiedNodes:   
            # remove node
            self.shaderLink.removeNode(copiedNode)
            
        for nodeToBeCopied in self.copyCommand.nodesToBeCopied:
            # update position
            newPos = self.copyCommand.positions[nodeToBeCopied] - QtCore.QPointF(20.0, 20.0)
            self.copyCommand.positions[nodeToBeCopied] = newPos
                         
    def redo(self):
        for copiedNode in self.copiedNodes:   
            # add node
            self.shaderLink.addNode(copiedNode)

    def invalidateDirtyState(self):
        return True, True

class EditPropertyCommand(Command):
    def __init__(self, property, newValue):
        Command.__init__(self, 'EditProperty', Command.Normal)
        
        self.property = property
        self.newValue = newValue        
        self.oldValue = None

    def do(self):
        # save value for later undo
        self.oldValue = copy.deepcopy(self.property.value)
        
        # set new value
        self.property.value = copy.deepcopy(self.newValue)
        
        # propagate change
        self.property.fireChanged()
    
    def undo(self):
        # restore old value      
        self.property.value = copy.deepcopy(self.oldValue)

        # propagate change
        self.property.fireChanged()
        
    def redo(self):
        # just the same as do
        self.do()
        
    def invalidateDirtyState(self):
        return True, True
                
class EditTuple3DPropertyCommand(Command):
    def __init__(self, property, newValue, spaceIndex):
        Command.__init__(self, 'EditProperty', Command.Normal)
        
        self.property = property
        self.newValue = newValue        
        self.oldValue = None
        self.spaceIndex = spaceIndex

    def do(self):
        # save value for later undo
        self.oldValue = copy.deepcopy(self.property.value)
        self.oldSpaceIndex = self.property.spaceIndex
        
        # set new value
        self.property.value = copy.deepcopy(self.newValue)
        
        # propagate change
        self.property.fireChanged()
    
    def undo(self):
        # restore old value      
        self.property.value = copy.deepcopy(self.oldValue)
        self.property.spaceIndex = self.spaceIndex

        # propagate change
        self.property.fireChanged()
        
    def redo(self):
        # just the same as do
        self.do()        

    def invalidateDirtyState(self):
        return True, True
        
class NewCommand(Command):
    def __init__(self, mainWindow):
        Command.__init__(self, 'New', Command.ResetUndoRedo)
        
        self.mainWindow = mainWindow
    
    def do(self):
        self.mainWindow.shaderLink.clear()
        
        # update filename
        self.mainWindow.setFileName('')
        
        # rendering settings
        self.mainWindow.shaderLink.loadRenderingDefaultSettings()
        
    def invalidateDirtyState(self):
        return True, False

class OpenCommand(Command):
    def __init__(self, mainWindow, fileName):
        Command.__init__(self, 'Open', Command.ResetUndoRedo)
        
        self.mainWindow = mainWindow
        self.fileName = fileName
    
    def do(self):        
        nodes = None
        links = None

        # load a file
        f = open(self.fileName, 'rb')          
        
        try:                           
            import cPickle
            unpickler = cPickle.Unpickler(f)
        
            nodes = unpickler.load()
            linksToDo = unpickler.load()            
            nodeNamesInUse = unpickler.load()    
            renderingSettings = unpickler.load()
        finally:            
            f.close()
                        
        # clear the model
        self.mainWindow.shaderLink.clear()          
        
        # add nodes
        for node in nodes:
            self.mainWindow.shaderLink.addNode(node)

        # add links
        for linkToDo in linksToDo:
            from core.model import Link
            link = Link.buildFrom(linkToDo['sourceNode'], linkToDo['destNode'], 
                                  linkToDo['sourceProp'], linkToDo['destProp'])
            self.mainWindow.shaderLink.addLink(link)
        
        # add name cache
        self.mainWindow.shaderLink.nodeNamesInUse = nodeNamesInUse
        
        # update filename
        self.mainWindow.setFileName(self.fileName)
        
        # rendering settings
        import copy
        self.mainWindow.shaderLink.renderingSettings = copy.deepcopy(renderingSettings)
        self.mainWindow.shaderLink.fireRenderingSettingsLoaded()
        
        # fit in view
        items = self.mainWindow.gfxPanel.items()       
        if items == []:
            return        
        
        unionRect = items[0].sceneBoundingRect()
        for i in range(1, len(items)):
            rect = items[i].sceneBoundingRect()
            unionRect = unionRect.united(rect)
        
        self.mainWindow.gfxPanel.fitInView(unionRect, QtCore.Qt.KeepAspectRatio)  
        
    def invalidateDirtyState(self):
        return True, False

class SaveCommand(Command):
    def __init__(self, mainWindow, fileName):
        Command.__init__(self, 'Save', Command.ResetUndoRedo)
        
        self.mainWindow = mainWindow
        self.fileName = fileName
        
    def do(self):        
        # save to file
        f = open(self.fileName, 'wb')
        
        try:        
            import cPickle
            pickler = cPickle.Pickler(f, 2)
            
            # save nodes
            pickler.dump(self.mainWindow.shaderLink.nodes.values())
            
            # save links
            linksToDo = []
            for link in self.mainWindow.shaderLink.links.values():
                linkToDo = {'sourceNode' : link.sourceNode, 'destNode' : link.destNode, 
                            'sourceProp' : link.sourceProp, 'destProp' : link.destProp}
                linksToDo.append(linkToDo)            
            pickler.dump(linksToDo)
            
            # save name cache
            pickler.dump(self.mainWindow.shaderLink.nodeNamesInUse)
            
            # save rendering settings
            pickler.dump(self.mainWindow.shaderLink.renderingSettings)
        finally:    
            f.close()

        # update filename
        self.mainWindow.setFileName(self.fileName)

    def invalidateDirtyState(self):
        return True, False
          
class EditRenderingSettingsCommand(Command):
    def __init__(self, shaderLink, setting, value):
        Command.__init__(self, 'EditRenderingOptions', Command.NoUndo)
        
        self.shaderLink = shaderLink
        self.setting = setting
        self.value = value
        
    def do(self):
        import copy
        self.shaderLink.renderingSettings[self.setting] = copy.deepcopy(self.value)
        
    def invalidateDirtyState(self):
        return True, True

class RenderCommand(Command):
    def __init__(self, shaderLink, mainWindow):
        Command.__init__(self, 'RenderCommand', Command.NoUndo)
        
        self.shaderLink = shaderLink
        self.renderingSettings = self.shaderLink.renderingSettings 
        self.mainWindow = mainWindow
        
    def getRootNodeNameFromSettings(self, renderingSettingsShader):
        rootNodeNameList = renderingSettingsShader[0]
        rootNodeNameIndex = renderingSettingsShader[1]
        
        return rootNodeNameList[rootNodeNameIndex]

    def buildShaders(self, shaderBuilder):
        # build shaders and rib
        try:
            from time import gmtime, strftime
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Build shaders started at %s.' % timeStr)
            
            shaderBuilder.buildShaders()
            
            self.mainWindow.consolePanel.insertNormalText('Building shaders SUCCEEDED!')
            
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Build shaders done at %s.\n' % timeStr)
                                    
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Build rib started at %s.' % timeStr)        
            
            shaderBuilder.buildRib()
            
            self.mainWindow.consolePanel.insertNormalText('Building rib SUCCEEDED!')
            
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Build rib done at %s.\n' % timeStr)            
        except:
            from gui.view import MessagePanel
            self.mainWindow.messagePanel.insertMessage(MessagePanel.ErrorType, 'Error during code generation.')
            raise
        
    def compileShaders(self, shaderBuilder):
        compileCommandExecution = {}
        try:
            from time import gmtime, strftime
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Shaders compilation started at %s.' % timeStr)
            compileCommandExecution = shaderBuilder.compileShaders()
        except:
            from gui.view import MessagePanel
            self.mainWindow.messagePanel.insertMessage(MessagePanel.ErrorType, 'Error during shader compilation.')
            raise
        finally:
            # compile
            for shaderFileNamePath, cce in compileCommandExecution.iteritems():
                self.mainWindow.consolePanel.insertNormalText('Compiling shader %s.' % shaderFileNamePath)
                command = cce['command']
                self.mainWindow.consolePanel.insertNormalText(command)
                stdout = cce['commandResult']
                self.mainWindow.consolePanel.insertNormalText(stdout)
                if cce['retval'] != 0:
                    self.mainWindow.consolePanel.insertNormalText('Compilation FAILED!')
                else:
                    self.mainWindow.consolePanel.insertNormalText('Compilation SUCCEEDED!')
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Shaders compilation done at %s.\n' % timeStr)           

    def renderRib(self, shaderBuilder):
        renderCommandExecution = None
        try:
            from time import gmtime, strftime
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Rib rendering started at %s.' % timeStr)
            renderCommandExecution = shaderBuilder.renderRib()
        except:
            from gui.view import MessagePanel
            self.mainWindow.messagePanel.insertMessage(MessagePanel.ErrorType, 'Error during rib rendering.')
            raise
        finally:        
            if renderCommandExecution:                 
                command = renderCommandExecution['command']
                self.mainWindow.consolePanel.insertNormalText(command)
                stdout = renderCommandExecution['commandResult']
                self.mainWindow.consolePanel.insertNormalText(stdout)
                if renderCommandExecution['retval'] != 0:
                    self.mainWindow.consolePanel.insertNormalText('Rendering FAILED!')
                else:
                    self.mainWindow.consolePanel.insertNormalText('Rendering SUCCEEDED!')
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Rib rendering done at %s.\n' % timeStr)                    

        self.mainWindow.consolePanel.insertBoldText('--------------------------------')
                
    def do(self):
        # get root node names from settings
        rootNodeNames = [self.getRootNodeNameFromSettings(self.renderingSettings['Surface']),
                         self.getRootNodeNameFromSettings(self.renderingSettings['Displacement']),
                         self.getRootNodeNameFromSettings(self.renderingSettings['Atmosphere']),
                         self.getRootNodeNameFromSettings(self.renderingSettings['Interior']),
                         self.getRootNodeNameFromSettings(self.renderingSettings['Exterior']),
                         self.getRootNodeNameFromSettings(self.renderingSettings['Imager'])]
        
        # filter node names
        rootNodeNames = filter(lambda name: name != 'None', rootNodeNames)
        
        # get root nodes
        rootNodes = [self.shaderLink.getNodeFromName(name) for name in rootNodeNames]               
        
        # create shader builder        
        from core.generator import ShaderBuilder
        shaderBuilder = ShaderBuilder(self.shaderLink, rootNodes, self.shaderLink.renderingSettings)
        
        # build shaders
        self.buildShaders(shaderBuilder)

        # compile shaders
        self.compileShaders(shaderBuilder) 
        
        # render rib
        self.renderRib(shaderBuilder)
        
        # convert to png
        import os
        previewImgPath = os.path.join(self.shaderLink.paths['temp'], 'preview.tif')
        previewConvertedImgPath = os.path.join(self.shaderLink.paths['temp'], 'preview.png')
        import Image
        im = Image.open(previewImgPath)
        im.save(previewConvertedImgPath)                
        
        # preview
        p = QtGui.QPixmap(previewConvertedImgPath)
        if self.renderingSettings['Preview']:
            self.mainWindow.renderingPanel.previewImg.setPixmap(p)
        else:
            self.mainWindow.renderImageDialog.setPixmap(p)            
            self.mainWindow.renderImageDialog.exec_()
                           
    def invalidateDirtyState(self):
        return False, False

class EditNodeCodeCommand(Command):
    def __init__(self, node, code):
        Command.__init__(self, 'EditNode', Command.NoUndo)
        
        self.node = node
        self.code = code
        
    def do(self):
        self.node.code = self.code
        
    def invalidateDirtyState(self):
        return True, True

class EditPropertyShaderParameterCommand(Command):
    def __init__(self, property, value):
        Command.__init__(self, 'EditPropertyShaderParameter', Command.NoUndo)
        
        self.property = property
        self.value = value
        
    def do(self):
        self.property.isShaderParameter = self.value
        
    def invalidateDirtyState(self):
        return True, True
    
class PreviewNodeCommand(Command):
    def __init__(self, shaderLink, gfxNodes, mainWindow):
        Command.__init__(self, 'PreviewNodeCommand', Command.NoUndo)
        
        self.shaderLink = shaderLink
        self.gfxNodes = gfxNodes
        self.mainWindow = mainWindow
        
    def buildShaders(self, previewBuilder):
        # build shaders and rib
        try:
            from time import gmtime, strftime
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Build shaders started at %s.' % timeStr)
            
            previewBuilder.buildShaders()
            
            self.mainWindow.consolePanel.insertNormalText('Building shaders SUCCEEDED!')
            
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Build shaders done at %s.\n' % timeStr)
                                    
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Build rib started at %s.' % timeStr)        
            
            previewBuilder.buildRib()
            
            self.mainWindow.consolePanel.insertNormalText('Building rib SUCCEEDED!')
            
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Build rib done at %s.\n' % timeStr)            
        except:
            from gui.view import MessagePanel
            self.mainWindow.messagePanel.insertMessage(MessagePanel.ErrorType, 'Error during code generation.')
            raise
        
    def compileShaders(self, previewBuilder):
        compileCommandExecution = {}
        try:
            from time import gmtime, strftime
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Shaders compilation started at %s.' % timeStr)
            compileCommandExecution = previewBuilder.compileShaders()
        except:
            from gui.view import MessagePanel
            self.mainWindow.messagePanel.insertMessage(MessagePanel.ErrorType, 'Error during shader compilation.')
            raise
        finally:
            # compile
            for shaderFileNamePath, cce in compileCommandExecution.iteritems():
                self.mainWindow.consolePanel.insertNormalText('Compiling shader %s.' % shaderFileNamePath)
                command = cce['command']
                self.mainWindow.consolePanel.insertNormalText(command)
                stdout = cce['commandResult']
                self.mainWindow.consolePanel.insertNormalText(stdout)
                if cce['retval'] != 0:
                    self.mainWindow.consolePanel.insertNormalText('Compilation FAILED!')
                else:
                    self.mainWindow.consolePanel.insertNormalText('Compilation SUCCEEDED!')
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Shaders compilation done at %s.\n' % timeStr)           

    def renderRib(self, previewBuilder):
        renderCommandExecution = None
        try:
            from time import gmtime, strftime
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Rib rendering started at %s.' % timeStr)
            renderCommandExecution = previewBuilder.renderRib()
        except:
            from gui.view import MessagePanel
            self.mainWindow.messagePanel.insertMessage(MessagePanel.ErrorType, 'Error during rib rendering.')
            raise
        finally:        
            if renderCommandExecution:                 
                command = renderCommandExecution['command']
                self.mainWindow.consolePanel.insertNormalText(command)
                stdout = renderCommandExecution['commandResult']
                self.mainWindow.consolePanel.insertNormalText(stdout)
                if renderCommandExecution['retval'] != 0:
                    self.mainWindow.consolePanel.insertNormalText('Rendering FAILED!')
                else:
                    self.mainWindow.consolePanel.insertNormalText('Rendering SUCCEEDED!')
            timeStr = strftime('%a, %d %b %Y %H:%M:%S', gmtime())
            self.mainWindow.consolePanel.insertBoldText('Rib rendering done at %s.\n' % timeStr)                    

        self.mainWindow.consolePanel.insertBoldText('--------------------------------')
                
    def do(self):
        for gfxNode in self.gfxNodes:         
            if gfxNode.node.previewCodes == {}:
                from gui.view import MessagePanel
                self.mainWindow.messagePanel.insertMessage(MessagePanel.ErrorType, 
                                                           'Node %s doesn\'t have a preview attached.' % gfxNode.node.name)
                return            
                   
            # create shader builder        
            from core.generator import PreviewBuilder
            previewBuilder = PreviewBuilder(self.shaderLink, gfxNode)
            
            # build shaders
            self.buildShaders(previewBuilder)
    
            # compile shaders
            self.compileShaders(previewBuilder) 
            
            # render rib
            self.renderRib(previewBuilder)
            
            # convert to png
            import os
            previewImgPath = os.path.join(self.shaderLink.paths['temp'], gfxNode.node.name + '.tif')
            previewConvertedImgPath = os.path.join(self.shaderLink.paths['temp'], gfxNode.node.name + '.png')
            import Image
            im = Image.open(previewImgPath)
            im.save(previewConvertedImgPath)                
            
            # preview
            pixmap = QtGui.QPixmap(previewConvertedImgPath)
            gfxNode.setPreviewPixmap(pixmap)
                           
    def invalidateDirtyState(self):
        return False, False    

class HidePreviewCommand(Command):
    def __init__(self, gfxNodes):
        Command.__init__(self, 'HidePreviewCommand', Command.NoUndo)
        
        self.gfxNodes = gfxNodes
        
    def do(self):
        for gfxNode in self.gfxNodes:
            gfxNode.setPreviewPixmap(None)
        
    def invalidateDirtyState(self):
        return True, True

class RendererSettingsCommand(Command):
    def __init__(self, shaderlink, rendererIndex):
        Command.__init__(self, 'RendererSettingsCommand', Command.NoUndo)
        
        self.shaderlink = shaderlink
        self.rendererIndex = rendererIndex
        
    def do(self):
        self.shaderlink.currentRendererIndex = self.rendererIndex
        
    def invalidateDirtyState(self):
        return True, True