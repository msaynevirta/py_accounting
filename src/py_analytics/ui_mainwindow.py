# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 666)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 666))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.home = QtWidgets.QWidget()
        self.home.setObjectName("home")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.home)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_load = QtWidgets.QPushButton(self.home)
        self.btn_load.setMinimumSize(QtCore.QSize(200, 50))
        self.btn_load.setObjectName("btn_load")
        self.horizontalLayout.addWidget(self.btn_load, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.stackedWidget.addWidget(self.home)
        self.analytics = QtWidgets.QWidget()
        self.analytics.setObjectName("analytics")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.analytics)
        self.verticalLayout.setObjectName("verticalLayout")
        self.block_bar = QtWidgets.QStackedWidget(self.analytics)
        self.block_bar.setObjectName("block_bar")
        self.block_diagram = QtWidgets.QWidget()
        self.block_diagram.setObjectName("block_diagram")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.block_diagram)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.v_block_diagram = QtWidgets.QGraphicsView(self.block_diagram)
        self.v_block_diagram.setObjectName("v_block_diagram")
        self.horizontalLayout_3.addWidget(self.v_block_diagram)
        self.block_bar.addWidget(self.block_diagram)
        self.bar_diagram = QtWidgets.QWidget()
        self.bar_diagram.setObjectName("bar_diagram")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.bar_diagram)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.v_bar_chart = QChartView(self.bar_diagram)
        self.v_bar_chart.setObjectName("v_bar_chart")
        self.horizontalLayout_4.addWidget(self.v_bar_chart)
        self.block_bar.addWidget(self.bar_diagram)
        self.verticalLayout.addWidget(self.block_bar)
        self.qtcharts = QtWidgets.QHBoxLayout()
        self.qtcharts.setObjectName("qtcharts")
        self.v_method_pie = QChartView(self.analytics)
        self.v_method_pie.setObjectName("v_method_pie")
        self.qtcharts.addWidget(self.v_method_pie)
        self.v_cumulative_expenses = QChartView(self.analytics)
        self.v_cumulative_expenses.setObjectName("v_cumulative_expenses")
        self.qtcharts.addWidget(self.v_cumulative_expenses)
        self.verticalLayout.addLayout(self.qtcharts)
        self.stackedWidget.addWidget(self.analytics)
        self.verticalLayout_2.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_files = QtWidgets.QAction(MainWindow)
        self.actionOpen_files.setObjectName("actionOpen_files")
        self.menuFile.addAction(self.actionOpen_files)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        self.block_bar.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Transaction analytics"))
        self.btn_load.setText(_translate("MainWindow", "Select transaction files"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_files.setText(_translate("MainWindow", "Open files..."))
from PyQt5.QtChart import QChartView
