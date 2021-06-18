import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from form import spero

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainUI = spero()
    sys.exit(app.exec_())