##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

import math

from PyQt4 import QtCore, QtGui

class GfxPanelState(object):
    def __init__(self, controller):
        self.controller = controller
        
    def onMousePressEvent(self, event):
        assert(0), '%s:, onMousePressEvent must be implemented' % (self.__name__)

    def onMouseDoubleClickEvent(self, event):
        assert(0), '%s:, onMouseDoubleClickEvent must be implemented' % (self.__name__)
    
    def onMouseMoveEvent(self, event):
        assert(0), '%s:, onMouseMoveEvent must be implemented' % (self.__name__)
    
    def onMouseReleaseEvent(self, event):        
        assert(0), '%s:, onMouseReleaseEvent must be implemented' % (self.__name__)
    
    def onWheelEvent(self, event):
        assert(0), '%s:, onWheelEvent must be implemented' % (self.__name__)

    def onKeyPressEvent(self, event):
        assert(0), '%s:, onKeyPressEvent must be implemented' % (self.__name__)
                
    def onDragEnterEvent(self, event):
        assert(0), '%s:, onDragEnterEvent must be implemented' % (self.__name__)
    
    def onDragMoveEvent(self, event):
        assert(0), '%s:, onDragMoveEvent must be implemented' % (self.__name__)
    
    def onDropEvent(self, event):
        assert(0), '%s:, onDropEvent must be implemented' % (self.__name__)

class GfxPanelPanState(object):
    def __init__(self, controller):
        self.controller = controller
        self.panStartPos = None

    def onMousePressEvent(self, event):
        self.panStartPos = self.controller.gfxPanel.mapToScene(event.pos())
        
    def onMouseMoveEvent(self, event):
        panCurrentPos = self.controller.gfxPanel.mapToScene(event.pos())
        panDeltaPos = panCurrentPos - self.panStartPos

        # update view matrix
        self.controller.gfxPanel.setInteractive(False)
        self.controller.gfxPanel.translate(panDeltaPos.x(), panDeltaPos.y())        
        self.controller.gfxPanel.setInteractive(True)        

    def onMouseReleaseEvent(self, event):        
        self.panStartPos = None
        # return to idle state        
        self.controller.currentState = self.controller.states[GfxPanelIdleState]
                            
class GfxPanelIdleState(GfxPanelState):
    def __init__(self, controller):
        self.controller = controller
                
    def onMousePressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            # switch to pan state
            self.controller.currentState = self.controller.states[GfxPanelPanState] 
            # let the right state handle the event
            self.controller.currentState.onMousePressEvent(event)
            return
        
        itemPressed = self.controller.gfxPanel.itemAt(event.pos())
        
        # if we pick a node
        from gfx.view import GfxNode
        if isinstance(itemPressed, GfxNode):        
            #itemPressed.setSelected(True)
            # look up for a picked property (point in scene space)
            pickData = itemPressed.propertyAt(self.controller.gfxPanel.mapToScene(event.pos()))
            
            # if we pick a property
            from core.model import Property
            if pickData and pickData['property'].category is Property.Output:
                # switch to link state
                self.controller.currentState = self.controller.states[GfxPanelLinkState]                
            else:
                # switch to move state
                self.controller.currentState = self.controller.states[GfxPanelMoveState]
            
            # let the right state handle the event
            self.controller.currentState.onMousePressEvent(event)
        else:
            # stay in Idle model propagate the event to Qt
            QtGui.QGraphicsView.mousePressEvent(self.controller.gfxPanel, event)

    def onMouseDoubleClickEvent(self, event):
        itemPressed = self.controller.gfxPanel.itemAt(event.pos())
        
        # if we pick a node
        from gfx.view import GfxNode
        if isinstance(itemPressed, GfxNode):        
            from command.command import PreviewNodeCommand
            previewNodeCommand = PreviewNodeCommand(self.controller.shaderLink, [itemPressed,], 
                                                    self.controller.gfxPanel.parent())
            self.controller.commandProcessor.executeCommand(previewNodeCommand)
        else:
            QtGui.QGraphicsView.mouseDoubleClickEvent(self.controller.gfxPanel, event)
                
    def onMouseMoveEvent(self, event):
        QtGui.QGraphicsView.mouseMoveEvent(self.controller.gfxPanel, event)
    
    def onMouseReleaseEvent(self, event):        
        QtGui.QGraphicsView.mouseReleaseEvent(self.controller.gfxPanel, event)
        
    def onWheelEvent(self, event):
        scale = -1.0
        import sys
        if 'linux' in sys.platform:
            scale = 1.0     
        self.controller.scaleView(math.pow(2.0, scale * event.delta() / 600.0))
        
    def onKeyPressEvent(self, event):  
        QtGui.QGraphicsView.keyPressEvent(self.controller.gfxPanel, event)
    
    def onDragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-text'):
            event.accept()
        else:
            event.ignore()

    def onDragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/x-text'):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
            
    def onDropEvent(self, event):
        if event.mimeData().hasFormat('application/x-text'):
            # decode drop stuff
            data = event.mimeData().data('application/x-text')
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            dirName = QtCore.QString()
            nodeName = QtCore.QString()
            stream >> dirName
            stream >> nodeName
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            
            # save dropPoint in scene space
            self.dropNodePoint = self.controller.gfxPanel.mapToScene(event.pos())
            
            # create an add node command and execute it
            from command.command import AddNodeCommand
            addNodeCommand = AddNodeCommand(self.controller.shaderLink,
                                            self.controller.gfxPanel,
                                            unicode(dirName), unicode(nodeName),
                                            self.dropNodePoint)
            self.controller.commandProcessor.executeCommand(addNodeCommand)
        else:
            event.ignore()    
                                                              
