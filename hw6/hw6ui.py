# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hw6.ui'
#
# Created: Sun Mar 18 15:01:33 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import matplotlib
matplotlib.rcParams['backend.qt4']='PySide'

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(771, 603)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.search = QtGui.QLineEdit(self.centralwidget)
        self.search.setObjectName(_fromUtf8("search"))
        self.horizontalLayout_2.addWidget(self.search)
        self.searchbutton = QtGui.QPushButton(self.centralwidget)
        self.searchbutton.setObjectName(_fromUtf8("searchbutton"))
        self.horizontalLayout_2.addWidget(self.searchbutton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.urllabel = QtGui.QLabel(self.centralwidget)
        self.urllabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.urllabel.setText(_fromUtf8(""))
        self.urllabel.setObjectName(_fromUtf8("urllabel"))
        self.verticalLayout.addWidget(self.urllabel)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.rotate = QtGui.QPushButton(self.centralwidget)
        self.rotate.setObjectName(_fromUtf8("rotate"))
        self.horizontalLayout.addWidget(self.rotate)
        self.blur = QtGui.QPushButton(self.centralwidget)
        self.blur.setObjectName(_fromUtf8("blur"))
        self.horizontalLayout.addWidget(self.blur)
        self.filter = QtGui.QPushButton(self.centralwidget)
        self.filter.setObjectName(_fromUtf8("filter"))
        self.horizontalLayout.addWidget(self.filter)
        self.invert = QtGui.QPushButton(self.centralwidget)
        self.invert.setObjectName(_fromUtf8("invert"))
        self.horizontalLayout.addWidget(self.invert)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 771, 29))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "search query:", None, QtGui.QApplication.UnicodeUTF8))
        self.searchbutton.setText(QtGui.QApplication.translate("MainWindow", "search", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "image url:", None, QtGui.QApplication.UnicodeUTF8))
        self.rotate.setText(QtGui.QApplication.translate("MainWindow", "rotate", None, QtGui.QApplication.UnicodeUTF8))
        self.blur.setText(QtGui.QApplication.translate("MainWindow", "blur", None, QtGui.QApplication.UnicodeUTF8))
        self.filter.setText(QtGui.QApplication.translate("MainWindow", "filter", None, QtGui.QApplication.UnicodeUTF8))
        self.invert.setText(QtGui.QApplication.translate("MainWindow", "invert", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Ok", None, QtGui.QApplication.UnicodeUTF8))

