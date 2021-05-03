import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QCompleter
from PyQt5.QtCore import Qt, QDir
import sys, re, os, csv
#import xlsxwriter

#--------------------------------------------------- Pandas Model ------------------------------------------
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
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

###################
class ExtendedComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QtCore.QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox 
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))


    # on model change, update the models of the filter and completer as well 
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)    


#--------------------------------------------------- Checkable Pandas Model  ------------------------------
class CheckablePandasModel(PandasModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(df, parent)
        self.checkable_values = set()
        self._checkable_column = -1

    @property
    def checkable_column(self):
        return self._checkable_column

    @checkable_column.setter
    def checkable_column(self, column):
        if self.checkable_column == column:
            return
        last_column = self.checkable_column
        self._checkable_column = column

        if last_column == -1:
            self.beginInsertColumns(
                QtCore.QModelIndex(), self.checkable_column, self.checkable_column
            )
            self.endInsertColumns()

        elif self.checkable_column == -1:
            self.beginRemoveColumns(QtCore.QModelIndex(), last_column, last_column)
            self.endRemoveColumns()
        for c in (last_column, column):
            if c > 0:
                self.dataChanged.emit(
                    self.index(0, c), self.index(self.columnCount() - 1, c)
                )

    def columnCount(self, parent=QtCore.QModelIndex()):
        return super().columnCount(parent) + (1 if self.checkable_column != -1 else 0)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if self.checkable_column != -1:
            row, col = index.row(), index.column()
            if col == self.checkable_column:
                if role == QtCore.Qt.CheckStateRole:
                    return (
                        QtCore.Qt.Checked
                        if row in self.checkable_values
                        else QtCore.Qt.Unchecked
                    )
                return QtCore.QVariant()
            if col > self.checkable_column:
                index = index.sibling(index.row(), col - 1)
        return super().data(index, role)

    def setData(self, index, value, role):
        if self.checkable_column != -1:
            row, col = index.row(), index.column()
            if col == self.checkable_column:
                if role == QtCore.Qt.CheckStateRole:
                    if row in self.checkable_values:
                        self.checkable_values.discard(row)
                    else:
                        self.checkable_values.add(row)
                    self.dataChanged.emit(index, index, (role,))
                    return True
                return False
            if col > self.checkable_column:
                index = index.sibling(index.row(), col - 1)
        return super().setData(index, value, role)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if self.checkable_column != -1:
            if section == self.checkable_column and orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant()
            if section > self.checkable_column and orientation == QtCore.Qt.Horizontal:
                section -= 1
        return super().headerData(section, orientation, role)

    def flags(self, index):
        if self.checkable_column != -1:
            col = index.column()
            if col == self.checkable_column:
                return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled
            if col > self.checkable_column:
                index = index.sibling(index.row(), col - 1)
        return super().flags(index)

#=========================================================== Main Window =========================================================

class CustomProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self._filters = dict()

    @property
    def filters(self):
        return self._filters

    def setFilter(self, expresion, column):
        if expresion:
            self.filters[column] = expresion
        elif column in self.filters:
            del self.filters[column]
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        for column, expresion in self.filters.items():
            text = self.sourceModel().index(source_row, column, source_parent).data()
            regex = QtCore.QRegExp(
                expresion, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp
            )
            if regex.indexIn(text) == -1:
                return False
        return True


#========================================================================
class Ui_Form(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(Dialog)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1462, 913)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 250, 201, 40))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        #-------------------------------------------------- Upload Button
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.upload)
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(220, 20, 1231, 40))
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
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(220, 60, 1231, 40))
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
        self.gridLayoutWidget.setGeometry(QtCore.QRect(220, 100, 1231, 801))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.tableView.setFont(font)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 300, 201, 40))
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

        #------------------------------------------------- validate button
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.validate)
        self.verticalLayout_4.addWidget(self.pushButton_2)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 380, 201, 41))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        #----------------------------------------------- ComboBox to filter date wise
        self.comboBox = ExtendedComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_3.addWidget(self.comboBox, 5, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 350, 169, 21))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 430, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 480, 201, 41))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")

        #-------------------------------------------------- ComboBox_2 to filter Facility Name wise
        self.comboBox_2 = ExtendedComboBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout_4.addWidget(self.comboBox_2, 0, 0, 1, 1)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 530, 201, 41))
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
        self.pushButton_3.clicked.connect(self.export_to_csv)
        self.verticalLayout_5.addWidget(self.pushButton_3)
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(10, 580, 201, 41))
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
        self.pushButton_3.clicked.connect(self.reset)
        self.gridLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(60, 20, 117, 144))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("icon.jpg"))
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Upload"))
        self.pushButton_2.setText(_translate("Dialog", "Validate"))
        self.label.setText(_translate("Dialog", "Select Date"))
        self.label_2.setText(_translate("Dialog", "Select Facility Name"))
        self.pushButton_3.setText(_translate("Dialog", "Export"))
        self.pushButton_4.setText(_translate("Dialog", "Reset"))

    
    #====================================================== Control Function =================================================        
            
    # Reset button functionality
    def reset(self):
        self.lineEdit.clear()
        self.tableView.clearSpans()
        self.comboBox_2.clear()
        self.comboBox.clear()
        self.tableView.reset()
        self.isChanged = True
        print('reset data is successful...........!')
        self.pushButton.setEnabled(True)
        self.pushButton_4.setDisabled(True)
        self.pushButton_2.setDisabled(True)
        self.pushButton_3.setDisabled(True)
    
    def upload(self):
        global df_, df_OrgHeaders

        # getting file and its name
        fileName, _ = QFileDialog.getOpenFileName(Dialog, "Open CSV",(QtCore.QDir.homePath()), "CSV (*.csv)")
        # displaying filename in display box
        self.lineEdit.setText(fileName)
        # reading csv files
        df_ = pd.read_csv(fileName)

        #grab the first row for the header
        new_header = df_.iloc[1] 

        #set the header row as the df header
        df_.columns = new_header 

        #df_.dropna(how='all', axis=1)
        df_.columns = ['col_' + str(index) for index in range(1, len(df_.columns)+1)]
        df_OrgHeaders = df_.iloc[[0, 1]]
        
        df_.drop(df_.index[[0, 1]], inplace=True)

        self.model = PandasModel(df_)
        self.proxy = CustomProxyModel(self)
        self.proxy.setSourceModel(self.model)

        # Filtering model
        filter_proxy_model = QtCore.QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(self.model)

        # filter_proxy_model to filter text
        self.lineEdit_2.textChanged.connect(filter_proxy_model.setFilterRegExp)
        
        self.tableView.setModel(filter_proxy_model)
        return df_

    # Upload file button functionality
    def loadFile(self, df_):

        self.model = PandasModel(df_)
        self.proxy = CustomProxyModel(self)
        self.proxy.setSourceModel(self.model)
        # Filtering model
        filter_proxy_model = QtCore.QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(self.model)
        filter_proxy_model.setFilterKeyColumn(12)

        # filter_proxy_model to filter text
        #self.lineEdit_2.textChanged.connect(filter_proxy_model.setFilterRegExp)
        
        self.tableView.setModel(filter_proxy_model)

        self.comboBox.addItems(["{0}".format(col) for col in self.model._df['col_1'][:]])
        self.comboBox_2.addItems(["{0}".format(col) for col in self.model._df['col_13'][:]])
        self.comboBox.currentIndexChanged.connect(self.index_changed)
        self.comboBox.currentIndexChanged[str].connect(filter_proxy_model.setFilterRegExp)
        self.comboBox_2.currentIndexChanged.connect(self.index_changed)
        self.comboBox_2.currentIndexChanged[str].connect(filter_proxy_model.setFilterRegExp)
        self.lineEdit_2.textChanged.connect(filter_proxy_model.setFilterRegExp)
        self.pushButton.setDisabled(True)
        return df_

    def validate(self):
        # df = self.loadFile()
        df = self.loadFile(df_)
        
        # 4.3 <= 2.1.1.a + 2.1.1.b + 2.2
        def res1(df):
            if float(df['col_74']) > float(df['col_48']) + float(df['col_49']) + float(df['col_52']):
                return 'Inconsistent'
            elif pd.isnull(df['col_74']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']) and pd.isnull(df['col_52']):
                return 'Blank'
            elif pd.isnull(df['col_74']) or pd.isnull(df['col_48']) or pd.isnull(df['col_49']) or pd.isnull(df['col_52']):
                return 'Blank Error'
            else:
                return 'Consistent'

        # 1.1.1 <= 1.1
        def res2(df):
            if df['col_22'] > df['col_21']:
                return 'Inconsistent'
            elif pd.isnull(df['col_21']) and pd.isnull(df['col_22']):
                return 'Blank'
            elif pd.isnull(df['col_21']):
                return 'Blank Error (1.1 is blank)'
            elif pd.isnull(df['col_22']):
                return 'Blank Error (1.1.1 is blank)'
            else:
                return 'Consistent'

        
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
            #if float(df['col_146']) <= float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120'] + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
            if float(df['col_144']) > float(df['col_105']) + float(df['col_106']) + float(df['col_107'])+ float(df['col_108']) + float(df['col_109']) + float(df['col_110'])+ float(df['col_111']) + float(df['col_112']) + float(df['col_113'])+ float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118'])+ float(df['col_119']) + float(df['col_120'])+ float(df['col_121'])+ float(df['col_122'])+ float(df['col_123'])+ float(df['col_124'])+ float(df['col_125'])+ float(df['col_126'])+ float(df['col_127']) + float(df['col_128'])+ float(df['col_131'])+ float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
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
            #if float(df['col_146']) <= float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120'] + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
            if float(df['col_145']) > float(df['col_105']) + float(df['col_106']) + float(df['col_107'])+ float(df['col_108']) + float(df['col_109']) + float(df['col_110'])+ float(df['col_111']) + float(df['col_112']) + float(df['col_113'])+ float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118'])+ float(df['col_119']) + float(df['col_120'])+ float(df['col_121'])+ float(df['col_122'])+ float(df['col_123'])+ float(df['col_124'])+ float(df['col_125'])+ float(df['col_126'])+ float(df['col_127']) + float(df['col_128'])+ float(df['col_131'])+ float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
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
            #if float(df['col_146']) <= float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120'] + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
            if float(df['col_146']) > float(df['col_105']) + float(df['col_106']) + float(df['col_107'])+ float(df['col_108']) + float(df['col_109']) + float(df['col_110'])+ float(df['col_111']) + float(df['col_112']) + float(df['col_113'])+ float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118'])+ float(df['col_119']) + float(df['col_120'])+ float(df['col_121'])+ float(df['col_122'])+ float(df['col_123'])+ float(df['col_124'])+ float(df['col_125'])+ float(df['col_126'])+ float(df['col_127']) + float(df['col_128'])+ float(df['col_131'])+ float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
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


        
        df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res1, axis = 1)
        df['1.1 <= 1.1.1'] = df.apply(res2, axis = 1)
        df['1.3.1.a <= 1.3.1'] = df.apply(res3, axis = 1)
        df['1.2.7 <= 1.1'] = df.apply(res4, axis = 1)
        df['1.5.1.a <= 1.1'] = df.apply(res5, axis = 1)
        df['1.5.1.b <= 1.5.1.a'] = df.apply(res6, axis = 1)
        df['2.1.2 <= 2.1.1.a + 2.1.1.b'] = df.apply(res7, axis = 1)
        #df['validity_check_8'] = df.apply(res8, axis = 1)
        df['2.1.3 <= 2.1.1.a + 2.1.1.b'] = df.apply(res9, axis = 1)
        df['2.2.2 <= 2.2'] = df.apply(res10, axis = 1)
        df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res11, axis = 1)
        df['6.1.1 <= 3.1.1.a + 3.1.1.b'] = df.apply(res12, axis = 1)
        df['6.1.9 <= 3.1.1.a + 3.1.1.b'] = df.apply(res13, axis = 1)
        df['6.1.13 <= 3.1.1.a + 3.1.1.b'] = df.apply(res14, axis = 1)
        df['2.2.1 <= 2.2'] = df.apply(res15, axis = 1)
        df['3.1.2 <= 3.1.1.a + 3.1.1.b'] = df.apply(res16, axis = 1)
        df['3.3.1 <= 3.1.1.a + 3.1.1.b'] = df.apply(res17, axis = 1)
        df['3.3.2 <= 3.3.1'] = df.apply(res18, axis = 1)
        df['4.1 <= 2.1.1.a + 2.1.1.b'] = df.apply(res19, axis = 1)
        df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res20, axis = 1)
        df['4.1 <= 2.1.1.a + 2.1.1.b'] = df.apply(res21, axis = 1)
        df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'] = df.apply(res22, axis = 1)
        df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(res23, axis = 1)
        df['6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(res24, axis = 1)
        df['6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(res25, axis = 1)
        df['6.7.3<=6.7.2'] = df.apply(res26, axis = 1)
        df['10.1.2<=10.1.1'] = df.apply(res27, axis = 1)
        df['10.2.1.b<=10.2.1.a'] = df.apply(res28, axis = 1)
        df['3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2'] = df.apply(res29, axis = 1)
        df['8.1.1.c<=8.1.1.a'] = df.apply(res30, axis = 1)
        df['9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8'] = df.apply(res31, axis = 1)
        df['8.1.1.b<=8.1.1.a'] = df.apply(res32, axis = 1)
        

        df = pd.concat([df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'],
                        df['1.1 <= 1.1.1'],
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
        
        frames = [df_OrgHeaders, df_]
        df = pd.concat(frames, sort=False)

        df.astype(str)
        
        #df.to_csv('TEST_DATA.csv')
        
        # df_.astype(str)
        # df = df_ + df
        
        # model to display on screen
        # model = PandasModel(df)
        # self.tableView.setModel(model)
        
        self.model = PandasModel(df)
        self.proxy = CustomProxyModel(self)
        self.proxy.setSourceModel(self.model)
        # Filtering model
        filter_proxy_model = QtCore.QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(self.model)
        self.tableView.setModel(filter_proxy_model)
        self.comboBox_2.currentIndexChanged[str].connect(filter_proxy_model.setFilterRegExp) and self.comboBox.currentIndexChanged[str].connect(filter_proxy_model.setFilterRegExp)
        filter_proxy_model.setFilterKeyColumn(0)
        self.lineEdit_2.textChanged.connect(filter_proxy_model.setFilterRegExp)
        
        #----------------------------------------------------------------------------------------------------
        return df

    def index_changed(self, i):
        print(i)

    def text_changed(self, j):
        print(j) 
       
    def export_to_csv(self):
        # filename = QFileDialog.getSaveFileName(Dialog, "Save to CSV", "table.csv",
        #                                        "Comma Separated Values Spreadsheet (*.csv);;"
        #                                        "All Files (*)")[0]
 
        # if filename:
        #     self.save_csv(filename, df)
        df.to_csv('table.csv')
        
 
    def save_csv(self, filename, df):
        """Save the current table data to the specified CSV file."""

        datamodel = PandasModel(df)
        row_count = datamodel.rowCount()
        col_count = datamodel.columnCount()
 
        with open(filename, 'w') as fd:
            writer = csv.writer(fd, quoting=csv.QUOTE_MINIMAL)
 
            # write headers
            csv_row = []
            for col in range(col_count):
                csv_row.append(datamodel.headerData(col, Qt.Horizontal, Qt.DisplayRole))
 
            writer.writerow(csv_row)
 
            # write data
            for row in range(row_count):
                csv_row = []
 
                for col in range(col_count):
                    index = datamodel.index(row, col)
                    csv_row.append(datamodel.data(index, Qt.DisplayRole))
 
                writer.writerow(csv_row)

    ####################################################################################
    @QtCore.pyqtSlot(int)
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):

        self.logicalIndex   = logicalIndex
        self.menuValues     = QtWidgets.QMenu(self)
        self.signalMapper   = QtCore.QSignalMapper(self)
        self.comboBox.blockSignals(True)
        self.comboBox.setCurrentIndex(self.logicalIndex)
        self.comboBox.blockSignals(True)

        valuesUnique = self.model._df.iloc[:, self.logicalIndex].unique()

        actionAll = QtWidgets.QAction("All", self)
        actionAll.triggered.connect(self.on_actionAll_triggered)
        self.menuValues.addAction(actionAll)
        self.menuValues.addSeparator()
        for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):
            action = QtWidgets.QAction(actionName, self)
            self.signalMapper.setMapping(action, actionNumber)
            action.triggered.connect(self.signalMapper.map)
            self.menuValues.addAction(action)
        self.signalMapper.mapped.connect(self.on_signalMapper_mapped)
        headerPos = self.tableView.mapToGlobal(self.horizontalHeader.pos())
        posY = headerPos.y() + self.horizontalHeader.height()
        posX = headerPos.x() + self.horizontalHeader.sectionPosition(self.logicalIndex)

        self.menuValues.exec_(QtCore.QPoint(posX, posY))

    @QtCore.pyqtSlot()
    def on_actionAll_triggered(self):
        filterColumn = self.logicalIndex
        self.proxy.setFilter("", filterColumn)

    @QtCore.pyqtSlot(int)
    def on_signalMapper_mapped(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        self.proxy.setFilter(stringAction, filterColumn)

    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        self.proxy.setFilter(text, self.proxy.filterKeyColumn())

    @QtCore.pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self.proxy.setFilterKeyColumn(index)
    
    
#======================================================== Class For Checkable Combo Box ==========================================

class CheckableComboBox(QtWidgets.QComboBox):
    def __init__(self, parent = None):
        super(CheckableComboBox, self).__init__(parent)
        self.setView(QtWidgets.QListView(self))
        self.view().pressed.connect(self.handle_item_pressed)
        self.setModel(QtGui.QStandardItemModel(self))

    # when any item get pressed 
    def handle_item_pressed(self, index): 
  
        # getting which item is pressed 
        item = self.model().itemFromIndex(index) 
  
        # make it check if unchecked and vice-versa 
        if item.checkState() == Qt.Checked: 
            item.setCheckState(Qt.Unchecked) 
        else: 
            item.setCheckState(Qt.Checked) 
  
        # calling method 
        self.check_items() 
  
    # method called by check_items 
    def item_checked(self, index): 
  
        # getting item at index 
        item = self.model().item(index, 0) 
  
        # return true if checked else false 
        return item.checkState() == Qt.Checked 
  
    # calling method 
    def check_items(self): 
        # blank list 
        checkedItems = [] 
  
        # traversing the items 
        for i in range(self.count()): 
  
            # if item is checked add it to the list 
            if self.item_checked(i): 
                checkedItems.append(i) 
  
        # call this method 
        self.update_labels(checkedItems) 
  
    # method to update the label 
    def update_labels(self, item_list): 
        global n
        n = '' 
        count = 0
  
        # traversing the list 
        for i in item_list: 
  
            # if count value is 0 don't add comma 
            if count == 0: 
                n += ' % s' % i 
            # else value is greater then 0 
            # add comma 
            else: 
                n += ', % s' % i 
  
            # increment count 
            count += 1
  
  
        # loop 
        for i in range(self.count()): 
  
            # getting label 
            text_label = self.model().item(i, 0).text() 
  
            # default state 
            if text_label.find('-') >= 0: 
                text_label = text_label.split('-')[0] 
  
            # shows the selected items 
            item_new_text_label = text_label + ' - selected index: ' + n 
  
           # setting text to combo box 
            self.setItemText(i, item_new_text_label) 
        
        return n
    # flush 
    sys.stdout.flush()

#============================================================= PandasModel Class =======================


#============================================================== Main Function =====================================================

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QWidget()
    ui = Ui_Form()
    Dialog.show()
    sys.exit(app.exec_())