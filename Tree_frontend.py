# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tree.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Tree_window(object):
    def setupUi(self, Tree_window):
        Tree_window.setObjectName("Tree_window")
        Tree_window.resize(920, 597)
        Tree_window.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0.21, x2:1, y2:1, stop:0 rgba(0, 150, 255, 248), stop:0.243094 rgba(0, 150, 255, 226), stop:1 rgba(255, 255, 255, 255));")
        self.centralwidget = QtWidgets.QWidget(Tree_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 791, 541))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        Tree_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Tree_window)
        self.statusbar.setObjectName("statusbar")
        Tree_window.setStatusBar(self.statusbar)

        self.retranslateUi(Tree_window)
        QtCore.QMetaObject.connectSlotsByName(Tree_window)

    def retranslateUi(self, Tree_window):
        _translate = QtCore.QCoreApplication.translate
        Tree_window.setWindowTitle(_translate("Tree_window", "MainWindow"))
        self.label.setText(_translate("Tree_window", "Tree"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Tree_window = QtWidgets.QMainWindow()
    ui = Ui_Tree_window()
    ui.setupUi(Tree_window)
    Tree_window.show()
    sys.exit(app.exec_())