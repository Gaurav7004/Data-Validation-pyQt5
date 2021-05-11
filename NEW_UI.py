from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QCompleter, QWidget
from PyQt5.QtCore import Qt, QDir, QSortFilterProxyModel, QRegExp
import sys, re, os, csv
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QGroupBox, QHBoxLayout, QMainWindow, QApplication, QLineEdit, QFileDialog,  QTableWidget,QTableWidgetItem, QTableView, QStyledItemDelegate
import pandas as pd


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1678, 977)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 290, 201, 40))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        ###################################################################
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.clicked.connect(self.loadAll)

        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(220, 20, 1441, 40))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(220, 60, 1441, 40))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_3.addWidget(self.lineEdit_2)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(220, 100, 1441, 861))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        ############## tableView
        self.filterall = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.filterall.setColumnCount(0)
        self.filterall.setRowCount(0)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.horizontalHeader = self.filterall.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked)
        self.checkBoxs = []
        self.col = None
        self.filterall.setFont(font)
        self.filterall.setObjectName("tableView")
        ##########################################

        self.gridLayout.addWidget(self.filterall, 0, 1, 1, 1)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 350, 201, 40))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_4.addWidget(self.pushButton_2)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 410, 201, 41))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_5.addWidget(self.pushButton_3)
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(10, 470, 201, 41))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_6.addWidget(self.pushButton_4)
        self.gridLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(60, 20, 117, 144))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("../../../../Pictures/74067_web (2).jpg"))
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Upload"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "Search..."))
        self.pushButton_2.setText(_translate("Dialog", "Validate HSC Data"))
        self.pushButton_3.setText(_translate("Dialog", "Export"))
        self.pushButton_4.setText(_translate("Dialog", "Reset"))

    def slotSelect(self, state):
        for checkbox in self.checkBoxs:
            checkbox.setChecked(QtCore.Qt.Checked == state)

    def on_view_horizontalHeader_sectionClicked(self, index):
        # self.clearFilter()
        self.menu = QtWidgets.QMenu(Dialog)
        font = self.menu.font()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.menu.setFont(font)

        self.col = index

        data_unique = []

        self.checkBoxs = []

        checkBox = QtWidgets.QCheckBox("Select all", self.menu)
        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(checkBox)
        self.menu.addAction(checkableAction)
        checkBox.setChecked(True)
        checkBox.stateChanged.connect(self.slotSelect)

        for i in range(self.filterall.rowCount()):
            if not self.filterall.isRowHidden(i):
                item = self.filterall.item(i, index)
                if item.text() not in data_unique:
                    data_unique.append(item.text())
                    checkBox = QtWidgets.QCheckBox(item.text(), self.menu)
                    checkBox.setChecked(True)
                    checkableAction = QtWidgets.QWidgetAction(self.menu)
                    checkableAction.setDefaultWidget(checkBox)
                    self.menu.addAction(checkableAction)
                    self.checkBoxs.append(checkBox)

        btn = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
                                     QtCore.Qt.Horizontal, self.menu)
        btn.accepted.connect(self.menuClose)
        btn.rejected.connect(self.menu.close)
        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)

        headerPos = self.filterall.mapToGlobal(self.horizontalHeader.pos())

        posY = headerPos.y() + self.horizontalHeader.height()
        posX = headerPos.x() + self.horizontalHeader.sectionPosition(index)
        self.menu.exec_(QtCore.QPoint(posX, posY))

    def menuClose(self):
        self.keywords[self.col] = []
        for element in self.checkBoxs:
            if element.isChecked():
                self.keywords[self.col].append(element.text())
        self.filterdata()
        self.menu.close()

    def loadAll(self):
        #global df_, df_OrgHeaders
        fileName, _ = QFileDialog.getOpenFileName(Dialog , "Open CSV",(QtCore.QDir.homePath()), "CSV (*.csv)")
        self.lineEdit.setText(fileName)

        with open(fileName, "r+") as inpfil:
            reader = csv.reader(inpfil, delimiter=',')
            csheader = next(reader)
            ncol = len(csheader)
            data = list(reader)
            row_count = len(data)

            self.filterall.setRowCount(row_count)
            self.filterall.setColumnCount(ncol)
            self.filterall.setHorizontalHeaderLabels(('%s' % ', '.join(map(str, csheader))).split(","))

            for ii in range(0, row_count):
                mainins = data[ii]
                for var in range(0, ncol):
                    self.filterall.setItem(ii, var, QtWidgets.QTableWidgetItem(mainins[var]))

        self.keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        #return keywords

    def clearFilter(self):
        for i in range(self.filterall.rowCount()):
            self.filterall.setRowHidden(i, False)

    def filterdata(self):
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(self.filterall.rowCount())])
        
        for i in range(self.filterall.rowCount()):  
            for j in range(self.filterall.columnCount()):
                item = self.filterall.item(i, j)
                if self.keywords[j]:
                    if item.text() not in self.keywords[j]:
                        columnsShow[i] = False

        for key, value in columnsShow.items():
            self.filterall.setRowHidden(key, not value)

###################################################### main function #######################################

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
