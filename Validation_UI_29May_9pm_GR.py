from __future__ import unicode_literals
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QFileDialog
import sys, re
from xlwt import Workbook
import io




################################### PandasModel to display it on tableView ####################################

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


##################################################### Main UI ############################################
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1678, 977)
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
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 710, 201, 41))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        # Export to csv signal
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
        self.pushButton_5.setGeometry(QtCore.QRect(10, 380, 201, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 430, 201, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_8 = QtWidgets.QPushButton(Dialog)
        self.pushButton_8.setGeometry(QtCore.QRect(0, 480, 211, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(Dialog)
        self.pushButton_9.setGeometry(QtCore.QRect(0, 530, 211, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(Dialog)
        self.pushButton_10.setGeometry(QtCore.QRect(0, 580, 211, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setObjectName("pushButton_10")

        ############################################# Upload Button 
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.clicked.connect(self.upload)

        self.pushButton.setGeometry(QtCore.QRect(10, 180, 199, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        
        self.pushButton_2.setGeometry(QtCore.QRect(10, 280, 199, 33))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        ############################################# ComboBox to filter Facility Type
        self.comboBox = QtWidgets.QComboBox(Dialog)
        #self.comboBox.setPlaceholderText('Select Facility Type')
        self.comboBox.setGeometry(QtCore.QRect(10, 231, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Waree")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "Search..."))
        self.pushButton_3.setText(_translate("Dialog", "Export"))
        self.pushButton_4.setText(_translate("Dialog", "Reset"))
        self.pushButton_5.setText(_translate("Dialog", "Select State"))
        self.pushButton_6.setText(_translate("Dialog", "Select District"))
        self.pushButton_8.setText(_translate("Dialog", "Select Facility Name"))
        self.pushButton_9.setText(_translate("Dialog", "Select Month"))
        self.pushButton_10.setText(_translate("Dialog", "Select Year"))
        self.pushButton.setText(_translate("Dialog", "Upload"))
        self.pushButton_2.setText(_translate("Dialog", "Validate"))


    # Function To upload file
    def upload(self):
        global df_, df_OrgHeaders

        #fileName, _ = QFileDialog.getOpenFileName(Dialog, "Open CSV",(QtCore.QDir.homePath()), "CSV (*.csv)")
        fileName, _ = QFileDialog.getOpenFileName(Dialog, "Open Excel",(QtCore.QDir.homePath()), "Excel (*.xls *.xlsx)")
        
        # displaying filename in display box
        self.lineEdit.setText(fileName)

        df_ = pd.read_excel(fileName)

        df_.to_csv("FileName.csv")
        df_ = pd.read_csv("FileName.csv")
        print(df_)

        #Dropping last two rows
        df_.drop(df_.index[[-1, -2]], inplace=True)

        # Extracting string from 1st cell of dataframe
        str_to_extr_MonthYear = str(df_.iloc[0])

        # grab the first row for the header
        new_header = df_.iloc[1]

        # #take the data less the header row
        df_ = df_[1:]

        #set the header row as the df header
        df_.columns = new_header        

        # Extracting Month , Year from string
        results = re.findall(r"[abceglnoprtuvyADFJMNOS|]{3}[\s-]\d{2,4}" , str_to_extr_MonthYear)
        print(results)

        # Splitting Month and Year
        MYList = results[0].split('-')
        
        # Partial list of headers
        lst1 = df_.columns[:16].values

        # Picking row items after 18th row to merge with lst1
        lst2 = df_.iloc[1, 16:].to_numpy()

        # Merging both lists
        lst3 = np.concatenate((lst1, lst2))

        # Assign lst3 as new column header
        df_.columns = lst3

        # Taking DataFrame from second row
        df_ = df_[2:]

        # Insering Month and Year to the orignal dataframe
        df_.insert(1, 'Month', MYList[0])
        df_.insert(2, 'Year', MYList[1])

        # Removing A column named as # coming from orignal data
        df_ = df_.loc[:, df_.columns != '#']

        # Reindexing dataframe
        df_ = df_.reset_index(drop=True)

        df_ = df_.iloc[:,1:]

        # Temporary column to verify modified checks
        temp_columns = ['col_' + str(index) for index in range(1, len(df_.columns)+1)]

        # Merging and converting temp_columns to orignal header to dictionary
        res_dict = {temp_columns[i]: df_.columns[i] for i in range(len(temp_columns))}
        
        # Picking the temporary column names and renaming column headers with it
        df_.columns = [i for i in res_dict.keys()]


        #Orignal Header
        df_OrgHeaders = [i for i in res_dict.values()]
        
        # convert the set to the list and fill inside comboBox to select facility type
        list_set = df_['col_12'].tolist()
        unique_list = set(list_set)
        print(unique_list)
        self.comboBox.addItems(["{0}".format(col) for col in unique_list])

        # Connecting comboBox to VerifyFType function 
        self.comboBox.currentIndexChanged[str].connect(self.VerifyFType)     
        
        # Displaying uploaded dataframe
        self.tableView.setModel(PandasModel(df_))

        # Disabling upload Button
        self.pushButton.setDisabled(True)
        return df_

    # Filtering Facility Type
    def VerifyFType(self):
        
        FType = self.comboBox.currentText()
        try :
            if (FType == 'Health Sub Centre'):
                print('Facility Type - ', FType)

                df = self.loadFile(df_)
                
                # Signaling HSC_Validate function i.e function where validation checks are present
                self.pushButton_2.clicked.connect(self.HSC_Validate)

                
                # Signaling onSelectState function i.e dropdown to Filter state
                self.pushButton_5.clicked.connect(self.onSelectState)

               
                # Signaling onSelectDistrict function i.e dropdown to Filter District
                self.pushButton_6.clicked.connect(self.onSelectDistrict)

                # Signaling onSelectFacilityName function i.e dropdown to Filter FacilityName
                self.pushButton_8.clicked.connect(self.onSelectFacilityName)

                # Signaling onSelectMonth function i.e dropdown to Filter Month
                self.pushButton_9.clicked.connect(self.onSelectMonth)

                # Signaling onSelectYear function i.e dropdown to Filter Year
                self.pushButton_10.clicked.connect(self.onSelectYear)

            elif ((FType == 'DH')):
                print(FType)
                self.DH_Validate()
            elif ((FType == 'SDH')):
                print(FType)
                self.SDH_Validate()
            elif ((FType == 'CHC')):
                print(FType)
                self.CHC_Validate()
            elif ((FType == 'PHC')):
                print(FType)
                self.PHC_Validate()
        except:
            raise Exception('Facility Type Name is not matching')


    # Upload file button functionality
    def loadFile(self, df_):   
        return df_


    # Validation for HSC 
    def HSC_Validate(self):
        global df
        # df = self.loadFile(df_)

        filterString = self.comboBox.currentText()
        df = df_.loc[df_['col_12'] == filterString]
        print(df)
        print('Entered HSC_Validate')

        # Modified Checks of HSC

        # 1.1(col_22) >= 1.1.1(col_23) (for related data items)
        def res2(df):
            if pd.isnull(df['col_22']) and pd.isnull(df['col_23']):
                return 'Blank'
            elif pd.isnull(df['col_22']) or pd.isnull(df['col_23']):
                if pd.isnull(df['col_22']):
                    return 'Inconsistent (Source is null)'
                elif pd.isnull(df['col_23']):
                    return 'Probable Reporting Error (1.1.1 is blank)'
            elif df['col_22'] < df['col_23']:
                return 'Inconsistent (Check Fails)' 
            elif df['col_22'] == 0 and df['col_23'] == 0 :     
                return 'consistent'
            else:
                return 'consistent'
            return df 

        
        # 1.3.1.a(col_29) <= 1.3.1(col_28) (for related data items) 
        # def res3(df):
        #     if (df['col_29'] is None) and (df['col_28'] is None):
        #         return 'Blank'
        #     elif (df['col_29'] is None) or (df['col_28'] is None):
        #         if (df['col_29'] is None):
        #             return 'Inconsistent (Source is null)'
        #         elif (df['col_28'] is None):
        #             return 'Probable Reporting Error (1.3.1 is blank)'
        #     if (df['col_29'] is None) > (df['col_28'] is None):
        #         return 'Inconsistent (Check Fails)' 
        #     elif df['col_29'] == 0 and df['col_28'] == 0 :     
        #         return 'consistent'
        #     else:
        #         return 'consistent'
        #     return df

        '''
        WE HAVE MERGING PROBLEM HERE
        '''
        df['1.1 >= 1.1.1'] = df.apply(res2, axis=1)
        # count_condition_2_consistent = df['1.1 <= 1.1.1'].str.count(
        #     "consistent").sum()
        # count_condition_2_inconsistent = df['1.1 <= 1.1.1'].str.count(
        #     "Inconsistent").sum()
        # count_condition_2_blank = df['1.1 <= 1.1.1'].str.count("Blank").sum()
        # count_condition_2_blank_error = df['1.1 <= 1.1.1'].str.count(
        #     "Blank Error").sum()

        #df['1.3.1.a <= 1.3.1'] = df.apply(res3, axis=1)
        # count_condition_3_consistent = df['1.3.1.a <= 1.3.1'].str.count(
        #     "consistent").sum()
        # count_condition_3_inconsistent = df['1.3.1.a <= 1.3.1'].str.count(
        #     "Inconsistent").sum()
        # count_condition_3_blank = df['1.3.1.a <= 1.3.1'].str.count(
        #     "Blank").sum()
        # count_condition_3_blank_error = df['1.3.1.a <= 1.3.1'].str.count(
        #     "Blank Error").sum()

        '''
        Don't remove this line otherwise you will face an error with the dataframes,
        while converting it to the list
        '''
        df = pd.concat([df['1.1 >= 1.1.1']], axis=1)
        
        # Mergining current result of modified checks with original dataframe and displaying it on screen
        frames =  [df_, df]
        print(frames)
        df = pd.concat(frames,axis=1, sort=False)
        #df = df.dropna(axis=0, subset=['col_2']) 

        '''
        ORIGNAL HEADERS
        '''
        # df.columns = df_OrgHeaders
        # df.astype(str)

        df.to_csv('HSC_ValidationChecks.csv')

        self.tableView.setModel(PandasModel(df))
        return df

    # Validation for DH
    def DH_Validate(self):
        print('Entered DH_Validate')

    # Validation for SDH
    def SDH_Validate(self):
        print('Entered SDH_Validate')

    # Validation for CHC
    def CHC_Validate(self):
        print('Entered CHC_Validate')

    # Validation for PHC
    def PHC_Validate(self):
        print('Entered PHC_Validate')


    #################################### Filter Functions after validation ##################################
    '''
    All the filters applied on Dropdowns are written here ...!
    '''
    ################################################################################
    # Select State Functionality
    def onSelectState(self, index):
        global list_set
        # convert the list to set, this will fill select state with unique value
        list_set = df['col_3'].to_list()
        
        #unique_list = set(list_set) 

        self.keywords = dict([(i, []) for i in range(df.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 400 }')
        font = self.menu.font()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.menu.setFont(font) 
        
        index = 3
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
    # Select District Functionality
    def onSelectDistrict(self, index):
        # convert the list to set, this will fill select state with unique value
        list_set_District = df['col_5'].tolist()
        
        list_set = list_set_District
        print(list_set)
        #unique_list = set(list_set) 

        self.keywords = dict([(i, []) for i in range(final_df.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 400 }')
        font = self.menu.font()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.menu.setFont(font) 
        
        index = 5
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
        item = list_set
        
        # looping to fill checkboxes, initially all checkboxes will be checked
        for i in range(len(final_df)):
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
        self.filterdataDistrict()
        self.menu.close()

    # Filter data columnwise
    def filterdataDistrict(self):
        global final_df_District
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(final_df.shape[0])])

        # for i in range(df.shape[0]): 
        j=0 
        for j in range(final_df.shape[0]):
            item = df['col_5'].tolist()
            
            print(self.keywords[self.col])
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
    # Select Facility Name Functionality
    def onSelectFacilityName(self, index):
        # convert the list to set, this will fill select state with unique value
        
        list_set = final_df_District['col_14'].tolist()
        print(list_set)
        #unique_list = set(list_set) 

        self.keywords = dict([(i, []) for i in range(final_df_District.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 400 }')
        font = self.menu.font()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.menu.setFont(font) 
        
        index = 14
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

        # list storing state data
        item = list_set
        
        # looping to fill checkboxes, initially all checkboxes will be checked
        for i in range(len(final_df_District)):
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
        self.filterdataFacilityName()
        self.menu.close()

    # Filter data columnwise
    def filterdataFacilityName(self):
        global final_df_FacilityName
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(final_df_District.shape[0])])

        # for i in range(df.shape[0]): 
        j=0 
        for j in range(final_df_District.shape[0]):
            item = df['col_14'].tolist()
            
            print(self.keywords[self.col])
            #if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False     

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()] 
        print(final_lst, 'this is final list of Select Facility Name')
        final_df_FacilityName = final_df_District[final_lst]
        print(final_df_FacilityName)
        self.tableView.setModel(PandasModel(final_df_FacilityName))
        return final_df_FacilityName

    ################################################################################
    # Select Month Functionality
    def onSelectMonth(self, index):
        # convert the list to set, this will fill select state with unique value
        
        list_set = final_df_FacilityName['col_1'].tolist()
        print(list_set)
        #unique_list = set(list_set) 

        self.keywords = dict([(i, []) for i in range(final_df_FacilityName.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 400 }')
        font = self.menu.font()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.menu.setFont(font) 
        
        index = 1
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
        checkBox.stateChanged.connect(self.slotSelectMonth)

        # list storing state data
        item = list_set
        
        # looping to fill checkboxes, initially all checkboxes will be checked
        for i in range(len(final_df_FacilityName)):
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
        btn.accepted.connect(self.menuCloseMonth)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)
        self.pushButton_9.setMenu(self.menu)

    # method to check -> uncheck and vice versa
    def slotSelectMonth(self, state):
        for checkbox in self.checkBoxs:
            checkbox.setChecked(QtCore.Qt.Checked == state)

    # after ok selected 
    def menuCloseMonth(self):
        self.keywords[self.col] = []
        for element in self.checkBoxs:
            if element.isChecked():
                self.keywords[self.col].append(element.text())
        self.filterdataMonth()
        self.menu.close()

    # Filter data columnwise
    def filterdataMonth(self):
        global final_df_Month
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(final_df_FacilityName.shape[0])])

        # for i in range(df.shape[0]): 
        j=0 
        for j in range(final_df_FacilityName.shape[0]):
            item = df['col_14'].tolist()
            
            print(self.keywords[self.col])
            #if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False     

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()] 
        print(final_lst, 'this is final list of Select Facility Name')
        final_df_Month = final_df_FacilityName[final_lst]
        print(final_df_Month)
        self.tableView.setModel(PandasModel(final_df_Month))
        return final_df_Month


    ################################################################################
    # Select Year Filter
    def onSelectYear(self, index):
        # convert the list to set, this will fill select state with unique value
        
        list_set = final_df_Month['col_2'].tolist()
        print(list_set)
        #unique_list = set(list_set) 

        self.keywords = dict([(i, []) for i in range(final_df_Month.shape[0])])
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
        checkBox.stateChanged.connect(self.slotSelectYear)

        # list storing state data
        item = list_set
        
        # looping to fill checkboxes, initially all checkboxes will be checked
        for i in range(len(final_df_Month)):
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
        btn.accepted.connect(self.menuCloseYear)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)
        self.pushButton_10.setMenu(self.menu)

    # method to check -> uncheck and vice versa
    def slotSelectYear(self, state):
        for checkbox in self.checkBoxs:
            checkbox.setChecked(QtCore.Qt.Checked == state)

    # after ok selected 
    def menuCloseYear(self):
        self.keywords[self.col] = []
        for element in self.checkBoxs:
            if element.isChecked():
                self.keywords[self.col].append(element.text())
        self.filterdataYear()
        self.menu.close()

    # Filter data columnwise
    def filterdataYear(self):
        global final_df_Year
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(final_df_Month.shape[0])])

        # for i in range(df.shape[0]): 
        j=0 
        for j in range(final_df_Month.shape[0]):
            item = df['col_2'].tolist()
            
            print(self.keywords[self.col])
            #if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False     

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()] 
        print(final_lst, 'this is final list of Select Facility Name')
        final_df_Year = final_df_Month[final_lst]
        print(final_df_Year)
        self.tableView.setModel(PandasModel(final_df_Year))
        return final_df_Year




    def exportCSV (self, final_df_Year):
        filename = QFileDialog.getSaveFileName(Dialog, "Save to CSV", "table.csv",
                                               "Comma Separated Values Spreadsheet (*.csv);;"
                                               "All Files (*)")[0]

        
        final_df_Year.to_csv(filename + "_" + 'ModifiedChecks.csv')



############################################# Main Function ##############################################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