class GfxPanelMoveState(GfxPanelState):
    def __init__(self, controller):
        self.controller = controller

        # original positions of view items
        self.startPositions = {}
        self.endPositions = {}
        
        # to understand if we actually move the cursor
        self.mousePressPosition = None
        self.mouseReleasePosition = None

    def onMousePressEvent(self, event):        
        # propagate so that the qt selection mechanism takes place
        QtGui.QGraphicsView.mousePressEvent(self.controller.gfxPanel, event)
        
        self.startPositions.clear()
        self.endPositions.clear()
        
        # save start positions of view items
        scene = self.controller.gfxPanel.scene()
        for selectedItem in scene.selectedItems():
            self.startPositions[selectedItem] = QtCore.QPointF(selectedItem.pos())
            
        # save start mouse press position
        self.mousePressPosition = QtCore.QPoint(event.pos()) 
    
    def onMouseMoveEvent(self, event):
        QtGui.QGraphicsView.mouseMoveEvent(self.controller.gfxPanel, event)
    
    def onMouseReleaseEvent(self, event):
        # to understand if we actually move the cursor
        self.mouseReleasePosition = QtCore.QPoint(event.pos())
        
        # check if we actually moved
        if self.mousePressPosition != self.mouseReleasePosition:
            # save end positions of view items
            scene = self.controller.gfxPanel.scene()
            for selectedItem in scene.selectedItems():
                self.endPositions[selectedItem] = QtCore.QPointF(selectedItem.pos())
            
            # create a move command and execute it
            from command.command import MoveCommand
            moveCommand = MoveCommand(self.controller.gfxPanel, self.startPositions, self.endPositions)
            self.controller.commandProcessor.executeCommand(moveCommand)
            
        # return to idle state        
        self.controller.currentState = self.controller.states[GfxPanelIdleState]
        
        QtGui.QGraphicsView.mouseReleaseEvent(self.controller.gfxPanel, event)
        
    def onWheelEvent(self, event):
        self.controller.scaleView(math.pow(2.0, -event.delta() / 600.0))
        
