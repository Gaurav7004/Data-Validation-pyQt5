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
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 230, 201, 40))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        # Upload Button Signal
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
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 270, 201, 40))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        
        # Validate Button Signal
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
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 710, 201, 41))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        
        # Export Button Signal
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.pushButton_3.clicked.connect(self.exportCSV)
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_5.addWidget(self.pushButton_3)
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(10, 770, 201, 41))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        
        # Reset Button Signal
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
        
        # Select State Signal
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.clicked.connect(self.onSelectState)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 330, 201, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        
        # Select District Signal
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.clicked.connect(self.onSelectDistrict)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 380, 201, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        
        # Select Facility Type Signal
        self.pushButton_7 = QtWidgets.QPushButton(Dialog)
        self.pushButton_7.clicked.connect(self.onSelectFacilitytype)
        self.pushButton_7.setGeometry(QtCore.QRect(0, 430, 211, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        
        # Select Facility Name Signal
        self.pushButton_8 = QtWidgets.QPushButton(Dialog)
        self.pushButton_8.clicked.connect(self.onSelectFacilityName)
        self.pushButton_8.setGeometry(QtCore.QRect(0, 480, 211, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")
        
        #Select Month Signal
        self.pushButton_9 = QtWidgets.QPushButton(Dialog)
        self.pushButton_9.setGeometry(QtCore.QRect(0, 530, 211, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_9")
        
        #Select Year Signal
        self.pushButton_10 = QtWidgets.QPushButton(Dialog)
        self.pushButton_10.setGeometry(QtCore.QRect(0, 580, 211, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setObjectName("pushButton_10")

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
        self.pushButton_7.setText(_translate("Dialog", "Select Facility Type"))
        self.pushButton_8.setText(_translate("Dialog", "Select Facility Name"))
        self.pushButton_9.setText(_translate("Dialog", "Select Month"))
        self.pushButton_10.setText(_translate("Dialog", "Select Year"))

    # To upload file
    def upload(self):
        global df_, df_OrgHeaders
        products = {'Date': [2,3,1,5,3,9],
                    'Month': ['April', 'May', 'April', 'June', 'May', 'July'],        
                    'Year': [2020, 2021, 2019, 2020, 2020, 2020],
                    'State': ['BR', 'JH', 'HR', 'JH', 'BR', 'PB'],
                    'Blank': ['nan','nan','nan','nan','nan','nan'],
                    'District' : ['BS', 'GW', 'AM', 'RN', 'PB', 'GR'],
                    'Facility Type': ['HSC', 'DH', 'HSC', 'CHC', 'HSC', 'DH'],
                    'Facility Name': ['PP CAC', 'SC Bkr', 'SC Bara', 'SC Bkr', 'PP CAC', 'PP CAC'],
                    '4.3': [1, 0, 2, 2, 9, 8],
                    '2.1.1.a': [0, 1, 1, 2, 3, 4],
                    '2.1.1.b': [1, 2, 0, 0, 0, 0],
                    '2.2': [1,2, 3, 4, 0, 0],
                    }
        df_ = pd.DataFrame(products, columns= ['Date', 'Month', 'Year', 'State', 'Blank', 'District', 'Facility Type', 'Facility Name', '4.3', '2.1.1.a', '2.1.1.b', '2.2'])

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
        self.pushButton.setDisabled(False)
        return df_

    # to validate modified checks
    def validate(self):
        global df, list_set
        # df = self.loadFile()
        df = self.loadFile(df_)

        print("Entering Validate")

        # 4.3 <= 2.1.1.a + 2.1.1.b + 2.2
        def res1(df):
            count = 0
            if float(df['col_9']) > float(df['col_10']) + float(df['col_11']) + float(df['col_12']):
                count = count+1
                return 'Inconsistent'
            elif pd.isnull(df['col_9']) and pd.isnull(df['col_10']) and pd.isnull(df['col_11']) and pd.isnull(df['col_12']):
                return 'Blank'
            elif pd.isnull(df['col_9']) or pd.isnull(df['col_10']) or pd.isnull(df['col_11']) or pd.isnull(df['col_12']):
                return 'Blank Error'
            else:
                return 'Consistent'
        
        df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res1, axis=1)
        
        df = pd.concat([df_, df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2']], axis=1)

        df.astype(str)
        # Select State #
        # convert the set to the list
        list_set = df_['col_4'].tolist()
        unique_list = set(list_set)
        return df

    ################################################################################
    # Select State

    # Select State Functionality
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
        
        index = 4
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
        item = list_set
        
        # looping to fill checkboxes, initially all checkboxes will be checked
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

    # method to check -> uncheck and vice versa
    def slotSelect(self, state):
        for checkbox in self.checkBoxs:
            checkbox.setChecked(QtCore.Qt.Checked == state)

    # after ok selected 
    def menuClose(self):
        self.keywords[self.col] = []
        for element in self.checkBoxs:
            if element.isChecked():
                self.keywords[self.col].append(element.text())
        self.filterdata()
        self.menu.close()

    # Filter data columnwise
    def filterdata(self):
        global final_df
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(df.shape[0])])

        # for i in range(df.shape[0]): 
        j=0 
        for j in range(df.shape[0]):
            item = list_set
            
            print(self.keywords[self.col])
            #if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False     

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()] 
        print(final_lst, 'this is final list of Select State')
        final_df = df[final_lst]
        print(final_df)
        self.tableView.setModel(PandasModel(final_df))
        return final_df

    
    ################################################################################
    # Select District

        # Select District Functionality
    def onSelectDistrict(self, index):
        self.keywords = dict([(i, []) for i in range(final_df.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 400 }')
        font = self.menu.font()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.menu.setFont(font) 
        
        index = 6
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
        checkBox.stateChanged.connect(self.slotSelectDistrict)

        # list storing state data
        list_set = final_df['col_6'].to_list()

        item = list_set
        
        # looping to fill checkboxes, initially all checkboxes will be checked
        for i in range(len(item)):
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
        btn.accepted.connect(self.menuCloseDistrict)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)
        self.pushButton_6.setMenu(self.menu)

    # method to check -> uncheck and vice versa
    def slotSelectDistrict(self, state):
        for checkbox in self.checkBoxs:
            checkbox.setChecked(QtCore.Qt.Checked == state)

    # after ok selected 
    def menuCloseDistrict(self):
        self.keywords[self.col] = []
        for element in self.checkBoxs:
            if element.isChecked():
                self.keywords[self.col].append(element.text())
        print(self.keywords[self.col])
        self.filterdataDistrict()
        self.menu.close()

    # Filter data columnwise
    def filterdataDistrict(self):
        global final_df_District
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(final_df['col_6'].shape[0])])
        print(columnsShow)

        j=0 
        for j in range(final_df['col_6'].shape[0]):
            item = final_df['col_6'].to_list()
            
            #if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False     

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()] 
        print(final_lst, 'this is final list of Select District')
        final_df_District = final_df[final_lst]
        print(final_df_District)
        self.tableView.setModel(PandasModel(final_df_District))
        return final_df_District


    ################################################################################
    # Select Facility Type

    # Select Facilitytype Functionality
    def onSelectFacilitytype(self, index):
        self.keywords = dict([(i, []) for i in range(final_df_District.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 400 }')
        font = self.menu.font()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.menu.setFont(font) 
        
        index = 7
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
        checkBox.stateChanged.connect(self.slotSelectFacilityType)

        # list storing Facility Type data
        list_set = final_df['col_7'].to_list()

        item = list_set
        
        # looping to fill checkboxes, initially all checkboxes will be checked
        for i in range(len(item)):
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
        btn.accepted.connect(self.menuCloseFacilityType)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)
        ############# Always set Pushbutton ####################
        self.pushButton_7.setMenu(self.menu)

    # method to check -> uncheck and vice versa
    def slotSelectFacilityType(self, state):
        for checkbox in self.checkBoxs:
            checkbox.setChecked(QtCore.Qt.Checked == state)

    # after ok selected 
    def menuCloseFacilityType(self):
        self.keywords[self.col] = []
        for element in self.checkBoxs:
            if element.isChecked():
                self.keywords[self.col].append(element.text())
        print(self.keywords[self.col])
        self.filterdataFacilityType()
        self.menu.close()

    # Filter data columnwise
    def filterdataFacilityType(self):
        global final_df_FacilityType
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(final_df_District['col_7'].shape[0])])
        print(columnsShow)

        j=0 
        for j in range(final_df_District['col_7'].shape[0]):
            item = final_df_District['col_7'].to_list()
            
            #if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False     

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()] 
        print(final_lst, 'this is final list of Select District')

        # matching list of facility type with col of dataframe returned by onSelectDistrict fun
        final_df_FacilityType = final_df_District[final_lst]
        print(final_df_FacilityType)
        self.tableView.setModel(PandasModel(final_df_FacilityType))
        return final_df_FacilityType

    
    ################################################################################
    # Select Facility Name

    # Select FacilityName Functionality
    def onSelectFacilityName(self, index):
        self.keywords = dict([(i, []) for i in range(final_df_FacilityType.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 400 }')
        font = self.menu.font()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.menu.setFont(font) 
        
        index = 8
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
        checkBox.stateChanged.connect(self.slotSelectFacilityName)

        # list storing Facility Name data
        list_set = final_df_FacilityType['col_8'].to_list()

        item = list_set
        
        # looping to fill checkboxes, initially all checkboxes will be checked
        for i in range(len(item)):
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
        btn.accepted.connect(self.menuCloseFacilityName)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)

        ############# Always set Pushbutton ####################
        self.pushButton_8.setMenu(self.menu)

    # method to check -> uncheck and vice versa
    def slotSelectFacilityName(self, state):
        for checkbox in self.checkBoxs:
            checkbox.setChecked(QtCore.Qt.Checked == state)

    # after ok selected 
    def menuCloseFacilityName(self):
        self.keywords[self.col] = []
        for element in self.checkBoxs:
            if element.isChecked():
                self.keywords[self.col].append(element.text())
        print(self.keywords[self.col])
        self.filterdataFacilityName()
        self.menu.close()

    # Filter data columnwise
    def filterdataFacilityName(self):
        global final_df_FacilityName
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(final_df_FacilityType['col_8'].shape[0])])
        print(columnsShow)

        j=0 
        for j in range(final_df_FacilityType['col_8'].shape[0]):
            item = final_df_FacilityType['col_8'].to_list()
            
            #if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False     

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()] 
        print(final_lst, 'this is final list of Select District')

        # matching list of facility type with col of dataframe returned by onSelectDistrict fun
        final_df_FacilityName = final_df_FacilityType[final_lst]
        print(final_df_FacilityName)
        self.tableView.setModel(PandasModel(final_df_FacilityName))
        return final_df_FacilityName


    # Export final result
    def exportCSV(self):
        filename = QFileDialog.getSaveFileName(Dialog, "Save to CSV", "table.csv",
                                               "Comma Separated Values Spreadsheet (*.csv);;"
                                               "All Files (*)")[0]
        filename = filename + ".csv"
        final_df.to_csv(filename, index=False)


################################# Main Function ##################################

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
