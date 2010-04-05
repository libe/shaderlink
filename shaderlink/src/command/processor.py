##################################################################################
#
#  Shaderlink - A RenderMan Shader Authoring Toolkit 
#  http://libe.ocracy.org/shaderlink.html
#  2010 Libero Spagnolini (libero.spagnolini@gmail.com)
#
##################################################################################

from PyQt4 import QtCore

class CommandProcessor(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.doneCommandsStack = []
        self.unDoneCommandsStack = []
        
        self.copyCommand = None
        
    def executeCommand(self, command):
        # execute the command
        command.do()

        # fire dirty state update
        changeDirtyState, dirtyStateValue = command.invalidateDirtyState()
        if changeDirtyState:
            self.emit(QtCore.SIGNAL('dirtyStateChanged'), dirtyStateValue)

        # set up undo and redo stacks
        from command import Command
        if command.type == Command.Normal:
            self.doneCommandsStack.append(command)            
        elif command.type == Command.NoUndo:
            pass
        elif command.type == Command.ResetUndoRedo:
            self.doneCommandsStack = []
            self.unDoneCommandsStack = []
        elif command.type == Command.ResetRedo:
            self.doneCommandsStack.append(command)
        else:
            assert 0, 'Unknown command!'

        self.emit(QtCore.SIGNAL('commandExecuted'))
            
        print 'done stack:', self.doneCommandsStack 
        print 'undone stack:', self.unDoneCommandsStack
                                
    def undoLastCommand(self):
        if self.doneCommandsStack == []:
            return
        
        # pop last done command
        lastCommand = self.doneCommandsStack.pop()
        
        # undo it
        lastCommand.undo()
        
        # store for later redo
        self.unDoneCommandsStack.append(lastCommand)
    
    def redoLastUndoneCommand(self):
        if self.unDoneCommandsStack == []:
            return

        # pop last undone command
        lastRedoCommand =self.unDoneCommandsStack.pop()
        
        # redo it
        lastRedoCommand.redo()
        
        # store for later undo
        self.doneCommandsStack.append(lastRedoCommand)
        
    def setCopyCommand(self, command):
        self.copyCommand = command
        
        self.emit(QtCore.SIGNAL('copyCommandChanged'), self.copyCommand)