class GfxPanelLinkState(GfxPanelState):
    def __init__(self, controller):
        self.controller = controller

        # temporary link
        self.gfxLink = None

        # source property stuff
        self.gfxSourceNode = None
        self.sourceProp = None
        self.sourcePoint = None        
        
        # destination property stuff
        self.gfxDestNode = None
        self.destProp = None        
        self.destPoint = None
        
        # mouse on property flag
        self.mouseOnProperty = False
        
    def onMousePressEvent(self, event):
        # propagate to Qt so selected graphics items are selected
        QtGui.QGraphicsView.mousePressEvent(self.controller.gfxPanel, event)
        
        # we got into this state so we know we are on a Property
        itemPressed = self.controller.gfxPanel.itemAt(event.pos())                    
        pickData = itemPressed.propertyAt(self.controller.gfxPanel.mapToScene(event.pos()))
        
        # set source property stuff
        self.gfxSourceNode = itemPressed
        self.sourceProp = pickData['property']
        self.sourcePoint = pickData['point']
        
        # create a GfxLink (points in scene space)
        from gfx.view import GfxLink
        self.gfxLink = GfxLink.createFromPoints(self.sourcePoint, 
                                                self.controller.gfxPanel.mapToScene(event.pos()))
        
        # add GfxLink to the scene
        scene = self.controller.gfxPanel.scene()
        scene.addItem(self.gfxLink)
            
    def onMouseMoveEvent(self, event):
        itemPressed = self.controller.gfxPanel.itemAt(event.pos())
              
        # we can only select GfxNode
        from gfx.view import GfxNode
        if isinstance(itemPressed, GfxNode):
            # look up for a picked property (point in scene space)
            pickData = itemPressed.propertyAt(self.controller.gfxPanel.mapToScene(event.pos()))
            
            from core.model import Property
            if pickData and pickData['property'].category is Property.Input:
                
                node = itemPressed.node 
                pickProperty = pickData['property']
                pickPropertyCenter = pickData['point']
                
                # OK property found
                # check if we can link two properties:
                # we can link if same type and not already linked
                if self.sourceProp.typeToStr() == pickProperty.typeToStr():
                    if not node.isInputPropertyLinked(pickProperty): 
                        self.mouseOnProperty = True
                        self.gfxDestNode = itemPressed
                        self.destProp = pickProperty
                        self.destPoint = pickPropertyCenter
                        self.gfxLink.setDestinationPoint(self.destPoint)
                        return

        # no property found
        self.mouseOnProperty = False
        self.gfxDestNode = None
        self.destProp = None
        self.destPoint = None                              
        self.gfxLink.setDestinationPoint(self.controller.gfxPanel.mapToScene(event.pos()))        
                            
    def onMouseReleaseEvent(self, event):        
        # if we release on a property
        if self.mouseOnProperty:
            # create a new add link command
            from command.command import AddLinkCommand
            addLinkCommand = AddLinkCommand(self.controller.shaderLink,
                                            self.controller.gfxPanel,
                                            self.gfxSourceNode.node, 
                                            self.gfxDestNode.node,
                                            self.sourceProp,
                                            self.destProp)
            # execute command
            self.controller.commandProcessor.executeCommand(addLinkCommand)                          
        
        # remove temporary gfx link
        self.removeGfxLink()
            
        # return to idle state
        self.controller.currentState = self.controller.states[GfxPanelIdleState] 
        
    def onWheelEvent(self, event):
        self.controller.scaleView(math.pow(2.0, -event.delta() / 600.0))
                    
    def removeGfxLink(self):        
        # gfx item
        self.controller.gfxPanel.scene().removeItem(self.gfxLink)
        self.gfxLink = None
        
        # source property stuff
        self.gfxSourceNode = None
        self.sourceProp = None
        self.sourcePoint = None        
        
        # destination property stuff
        self.gfxDestNode = None
        self.destProp = None        
        self.destPoint = None
        
        # mouse on property flag
        self.mouseOnProperty = False
        
class GfxPanelController(object):
    def __init__(self, gfxPanel, shaderLink, commandProcessor):
        self.gfxPanel = gfxPanel
        self.shaderLink = shaderLink         
        self.commandProcessor = commandProcessor

        # state management
        self.states = {GfxPanelIdleState : GfxPanelIdleState(self),
                       GfxPanelMoveState : GfxPanelMoveState(self),
                       GfxPanelLinkState : GfxPanelLinkState(self),
                       GfxPanelPanState : GfxPanelPanState(self)}
        
        # current state
        self.currentState = self.states[GfxPanelIdleState] 
 
    def onNodeAdded(self, node):
        # add it to scene
        scene = self.gfxPanel.scene()
        scene.addItem(node.gfxNode)        

    def onLinkAdded(self, link):                                
        # added it to the scene
        scene = self.gfxPanel.scene()
        scene.addItem(link.gfxLink)
        
    def onNodeRemoved(self, node):        
        # remove it from scene
        scene = self.gfxPanel.scene()
        scene.removeItem(node.gfxNode)    
        
    def onLinkRemoved(self, link):        
        # remove it from scene
        scene = self.gfxPanel.scene()
        scene.removeItem(link.gfxLink)  
                           
    def onMousePressEvent(self, event):
        self.currentState.onMousePressEvent(event)
        
    def onMouseDoubleClickEvent(self, event):
        self.currentState.onMouseDoubleClickEvent(event)
        
    def onMouseMoveEvent(self, event):
        self.currentState.onMouseMoveEvent(event)
        
    def onMouseReleaseEvent(self, event):        
        self.currentState.onMouseReleaseEvent(event)
                
    def onWheelEvent(self, event):
        self.currentState.onWheelEvent(event)

    def onKeyPressEvent(self, event):
        self.currentState.onKeyPressEvent(event)            
    
    def onDragEnterEvent(self, event):
        self.currentState.onDragEnterEvent(event)   
    
    def onDragMoveEvent(self, event):
        self.currentState.onDragMoveEvent(event)            
    
    def onDropEvent(self, event):
        self.currentState.onDropEvent(event)
        
    def scaleView(self, scaleFactor):
        factor = self.gfxPanel.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(-1, -1, 2, 2)).width()

        if factor < 0.07 or factor > 100:
            return

        self.gfxPanel.scale(scaleFactor, scaleFactor)      
        