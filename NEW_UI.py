from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QCompleter, QWidget
from PyQt5.QtCore import Qt, QDir, QSortFilterProxyModel, QRegExp
import sys, re, os, csv
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QGroupBox, QHBoxLayout, QMainWindow, QApplication, QLineEdit, QFileDialog,  QTableWidget,QTableWidgetItem, QTableView, QStyledItemDelegate
import pandas as pd

##################################### Pandas Model Class
class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df.copy()

    def toDataFrame(self):
        return self._df.copy()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending=order ==
                             QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


############################# UI Class
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

        ################################## Validate HSC DATA Button
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_2.clicked.connect(self.HSC_DATA_Validation)
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

        ############################## Export Button
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.exportCSV)
        self.verticalLayout_5.addWidget(self.pushButton_3)
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(10, 470, 201, 41))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        ################################## Reset Button
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.pushButton_4.clicked.connect(self.reset)
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

    # creates a new df from qtables dimensions,
    # copies qtable (data & headers) to the df and returns the df
    def write_qtable_to_df(self):
        global df_, df_OrgHeaders

        col_count = self.filterall.columnCount()
        row_count = self.filterall.rowCount()
        headers = [str(self.filterall.horizontalHeaderItem(i).text()) for i in range(col_count)]

        # df indexing is slow, so use lists
        df_list = []
        for row in range(row_count):
            df_list2 = []
            for col in range(col_count):
                table_item = self.filterall.item(row,col)
                df_list2.append('' if table_item is None else str(table_item.text()))
            df_list.append(df_list2)

        df_ = pd.DataFrame(df_list, columns=headers)
        print(df_)
                # grab the first row for the header
        new_header = df_.iloc[1]

        # set the header row as the df header
        df_.columns = new_header

        #df_.dropna(how='all', axis=1)
        df_.columns = ['col_' + str(index)
                       for index in range(1, len(df_.columns)+1)]
        df_OrgHeaders = df_.iloc[[0, 1]]

        df_.drop(df_.index[[0, 1]], inplace=True)
        return df_

    # 
    def loadFile(self, df_):
        print(df_)
        return df_

    # Validate HSC DATA
    def HSC_DATA_Validation(self, df_):
        global table_result

        df = self.loadFile(df_)
        #df = self.loadFile(df)
        # 4.3 <= 2.1.1.a + 2.1.1.b + 2.2
        def res1(df):
            count = 0
            if float(df['col_74']) > float(df['col_48']) + float(df['col_49']) + float(df['col_52']):
                count = count+1
                return 'Inconsistent'
            elif pd.isnull(df['col_74']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']) and pd.isnull(df['col_52']):
                return 'Blank'
            elif pd.isnull(df['col_74']) or pd.isnull(df['col_48']) or pd.isnull(df['col_49']) or pd.isnull(df['col_52']):
                return 'Blank Error'
            else:
                return 'Consistent'

        # 1.1(col_21) >= 1.1.1(col_22)

        def res2(df):
            if float(df['col_21']) < float(df['col_22']):
                return 'Inconsistent'
            elif pd.isnull(float(df['col_21'])) and pd.isnull(float(df['col_22'])):
                return 'Blank'
            elif pd.isnull(float(df['col_21'])) or pd.isnull(float(df['col_22'])):
                if pd.isnull(df['col_21']):
                    return 'Blank Error (1.1 is blank)'
                elif pd.isnull(df['col_22']):
                    return 'Blank Error (1.1.1 is blank)'
            elif float(df['col_21']) == 0 and float(df['col_22']) == 0:
                return 'consistent'
            else:
                return 'consistent'
            return df

        # 1.3.1.a <= 1.3.1
        def res3(df):
            if float(df['col_32']) > float(df['col_31']):
                return 'Inconsistent because 1.3.1.a <= 1.3.1'
            elif pd.isnull(df['col_32']) and pd.isnull(df['col_31']):
                return 'both 1.3.1.a, 1.3.1 columns are blank, so Invalid'
            elif pd.isnull(df['col_32']):
                return '1.3.1.a is blank, so Invalid'
            elif pd.isnull(df['col_31']):
                return '1.3.1 is blank, so Invalid'
            else:
                return 'Consistent'

        # 1.2.7 <= 1.1

        def res4(df):
            if float(df['col_29']) > float(df['col_21']):
                return 'Inconsistent'
            elif pd.isnull(df['col_29']) and pd.isnull(df['col_21']):
                return 'Blank'
            elif pd.isnull(df['col_29']):
                return 'blank Error'
            elif pd.isnull(df['col_21']):
                return 'blank Error'
            else:
                return 'Consistent'

        # 1.5.1.a <= 1.1
        def res5(df):
            if float(df['col_41']) > float(df['col_21']):
                return 'Inconsistent'
            elif pd.isnull(df['col_41']) and pd.isnull(df['col_21']):
                return 'Blank'
            elif pd.isnull(df['col_41']):
                return 'Blank Error'
            elif pd.isnull(df['col_21']):
                return 'Blank Error'
            else:
                return 'Consistent'

        # 1.5.1.b <= 1.5.1.a
        def res6(df):
            if float(df['col_41']) > float(df['col_42']):
                return 'Inconsistent'
            elif pd.isnull(df['col_41']) and pd.isnull(df['col_42']):
                return 'Blank'
            elif pd.isnull(df['col_41']):
                return 'Blank Error (1.5.1.b is blank)'
            elif pd.isnull(df['col_42']):
                return 'Blank Error (1.5.1.a is blank)'
            else:
                return 'Consistent'

        # 2.1.2 <= 2.1.1.a + 2.1.1.b

        def res7(df):
            if float(df['col_50']) > float(df['col_48']) + float(df['col_49']):
                return 'Inconsistent'
            elif pd.isnull(df['col_50']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']):
                return 'Blank'
            elif pd.isnull(df['col_50']):
                return 'Blank Error (2.1.2 is blank)'
            elif pd.isnull(df['col_48']):
                return 'Blank Error (2.1.1.a is blank)'
            elif pd.isnull(df['col_49']):
                return 'Blank Error (2.1.1.b is blank)'
            else:
                return 'Consistent'

        # 2.1.3 <= 2.1.1.a + 2.1.1.b
        def res9(df):
            if float(df['col_51']) > float(df['col_48']) + float(df['col_49']):
                return 'Inconsistent'
            elif pd.isnull(df['col_51']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']):
                return 'Blank Error'
            elif pd.isnull(df['col_51']):
                return 'Blank Error (2.1.3 is blank)'
            elif pd.isnull(df['col_48']):
                return 'Blank Error (2.1.1.a is blank)'
            elif pd.isnull(df['col_49']):
                return 'Blank Error (2.1.1.a is blank)'
            else:
                return 'Consistent'

        # 2.2.2 <= 2.2
        def res10(df):
            if float(df['col_54']) > float(df['col_52']):
                return 'Inconsistent'
            elif pd.isnull(df['col_54']) and pd.isnull(df['col_52']):
                return 'Blank'
            elif pd.isnull(df['col_52']):
                return 'Blank Error (2.2.2 is blank)'
            elif pd.isnull(df['col_54']):
                return 'Blank Error (2.2 is blank)'
            else:
                return 'Consistent'

        # 4.4 <= 2.1.1.a + 2.1.1.b + 2.2
        def res11(df):
            if float(df['col_75']) > float(df['col_48']) + float(df['col_49']) + float(df['col_52']):
                return 'Inconsistent'
            elif pd.isnull(df['col_75']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']) and pd.isnull(df['col_50']):
                return 'Blank'
            elif pd.isnull(df['col_75']):
                return 'Blank Error (4.4 is blank)'
            elif pd.isnull(df['col_48']):
                return 'Blank Error (2.1.1.a is blank)'
            elif pd.isnull(df['col_49']):
                return 'Blank Error (2.1.1.b is blank)'
            elif pd.isnull(df['col_52']):
                return 'Blank Error (2.2 is blank)'
            else:
                return 'Consistent'

        # 6.1.1 <= 3.1.1.a + 3.1.1.b
        def res12(df):
            if float(df['col_105']) > float(df['col_57']) + float(df['col_58']):
                return 'Inconsistent'
            elif pd.isnull(df['col_105']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'Blank'
            elif pd.isnull(df['col_105']):
                return 'Blank Error (6.1.1 is blank)'
            elif pd.isnull(df['col_57']):
                return 'Blank Error (3.1.1.a is blank)'
            elif pd.isnull(df['col_58']):
                return 'Blank Error (3.1.1.b is blank)'
            else:
                return 'Consistent'

        # 6.1.9 <= 3.1.1.a + 3.1.1.b
        def res13(df):
            if float(df['col_113']) > float(df['col_57']) + float(df['col_58']):
                return 'Inconsistent'
            elif pd.isnull(df['col_113']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'Blank'
            elif pd.isnull(df['col_113']):
                return 'Blank Error (6.1.9 is blank)'
            elif pd.isnull(df['col_57']):
                return 'Blank Error (3.1.1.a is blank)'
            elif pd.isnull(df['col_58']):
                return 'Blank Error (3.1.1.b is blank)'
            else:
                return 'Consistent'

        # 6.1.13 <= 3.1.1.a + 3.1.1.b
        def res14(df):
            if float(df['col_113']) > float(df['col_57']) + float(df['col_58']):
                return 'Inconsistent'
            elif pd.isnull(df['col_113']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'Blank'
            elif pd.isnull(df['col_113']):
                return 'Blank Error (6.1.13 is blank)'
            elif pd.isnull(df['col_57']):
                return 'Blank Error (6.1.13 is blank)'
            elif pd.isnull(df['col_58']):
                return 'Blank Error (6.1.13 is blank)'
            else:
                return 'Consistent'

        # 2.2.1 <= 2.2
        def res15(df):
            if float(df['col_41']) > float(df['col_42']):
                return 'Inconsistent'
            elif pd.isnull(df['col_41']) and pd.isnull(df['col_42']):
                return 'Blank'
            elif pd.isnull(df['col_41']):
                return 'Blank Error (2.2.1 is blank)'
            elif pd.isnull(df['col_42']):
                return 'Blank Error (2.2 is blank)'
            else:
                return 'Consistent'

        # 3.1.2 <= 3.1.1.a + 3.1.1.b
        def res16(df):
            if float(df['col_59']) > float(df['col_57']) + float(df['col_58']):
                return 'Inconsistent'
            elif pd.isnull(df['col_59']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'Blank'
            elif pd.isnull(df['col_59']):
                return 'Blank Error (3.1.2 is blank)'
            elif pd.isnull(df['col_57']):
                return 'Blank Error (3.1.1.a is blank)'
            elif pd.isnull(df['col_58']):
                return 'Blank Error (3.1.1.b is blank)'
            else:
                return 'Consistent'

        # 3.3.1 <= 3.1.1.a + 3.1.1.b
        def res17(df):
            if float(df['col_67']) > float(df['col_57']) + float(df['col_58']):
                return 'Inconsistent'
            elif pd.isnull(df['col_67']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'Blank'
            elif pd.isnull(df['col_67']):
                return 'Blank Error (3.3.1 is blank)'
            elif pd.isnull(df['col_57']):
                return 'Blank Error (3.3.1.a is blank)'
            elif pd.isnull(df['col_58']):
                return 'Blank Error (3.3.1.b is blank)'
            else:
                return 'Consistent'

        # 3.3.2 <= 3.3.1
        def res18(df):
            if float(df['col_68']) > float(df['col_67']):
                return 'Inconsistent'
            elif pd.isnull(df['col_68']) and pd.isnull(df['col_67']):
                return 'Blank'
            elif pd.isnull(df['col_68']):
                return 'Blank Error (3.3.2 is blank)'
            elif pd.isnull(df['col_67']):
                return 'Blank Error (3.3.1 is blank)'
            else:
                return 'Consistent'

        # 4.1 <= 2.1.1.a + 2.1.1.b
        def res19(df):
            if float(df['col_72']) > float(df['col_48']) + float(df['col_49']):
                return 'Inconsistent'
            elif pd.isnull(df['col_72']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']):
                return 'Blank'
            elif pd.isnull(df['col_72']):
                return 'Blank Error (4.1 is blank)'
            elif pd.isnull(df['col_48']):
                return 'Blank Error (2.1.1.a is blank)'
            elif pd.isnull(df['col_49']):
                return 'Blank Error (2.1.1.b is blank)'
            else:
                return 'Consistent'

        # 5.2 <= 2.1.1.a + 2.1.1.b + 2.2
        def res20(df):
            if float(df['col_86']) > float(df['col_48']) + float(df['col_49']) + float(df['col_52']):
                return 'Inconsistent'
            elif pd.isnull(df['col_86']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']) and pd.isnull(df['col_49']):
                return 'Blank'
            elif pd.isnull(df['col_86']):
                return 'Blank Error (5.2 is blank)'
            elif pd.isnull(df['col_48']):
                return 'Blank Error (2.1.1.a is blank)'
            elif pd.isnull(df['col_49']):
                return 'Blank Error (2.1.1.b is blank)'
            elif pd.isnull(df['col_52']):
                return 'Blank Error (2.2 is blank)'
            else:
                return 'Consistent'

        # 4.1 <= 2.1.1.a + 2.1.1.b
        def res21(df):
            if float(df['col_72']) > float(df['col_48']) + float(df['col_49']):
                return 'Inconsistent'
            elif pd.isnull(df['col_72']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']):
                return 'Blank'
            elif pd.isnull(df['col_72']):
                return 'Blank Error (4.1 is blank)'
            elif pd.isnull(df['col_48']):
                return 'Blank Error (2.1.1.a is blank)'
            elif pd.isnull(df['col_49']):
                return 'Blank Error (2.1.1.b is blank)'
            else:
                return 'Consistent'

        # 6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2
        def res22(df):
            if float(df['col_129']) + float(df['col_130']) > float(df['col_126']) + float(df['col_127']):
                return 'Inconsistent'
            elif pd.isnull(df['col_129']) and pd.isnull(df['col_130']) and pd.isnull(df['col_126']) and pd.isnull(df['col_127']):
                return 'Blank'
            elif pd.isnull(df['col_129']):
                return 'Blank Error (6.2.4.a is blank)'
            elif pd.isnull(df['col_130']):
                return 'Blank Error (6.2.4.b is blank)'
            elif pd.isnull(df['col_126']):
                return 'Blank Error (6.2.1 is blank)'
            elif pd.isnull(df['col_127']):
                return 'Blank Error (6.2.2 is blank)'
            else:
                return 'Consistent'

        # 6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4
        def res23(df):
            # if float(df['col_146']) <= float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120'] + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
            if float(df['col_144']) > float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
                return 'Inconsistent'
            elif pd.isnull(df['col_144']) and pd.isnull(df['col_105']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']) and pd.isnull(df['col_111']) and pd.isnull(df['col_112']) and pd.isnull(df['col_113']) and pd.isnull(df['col_114']) and pd.isnull(df['col_115']) and pd.isnull(df['col_116']) and pd.isnull(df['col_117']) and pd.isnull(df['col_118']) and pd.isnull(df['col_119']) and pd.isnull(df['col_120']) and pd.isnull(df['col_121']) and pd.isnull(df['col_122']) and pd.isnull(df['col_123']) and pd.isnull(df['col_124']) and pd.isnull(df['col_125']) and pd.isnull(df['col_126']) and pd.isnull(df['col_127']) and pd.isnull(df['col_128']) and pd.isnull(df['col_131']) and pd.isnull(df['col_132']) and pd.isnull(df['col_133']) and pd.isnull(df['col_134']) and pd.isnull(df['col_135']) and pd.isnull(df['col_136']) and pd.isnull(df['col_137']) and pd.isnull(df['col_138']) and pd.isnull(df['col_139']) and pd.isnull(df['col_140']) and pd.isnull(df['col_141']) and pd.isnull(df['col_142']) and pd.isnull(df['col_143']):
                return 'Blank'
            elif pd.isnull(df['col_144']) or pd.isnull(df['col_105']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']) or pd.isnull(df['col_111']) or pd.isnull(df['col_112']) or pd.isnull(df['col_113']) or pd.isnull(df['col_114']) or pd.isnull(df['col_115']) or pd.isnull(df['col_116']) or pd.isnull(df['col_117']) or pd.isnull(df['col_118']) or pd.isnull(df['col_119']) or pd.isnull(df['col_120']) or pd.isnull(df['col_121']) or pd.isnull(df['col_122']) or pd.isnull(df['col_123']) or pd.isnull(df['col_124']) or pd.isnull(df['col_125']) or pd.isnull(df['col_126']) or pd.isnull(df['col_127']) or pd.isnull(df['col_128']) or pd.isnull(df['col_131']) or pd.isnull(df['col_132']) or pd.isnull(df['col_133']) or pd.isnull(df['col_134']) or pd.isnull(df['col_135']) or pd.isnull(df['col_136']) or pd.isnull(df['col_137']) or pd.isnull(df['col_138']) or pd.isnull(df['col_139']) or pd.isnull(df['col_140']) or pd.isnull(df['col_141']) or pd.isnull(df['col_142']) or pd.isnull(df['col_143']):
                return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_105']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_106']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_107']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_108']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_109']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_110']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_111']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_112']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_113']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_114']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_115']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_116']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_117']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_118']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_119']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_120']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_121']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_122']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_123']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_124']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_125']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_126']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_127']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_128']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_131']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_132']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_133']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_134']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_135']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_136']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_137']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_138']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_139']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_140']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_141']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_142']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_143']):
            #     return 'Blank Error'
            else:
                return 'Consistent'

        # 6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4

        def res24(df):
            # if float(df['col_146']) <= float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120'] + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
            if float(df['col_145']) > float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
                return 'Inconsistent'
            elif pd.isnull(df['col_145']) and pd.isnull(df['col_105']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']) and pd.isnull(df['col_111']) and pd.isnull(df['col_112']) and pd.isnull(df['col_113']) and pd.isnull(df['col_114']) and pd.isnull(df['col_115']) and pd.isnull(df['col_116']) and pd.isnull(df['col_117']) and pd.isnull(df['col_118']) and pd.isnull(df['col_119']) and pd.isnull(df['col_120']) and pd.isnull(df['col_121']) and pd.isnull(df['col_122']) and pd.isnull(df['col_123']) and pd.isnull(df['col_124']) and pd.isnull(df['col_125']) and pd.isnull(df['col_126']) and pd.isnull(df['col_127']) and pd.isnull(df['col_128']) and pd.isnull(df['col_131']) and pd.isnull(df['col_132']) and pd.isnull(df['col_133']) and pd.isnull(df['col_134']) and pd.isnull(df['col_135']) and pd.isnull(df['col_136']) and pd.isnull(df['col_137']) and pd.isnull(df['col_138']) and pd.isnull(df['col_139']) and pd.isnull(df['col_140']) and pd.isnull(df['col_141']) and pd.isnull(df['col_142']) and pd.isnull(df['col_143']):
                return 'Blank'
            elif pd.isnull(df['col_145']) or pd.isnull(df['col_105']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']) or pd.isnull(df['col_111']) or pd.isnull(df['col_112']) or pd.isnull(df['col_113']) or pd.isnull(df['col_114']) or pd.isnull(df['col_115']) or pd.isnull(df['col_116']) or pd.isnull(df['col_117']) or pd.isnull(df['col_118']) or pd.isnull(df['col_119']) or pd.isnull(df['col_120']) or pd.isnull(df['col_121']) or pd.isnull(df['col_122']) or pd.isnull(df['col_123']) or pd.isnull(df['col_124']) or pd.isnull(df['col_125']) or pd.isnull(df['col_126']) or pd.isnull(df['col_127']) or pd.isnull(df['col_128']) or pd.isnull(df['col_131']) or pd.isnull(df['col_132']) or pd.isnull(df['col_133']) or pd.isnull(df['col_134']) or pd.isnull(df['col_135']) or pd.isnull(df['col_136']) or pd.isnull(df['col_137']) or pd.isnull(df['col_138']) or pd.isnull(df['col_139']) or pd.isnull(df['col_140']) or pd.isnull(df['col_141']) or pd.isnull(df['col_142']) or pd.isnull(df['col_143']):
                return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_105']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_106']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_107']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_108']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_109']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_110']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_111']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_112']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_113']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_114']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_115']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_116']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_117']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_118']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_119']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_120']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_121']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_122']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_123']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_124']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_125']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_126']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_127']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_128']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_131']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_132']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_133']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_134']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_135']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_136']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_137']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_138']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_139']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_140']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_141']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_142']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_143']):
            #     return 'Blank Error'
            else:
                return 'Consistent'

        # 6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4

        def res25(df):
            # if float(df['col_146']) <= float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120'] + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
            if float(df['col_146']) > float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
                return 'Inconsistent'
            elif pd.isnull(df['col_146']) and pd.isnull(df['col_105']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']) and pd.isnull(df['col_111']) and pd.isnull(df['col_112']) and pd.isnull(df['col_113']) and pd.isnull(df['col_114']) and pd.isnull(df['col_115']) and pd.isnull(df['col_116']) and pd.isnull(df['col_117']) and pd.isnull(df['col_118']) and pd.isnull(df['col_119']) and pd.isnull(df['col_120']) and pd.isnull(df['col_121']) and pd.isnull(df['col_122']) and pd.isnull(df['col_123']) and pd.isnull(df['col_124']) and pd.isnull(df['col_125']) and pd.isnull(df['col_126']) and pd.isnull(df['col_127']) and pd.isnull(df['col_128']) and pd.isnull(df['col_131']) and pd.isnull(df['col_132']) and pd.isnull(df['col_133']) and pd.isnull(df['col_134']) and pd.isnull(df['col_135']) and pd.isnull(df['col_136']) and pd.isnull(df['col_137']) and pd.isnull(df['col_138']) and pd.isnull(df['col_139']) and pd.isnull(df['col_140']) and pd.isnull(df['col_141']) and pd.isnull(df['col_142']) and pd.isnull(df['col_143']):
                return 'Blank'
            elif pd.isnull(df['col_146']) or pd.isnull(df['col_105']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']) or pd.isnull(df['col_111']) or pd.isnull(df['col_112']) or pd.isnull(df['col_113']) or pd.isnull(df['col_114']) or pd.isnull(df['col_115']) or pd.isnull(df['col_116']) or pd.isnull(df['col_117']) or pd.isnull(df['col_118']) or pd.isnull(df['col_119']) or pd.isnull(df['col_120']) or pd.isnull(df['col_121']) or pd.isnull(df['col_122']) or pd.isnull(df['col_123']) or pd.isnull(df['col_124']) or pd.isnull(df['col_125']) or pd.isnull(df['col_126']) or pd.isnull(df['col_127']) or pd.isnull(df['col_128']) or pd.isnull(df['col_131']) or pd.isnull(df['col_132']) or pd.isnull(df['col_133']) or pd.isnull(df['col_134']) or pd.isnull(df['col_135']) or pd.isnull(df['col_136']) or pd.isnull(df['col_137']) or pd.isnull(df['col_138']) or pd.isnull(df['col_139']) or pd.isnull(df['col_140']) or pd.isnull(df['col_141']) or pd.isnull(df['col_142']) or pd.isnull(df['col_143']):
                return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_105']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_106']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_107']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_108']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_109']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_110']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_111']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_112']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_113']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_114']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_115']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_116']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_117']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_118']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_119']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_120']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_121']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_122']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_123']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_124']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_125']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_126']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_127']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_128']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_131']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_132']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_133']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_134']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_135']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_136']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_137']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_138']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_139']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_140']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_141']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_142']):
            #     return 'Blank Error'
            # elif pd.isnull(df['col_146']) and pd.isnull(df['col_143']):
            #     return 'Blank Error'
            else:
                return 'Consistent'

        # 6.7.3<=6.7.2
        def res26(df):
            if float(df['col_149']) > float(df['col_148']):
                return 'Inconsistent'
            elif pd.isnull(df['col_148']) and pd.isnull(df['col_149']):
                return 'Blank'
            elif pd.isnull(df['col_148']):
                return 'Blank Error (6.7.3 is blank)'
            elif pd.isnull(df['col_149']):
                return 'Blank Error (6.7.2 is blank)'
            else:
                return 'Consistent'

        # 10.1.2<=10.1.1
        def res27(df):
            if float(df['col_250']) > float(df['col_249']):
                return 'Inconsistent'
            elif pd.isnull(df['col_250']) and pd.isnull(df['col_249']):
                return 'Blank'
            elif pd.isnull(df['col_250']):
                return 'Blank Error (10.1.2 is blank)'
            elif pd.isnull(df['col_249']):
                return 'Blank Error (10.1.1 is blank)'
            else:
                return 'Consistent'

        # 10.2.1.b<=10.2.1.a
        def res28(df):
            if float(df['col_256']) > float(df['col_255']):
                return 'Inconsistent'
            elif pd.isnull(df['col_256']) and pd.isnull(df['col_255']):
                return 'Blank'
            elif pd.isnull(df['col_256']):
                return 'Blank Error (10.2.1.b is blank)'
            elif pd.isnull(df['col_255']):
                return 'Blank Error (10.2.1.a is blank)'
            else:
                return 'Consistent'

        # 3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2
        def res29(df):
            if float(df['col_57']) + float(df['col_58']) + float(df['col_60']) < float(df['col_48']) + float(df['col_49']) + float(df['col_52']):
                return 'Inconsistent'
            elif pd.isnull(df['col_57']) and pd.isnull(df['col_58']) and pd.isnull(df['col_60']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']) and pd.isnull(df['col_52']):
                return 'Blank'
            elif pd.isnull(df['col_57']):
                return 'Blank Error (3.1.1.a is blank)'
            elif pd.isnull(df['col_58']):
                return 'Blank Error (3.1.1.b is blank)'
            elif pd.isnull(df['col_60']):
                return 'Blank Error (3.1.3 is blank)'
            elif pd.isnull(df['col_48']):
                return 'Blank Error (2.1.1.a is blank)'
            elif pd.isnull(df['col_49']):
                return 'Blank Error (2.1.1.b is blank)'
            elif pd.isnull(df['col_52']):
                return 'Blank Error (2.2 is blank)'
            else:
                return 'Consistent'

        # 8.1.1.c<=8.1.1.a
        def res30(df):
            if float(df['col_175']) > float(df['col_173']):
                return 'Inconsistent'
            elif pd.isnull(df['col_175']) and pd.isnull(df['col_173']):
                return 'Blank'
            elif pd.isnull(df['col_175']):
                return 'Blank Error (8.1.1.c is blank)'
            elif pd.isnull(df['col_173']):
                return 'Blank Error (8.1.1.a is blank)'
            else:
                return 'Consistent'

        # 9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8
        def res31(df):
            if float(df['col_200']) + float(df['col_201']) < float(df['col_191']) + float(df['col_192']) + float(df['col_193']) + float(df['col_194']) + float(df['col_195']) + float(df['col_196']) + float(df['col_197']) + float(df['col_198']):
                return 'Inconsistent'
            elif pd.isnull(df['col_200']) and pd.isnull(df['col_201']) and pd.isnull(df['col_191']) and pd.isnull(df['col_192']) and pd.isnull(df['col_193']) and pd.isnull(df['col_194']) and pd.isnull(df['col_195']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']):
                return 'Blank'
            elif pd.isnull(df['col_200']):
                return 'Blank Error (9.2.1 is blank)'
            elif pd.isnull(df['col_201']):
                return 'Blank Error (9.2.2 is blank)'
            elif pd.isnull(df['col_191']):
                return 'Blank Error (9.1.1 is blank)'
            elif pd.isnull(df['col_192']):
                return 'Blank Error (9.1.2 is blank)'
            elif pd.isnull(df['col_193']):
                return 'Blank Error (9.1.3 is blank)'
            elif pd.isnull(df['col_194']):
                return 'Blank Error (9.1.4 is blank)'
            elif pd.isnull(df['col_195']):
                return 'Blank Error (9.1.5 is blank)'
            elif pd.isnull(df['col_196']):
                return 'Blank Error (9.1.6 is blank)'
            elif pd.isnull(df['col_197']):
                return 'Blank Error (9.1.7 is blank)'
            elif pd.isnull(df['col_198']):
                return 'Blank Error (9.1.8 is blank)'
            else:
                return 'Consistent'

        # 8.1.1.b<=8.1.1.a

        def res32(df):
            if float(df['col_174']) > float(df['col_173']):
                return 'Inconsistent'
            elif pd.isnull(df['col_174']) and pd.isnull(df['col_173']):
                return 'Blank'
            elif pd.isnull(df['col_174']):
                return 'Blank Error (8.1.1.b is blank)'
            elif pd.isnull(df['col_173']):
                return 'Blank Error (8.1.1.a is blank)'
            else:
                return 'Consistent'

        df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res1, axis=1)
        count_condition_1_consistent = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Consistent").sum()
        count_condition_1_inconsistent = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Inconsistent").sum()
        count_condition_1_blank = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Blank").sum()
        count_condition_1_blank_error = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Blank Error").sum()
            

        df['1.1 >= 1.1.1'] = df.apply(res2, axis=1)
        count_condition_2_consistent = df['1.1 >= 1.1.1'].str.count(
            "Consistent").sum()
        count_condition_2_inconsistent = df['1.1 >= 1.1.1'].str.count(
            "Inconsistent").sum()
        count_condition_2_blank = df['1.1 >= 1.1.1'].str.count("Blank").sum()
        count_condition_2_blank_error = df['1.1 >= 1.1.1'].str.count(
            "Blank Error").sum()

        df['1.3.1.a <= 1.3.1'] = df.apply(res3, axis=1)
        count_condition_3_consistent = df['1.3.1.a <= 1.3.1'].str.count(
            "Consistent").sum()
        count_condition_3_inconsistent = df['1.3.1.a <= 1.3.1'].str.count(
            "Inconsistent").sum()
        count_condition_3_blank = df['1.3.1.a <= 1.3.1'].str.count(
            "Blank").sum()
        count_condition_3_blank_error = df['1.3.1.a <= 1.3.1'].str.count(
            "Blank Error").sum()

        df['1.2.7 <= 1.1'] = df.apply(res4, axis=1)
        count_condition_4_consistent = df['1.2.7 <= 1.1'].str.count(
            "Consistent").sum()
        count_condition_4_inconsistent = df['1.2.7 <= 1.1'].str.count(
            "Inconsistent").sum()
        count_condition_4_blank = df['1.2.7 <= 1.1'].str.count("Blank").sum()
        count_condition_4_blank_error = df['1.2.7 <= 1.1'].str.count(
            "Blank Error").sum()

        df['1.5.1.a <= 1.1'] = df.apply(res5, axis=1)
        count_condition_5_consistent = df['1.5.1.a <= 1.1'].str.count(
            "Consistent").sum()
        count_condition_5_inconsistent = df['1.5.1.a <= 1.1'].str.count(
            "Inconsistent").sum()
        count_condition_5_blank = df['1.5.1.a <= 1.1'].str.count("Blank").sum()
        count_condition_5_blank_error = df['1.5.1.a <= 1.1'].str.count(
            "Blank Error").sum()

        df['1.5.1.b <= 1.5.1.a'] = df.apply(res6, axis=1)
        count_condition_6_consistent = df['1.5.1.b <= 1.5.1.a'].str.count(
            "Consistent").sum()
        count_condition_6_inconsistent = df['1.5.1.b <= 1.5.1.a'].str.count(
            "Inconsistent").sum()
        count_condition_6_blank = df['1.5.1.b <= 1.5.1.a'].str.count(
            "Blank").sum()
        count_condition_6_blank_error = df['1.5.1.b <= 1.5.1.a'].str.count(
            "Blank Error").sum()

        df['2.1.2 <= 2.1.1.a + 2.1.1.b'] = df.apply(res7, axis=1)
        #df['validity_check_8'] = df.apply(res8, axis = 1)
        df['2.1.3 <= 2.1.1.a + 2.1.1.b'] = df.apply(res9, axis=1)
        df['2.2.2 <= 2.2'] = df.apply(res10, axis=1)
        df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res11, axis=1)
        df['6.1.1 <= 3.1.1.a + 3.1.1.b'] = df.apply(res12, axis=1)
        df['6.1.9 <= 3.1.1.a + 3.1.1.b'] = df.apply(res13, axis=1)
        df['6.1.13 <= 3.1.1.a + 3.1.1.b'] = df.apply(res14, axis=1)
        df['2.2.1 <= 2.2'] = df.apply(res15, axis=1)
        df['3.1.2 <= 3.1.1.a + 3.1.1.b'] = df.apply(res16, axis=1)
        df['3.3.1 <= 3.1.1.a + 3.1.1.b'] = df.apply(res17, axis=1)
        df['3.3.2 <= 3.3.1'] = df.apply(res18, axis=1)
        df['4.1 <= 2.1.1.a + 2.1.1.b'] = df.apply(res19, axis=1)
        df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res20, axis=1)
        df['4.1 <= 2.1.1.a + 2.1.1.b'] = df.apply(res21, axis=1)
        df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'] = df.apply(res22, axis=1)
        df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(
            res23, axis=1)
        df['6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(
            res24, axis=1)
        df['6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(
            res25, axis=1)
        df['6.7.3<=6.7.2'] = df.apply(res26, axis=1)
        df['10.1.2<=10.1.1'] = df.apply(res27, axis=1)
        df['10.2.1.b<=10.2.1.a'] = df.apply(res28, axis=1)
        df['3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2'] = df.apply(
            res29, axis=1)
        df['8.1.1.c<=8.1.1.a'] = df.apply(res30, axis=1)
        df['9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8'] = df.apply(
            res31, axis=1)
        df['8.1.1.b<=8.1.1.a'] = df.apply(res32, axis=1)

        df = pd.concat([df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'],
                        df['1.1 >= 1.1.1'],
                        df['1.3.1.a <= 1.3.1'],
                        df['1.2.7 <= 1.1'],
                        df['1.5.1.a <= 1.1'],
                        df['1.5.1.b <= 1.5.1.a'],
                        df['2.1.2 <= 2.1.1.a + 2.1.1.b'],
                        df['2.1.3 <= 2.1.1.a + 2.1.1.b'],
                        df['2.2.2 <= 2.2'],
                        df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'],
                        df['6.1.1 <= 3.1.1.a + 3.1.1.b'],
                        df['6.1.9 <= 3.1.1.a + 3.1.1.b'],
                        df['6.1.13 <= 3.1.1.a + 3.1.1.b'],
                        df['2.2.1 <= 2.2'],
                        df['3.1.2 <= 3.1.1.a + 3.1.1.b'],
                        df['3.3.1 <= 3.1.1.a + 3.1.1.b'],
                        df['3.3.2 <= 3.3.1'],
                        df['4.1 <= 2.1.1.a + 2.1.1.b'],
                        df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'],
                        df['4.1 <= 2.1.1.a + 2.1.1.b'],
                        df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'],
                        df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'],
                        df['6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'],
                        df['6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'],
                        df['6.7.3<=6.7.2'],
                        df['10.1.2<=10.1.1'],
                        df['10.2.1.b<=10.2.1.a'],
                        df['3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2'],
                        df['8.1.1.c<=8.1.1.a'],
                        df['9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8'],
                        df['8.1.1.b<=8.1.1.a']], axis=1)

        # merging dataframes
        frames = [df_OrgHeaders, df]
        df = pd.concat(frames, sort=False)

        # type conversion of dataframe
        df.astype(str)

        # Applying conditionals
        # Print table
        table_result = pd.DataFrame({"Conditions": ["4.3 <= 2.1.1.a + 2.1.1.b + 2.2", "1.1 >= 1.1.1", "1.3.1.a <= 1.3.1", "1.2.7 <= 1.1", "1.5.1.a <= 1.1", "1.5.1.b <= 1.5.1.a", "Total count"], "Consistent": [count_condition_1_consistent, count_condition_2_consistent, count_condition_3_consistent, count_condition_4_consistent, count_condition_5_consistent, count_condition_6_consistent, (count_condition_1_consistent+count_condition_2_consistent+count_condition_3_consistent+count_condition_4_consistent+count_condition_5_consistent+count_condition_6_consistent)], "Inconsistent": [count_condition_1_inconsistent, count_condition_2_inconsistent, count_condition_3_inconsistent, count_condition_4_inconsistent, count_condition_5_inconsistent, count_condition_6_inconsistent, (count_condition_1_inconsistent+count_condition_2_inconsistent +
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         count_condition_3_inconsistent+count_condition_4_inconsistent+count_condition_5_inconsistent+count_condition_6_inconsistent)], "Blank": [count_condition_1_blank, count_condition_2_blank, count_condition_3_blank, count_condition_4_blank, count_condition_5_blank, count_condition_6_blank, (count_condition_1_blank+count_condition_2_blank+count_condition_3_blank+count_condition_4_blank+count_condition_5_blank+count_condition_6_blank)], "Blank Error": [count_condition_1_blank_error, count_condition_2_blank_error, count_condition_3_blank_error, count_condition_4_blank_error, count_condition_5_blank_error, count_condition_6_blank_error, (count_condition_1_blank_error+count_condition_2_blank_error+count_condition_3_blank_error+count_condition_4_blank_error+count_condition_5_blank_error+count_condition_6_blank_error)]})
                
        self.model = PandasModel(df)
        self.filterall.setModel(self.model)

        msg = QMessageBox()
        msg.setWindowTitle("Result")
        msg.setText("HSC Data validation is Complete ...!")
        msg.exec()

        return df, table_result

    # Export df and summary report to csv
    def exportCSV(self): 
        filename = QFileDialog.getSaveFileName(Dialog, "Save to CSV", "table.csv",
                                               "Comma Separated Values Spreadsheet (*.csv);;"
                                               "All Files (*)")[0]
        filename = filename + ".csv"
        df.to_csv(filename, index=False)

        filename1 = filename + ' Summary_Report ' + '.csv'
        table_result.to_csv(filename1, index=False)

    # Reset button functionality
    def reset(self):
        self.lineEdit.clear()
        self.filterall.clearSpans()
        
        #self.comboBox.clear()
        self.filterall.reset()
        self.isChanged = True
        
        msg = QMessageBox()
        msg.setWindowTitle(" Reset Result")
        msg.setText("reset data is successful!")
        msg.exec()
        self.pushButton.setEnabled(True)   

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
