import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
import sys

########################################### PandasModel to display it on tableView #####################
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

################################################ Main UI ###############################################
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
        # upload
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.clicked.connect(self.upload)

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
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 350, 201, 40))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        
        # validate
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_2.clicked.connect(self.validate)
        
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_4.addWidget(self.pushButton_2)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 650, 201, 41))
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
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(10, 710, 201, 41))
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
        
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.selState = self.pushButton_5.clicked.connect(self.onSelectState)

        self.checkBoxs = []

        self.pushButton_5.setGeometry(QtCore.QRect(10, 420, 201, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 480, 201, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Upload"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "Search..."))
        self.pushButton_2.setText(_translate("Dialog", "Validate"))
        self.pushButton_3.setText(_translate("Dialog", "Export"))
        self.pushButton_4.setText(_translate("Dialog", "Reset"))
        self.pushButton_5.setText(_translate("Dialog", "Select State"))
        self.pushButton_6.setText(_translate("Dialog", "Select District"))


    def upload(self):
        global df_, df_OrgHeaders
        products = {'Date': ['2_April','3_May','1_June','5_July', '3_April', '9_July'],
                    'State': ['BR', 'JH', 'HR', 'JH', 'BR', 'PB'],
                    'Blank': ['nan','nan','nan','nan','nan','nan'],
                    'District' : ['BS', 'GW', 'AM', 'RN', 'PB', 'GR'],
                    '4.3': [1, 0, 2, 2, 9, 8],
                    '2.1.1.a': [0, 1, 1, 2, 3, 4],
                    '2.1.1.b': [1, 2, 0, 0, 0, 0],
                    '2.2': [1,2, 3, 4, 0, 0],
                    }
        df_ = pd.DataFrame(products, columns= ['Date', 'State', 'Blank', 'District', '4.3', '2.1.1.a', '2.1.1.b', '2.2'])

        self.tableView.setModel(PandasModel(df_))

        # grab the first row for the header
        new_header = df_.iloc[1]

        # set the header row as the df header
        df_.columns = new_header

        #df_.dropna(how='all', axis=1)
        df_.columns = ['col_' + str(index)
                       for index in range(1, len(df_.columns)+1)]
        df_OrgHeaders = df_.iloc[[0, 1]]
        #df_.drop(df_.index[[0, 1]], inplace=True)
        #df_.dropna(subset=['col_4'], how='all', inplace=True)
        return df_

    def loadFile(self, df_):
        self.pushButton.setDisabled(True)
        return df_

    def validate(self):
        global df
        # df = self.loadFile()
        df = self.loadFile(df_)

        print("Entering Validate")

        # 4.3 <= 2.1.1.a + 2.1.1.b + 2.2
        def res1(df):
            count = 0
            if float(df['col_5']) > float(df['col_6']) + float(df['col_7']) + float(df['col_8']):
                count = count+1
                return 'Inconsistent'
            elif pd.isnull(df['col_5']) and pd.isnull(df['col_6']) and pd.isnull(df['col_7']) and pd.isnull(df['col_8']):
                return 'Blank'
            elif pd.isnull(df['col_5']) or pd.isnull(df['col_6']) or pd.isnull(df['col_7']) or pd.isnull(df['col_8']):
                return 'Blank Error'
            else:
                return 'Consistent'
        
        df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res1, axis=1)
        
        df = pd.concat([df_, df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2']], axis=1)

        df.astype(str)
        ################################## Select State ###############################
        # convert the set to the list
        list_set = df_['col_2'].tolist()
        unique_list = set(list_set)
        
        #self.comboBox.addItems(["{0}".format(col) for col in unique_list])
        print(df)
        return df

    # method to check -> uncheck and vice versa
    def slotSelect(self, state):
        for checkbox in self.checkBoxs:
            checkbox.setChecked(QtCore.Qt.Checked == state)

    # Select State followed by Select District
    def onSelectState(self, index):
        self.keywords = dict([(i, []) for i in range(df.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 400 }')
        font = self.menu.font()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.menu.setFont(font) 

        index = 2
        self.col = index

        data_unique = []

        self.checkBoxs = []
        
        # Selectall added into Dropdown
        checkBox = QtWidgets.QCheckBox("Select all", self.menu)

        # All the checkboxes are enabled to check
        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(checkBox)
        self.menu.addAction(checkableAction)
        checkBox.setChecked(True)
        checkBox.stateChanged.connect(self.slotSelect)

        # list storing state data
        item = df['col_2'].tolist()
        
        # looping to fill checkboxes, initially all checkbosxes will be checked
        for i in range(len(df)):
            if item[i] not in data_unique:
                data_unique.append(item[i])
                checkBox = QtWidgets.QCheckBox(item[i], self.menu)
                checkBox.setChecked(True)
                checkableAction = QtWidgets.QWidgetAction(self.menu)
                checkableAction.setDefaultWidget(checkBox)
                self.menu.addAction(checkableAction)
                self.checkBoxs.append(checkBox)


        # Ok, cancel button
        btn = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
                                     QtCore.Qt.Horizontal, self.menu)

        # ok selected                             
        btn.accepted.connect(self.menuClose)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)
        self.pushButton_5.setMenu(self.menu)

    # after ok selected 
    def menuClose(self):
        self.keywords[self.col] = []
        for element in self.checkBoxs:
            if element.isChecked():
                self.keywords[self.col].append(element.text())
        self.filterdata()
        self.menu.close()

    def filterdata(self):
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(df.shape[0])])
        print(columnsShow, 'ColSHOWWWW')


        # for i in range(df.shape[0]): 
        j=0 
        for j in range(df.shape[0]):
            item = df['col_2'].to_list()
            
            print(self.keywords[self.col])
            #if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False

        

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()]
            
        print(final_lst)    
        final_df = df[final_lst]
        print(final_df)
        self.tableView.setModel(PandasModel(final_df))
            


    # Select District followed by Select date
    def onSelectDistrict(self, text):
        curr_text = []
        curr_text.append(text)
        boolean_series = df_onSelectState.col_4.isin(curr_text)
        df_onSelectDistrict = df_onSelectState[boolean_series]

        self.tableView.setModel(PandasModel(df_onSelectDistrict))
        return df_onSelectDistrict

    def exportCSV(self):
        filename = QFileDialog.getSaveFileName(Dialog, "Save to CSV", "table.csv",
                                               "Comma Separated Values Spreadsheet (*.csv);;"
                                               "All Files (*)")[0]
        filename = filename + ".csv"
        df.to_csv(filename, index=False)

################################################### Main Function
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
