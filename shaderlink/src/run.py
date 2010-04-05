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
from gui.mainwindow import MainWindow

if __name__ == '__main__':  
    app = QtGui.QApplication(sys.argv)

    # used by QSettings to store in registry (windows) or home (linux)
    app.setOrganizationName('Libero')
    app.setOrganizationDomain('Spagnolini')
    app.setApplicationName("Shaderlink")
    app.setWindowIcon(QtGui.QIcon(':/shaderLink.png'))

    form = MainWindow()    
    #form.resize(QtCore.QSize(1200, 900))
    form.showMaximized()
    form.show()   
    sys.exit(app.exec_())