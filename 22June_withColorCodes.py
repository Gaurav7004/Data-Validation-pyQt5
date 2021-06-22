import sys, re
import numpy as np
from numpy.lib.function_base import percentile
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidgetAction
from PyQt5.QtCore import Qt



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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1347, 859)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 20, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.upload)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 160, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)

        # 2
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.VerifyFType)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        
        self.comboBox.setGeometry(QtCore.QRect(30, 100, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
    
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 60, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 210, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 320, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.clicked.connect(self.export)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 740, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(320, 20, 1011, 821))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.tableView.setFont(font)
        self.tableView.setObjectName("tableView")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 430, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 530, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 630, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        # 4
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.installEventFilter(Dialog)
        self.pushButton_4.clicked.connect(self.onSelectState)

        self.pushButton_4.setGeometry(QtCore.QRect(30, 260, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        # 5
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.installEventFilter(Dialog)
        self.pushButton_5.clicked.connect(self.onSelectDistrict)

        self.pushButton_5.setGeometry(QtCore.QRect(30, 360, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")

        # 6
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.installEventFilter(Dialog)
        self.pushButton_6.clicked.connect(self.onSelectFacilityName)

        self.pushButton_6.setGeometry(QtCore.QRect(30, 470, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")

        # 7
        self.pushButton_7 = QtWidgets.QPushButton(Dialog)
        self.pushButton_7.installEventFilter(Dialog)
        self.pushButton_7.clicked.connect(self.onSelectMonth)

        self.pushButton_7.setGeometry(QtCore.QRect(30, 570, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")

        # 8
        self.pushButton_8 = QtWidgets.QPushButton(Dialog)
        self.pushButton_8.installEventFilter(Dialog)
        self.pushButton_8.clicked.connect(self.onSelectYear)

        self.pushButton_8.setGeometry(QtCore.QRect(30, 670, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")

        # 9
        self.pushButton_9 = QtWidgets.QPushButton(Dialog)
        self.pushButton_9.clicked.connect(self.reset)
        self.pushButton_9.setGeometry(QtCore.QRect(30, 800, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_9")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "UPLOAD "))
        self.pushButton_2.setText(_translate("Dialog", "VALIDATE "))
        self.label.setText(_translate("Dialog", "Facility Type"))
        self.label_2.setText(_translate("Dialog", "Filter State"))
        self.label_3.setText(_translate("Dialog", "Filter District"))
        self.pushButton_3.setText(_translate("Dialog", "Export CSV"))
        self.label_4.setText(_translate("Dialog", "Filter Facility Name"))
        self.label_5.setText(_translate("Dialog", "Filter Month"))
        self.label_6.setText(_translate("Dialog", "Filter Year"))
        self.pushButton_4.setText(_translate("Dialog", "- All Selected -"))
        self.pushButton_5.setText(_translate("Dialog", "- All Selected -"))
        self.pushButton_6.setText(_translate("Dialog", "- All Selected -"))
        self.pushButton_7.setText(_translate("Dialog", "- All Selected -"))
        self.pushButton_8.setText(_translate("Dialog", "- All Selected -"))
        self.pushButton_9.setText(_translate("Dialog", "Reset"))

    def upload(self):
        global df_, res_dict

        # Validation for uploaded valid excel file
        try:
            # Upload file by opening filedialog
            fileName, _ = QFileDialog.getOpenFileName(
                Dialog, "Open Excel", (QtCore.QDir.homePath()), "Excel (*.xls *.xlsx)")

            # Read uploaded excel file
            df_ = pd.read_excel(fileName)

            # Converted again to csv file
            df_.to_csv("FileName.csv")

            # Read converted csv file
            df_ = pd.read_csv("FileName.csv")
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Uploaded File Error Message")
            msg.setText(
                "The file which you have uploaded is not in the valid format of excel, Please upload valid excel file")
            msg.exec()

            try:
                # Upload file by opening filedialog
                fileName, _ = QFileDialog.getOpenFileName(
                    Dialog, "Open Excel", (QtCore.QDir.homePath()), "Excel (*.xls *.xlsx)")

                # Read uploaded excel file
                df_ = pd.read_excel(fileName)

                # Converted again to csv file
                df_.to_csv("FileName.csv")

                # Read converted csv file
                df_ = pd.read_csv("FileName.csv")
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Uploaded File Error Message")
                msg.setText("Please upload valid excel file, Try again!")
                msg.exec()
                self.close()

        # Dropping last two rows
        df_.drop(df_.index[[-1, -2]], inplace=True)

        # Extracting string from 1st cell of dataframe
        str_to_extr_MonthYear = str(df_.iloc[0])

        # grab the first row for the header
        new_header = df_.iloc[1]

        # #take the data less the header row
        df_ = df_[1:]

        # set the header row as the df header
        df_.columns = new_header

        # Extracting Month , Year from string
        results = re.findall(
            r"[abceglnoprtuvyADFJMNOS|]{3}[\s-]\d{2,4}", str_to_extr_MonthYear)
        print(results)

        # Splitting Month and Year
        MYList = results[0].split('-')
        print(MYList)

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

        df_ = df_.iloc[:, 1:]

        # Temporary column to verify modified checks
        temp_columns = ['col_' + str(index)
                        for index in range(1, len(df_.columns)+1)]

        # Merging and converting temp_columns to orignal header to dictionary
        res_dict = {temp_columns[i]: df_.columns[i]
                    for i in range(len(temp_columns))}

        # Picking the temporary column names and renaming column headers with it
        df_.columns = [i for i in res_dict.keys()]

        # Orignal Header
        df_OrgHeaders = [i for i in res_dict.values()]

        # convert the set to the list and fill inside comboBox to select facility type
        list_set = df_['col_12'].tolist()
        unique_list = set(list_set)
        print(unique_list)

        self.comboBox.addItems(['-select-'])
        self.comboBox.addItems(["{0}".format(col) for col in unique_list])

        # Displaying uploaded dataframe
        self.tableView.setModel(PandasModel(df_))

        # Disabling upload Button
        self.pushButton.setDisabled(True)
        return df_

    
    # Upload file button functionality
    def loadFile(self, df_):
        return df_


    # Filtering Facility Type
    def VerifyFType(self):
        global df, FType

        df = self.loadFile(df_)

        FType = self.comboBox.currentText()
        print(FType)

        if (FType == 'Primary Health Centre'):
            print('Facility Type - ',FType)

            # Signaling PHC_Validate function i.e function where validation checks are present
            self.PHC_Validate()

        elif (FType == 'Health Sub Centre' ):
            print('Facility Type - ', FType)
            
            # Signaling HSC_Validate function i.e function where validation checks are present
            self.HSC_Validate()

        elif (FType == 'DH'):
            print('Facility Type - ',FType)
            # self.DH_Validate()

        elif (FType == 'SDH'):
            print('Facility Type - ',FType)
            # self.SDH_Validate()

        elif (FType == 'CHC'):
            print('Facility Type - ',FType)
            # self.CHC_Validate()

        else:
            raise Exception('Facility Type Name is not matching')



    #############################################################################################
    # Public Health Center Validation Rules Function
    def PHC_Validate(self):
        global df

        df = self.loadFile(df_)

        filterString = self.comboBox.currentText()
        
        df = df_.loc[df_['col_12'] == filterString]
        print(df)

        print('Entered PHC_Validate')

        # Modified Checks of PHC
        
        # 9.1.1(103) <= 4.1.1.a(56) + 4.1.1.b(57)
        def res1(df):
            if pd.isnull(df['col_103']) and pd.isnull(df['col_56']) and pd.isnull(df['col_57']):
                return 'Blank'
            elif pd.isnull(df['col_103']) or pd.isnull(df['col_56']) or pd.isnull(df['col_57']):
                if pd.isnull(df['col_59']):
                    return 'Probable Reporting Error(9.1.1 is blank)'
                elif pd.isnull(float(df['col_56']) + float(df['col_57'])):
                    return 'Inconsistent'
            elif float(df['col_103']) > float(df['col_56']) + float(df['col_57']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.1.1(23) <= 1.1(22)
        def res2(df):
            if pd.isnull(df['col_23']) and pd.isnull(df['col_22']):
                return 'Blank'
            elif pd.isnull(df['col_23']) or pd.isnull(df['col_22']):
                if pd.isnull(df['col_23']):
                    return 'Probable Reporting Error(1.1.1 is blank)'
                elif pd.isnull(df['col_22']):
                    return 'Inconsistent'
            elif float(df['col_23']) > float(df['col_22']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.2.4(27) <= 1.1(22)
        def res3(df):
            if pd.isnull(df['col_27']) and pd.isnull(df['col_22']):
                return 'Blank'
            elif pd.isnull(df['col_27']) or pd.isnull(df['col_22']):
                if pd.isnull(df['col_27']) and not pd.isnull(float(df['col_22'])):
                    return 'Probable Reporting Error'
                else:
                    return 'Probable Reporting Error'

            # If value exists for all the elements
            else:

                lhs_value = float(df['col_27'])
                rhs_value = float(df['col_22'])

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

        # 1.2.5(28) <= 1.1(22)
        def res4(df):
            if pd.isnull(df['col_28']) and pd.isnull(df['col_22']):
                return 'Blank'
            elif pd.isnull(df['col_28']) or pd.isnull(df['col_22']):
                if pd.isnull(df['col_28']) and not pd.isnull(float(df['col_22'])):
                    return 'Probable Reporting Error'
                else:
                    return 'Probable Reporting Error'

            # If value exists for all the elements
            else:

                lhs_value = float(df['col_28'])
                rhs_value = float(df['col_22'])

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

        # 1.2.7(30) <= 1.1(22)
        def res5(df):
            if pd.isnull(df['col_30']) and pd.isnull(df['col_22']):
                return 'Blank'
            elif pd.isnull(df['col_30']) or pd.isnull(df['col_22']):
                if pd.isnull(df['col_30']) and not pd.isnull(float(df['col_22'])):
                    return 'Probable Reporting Error'
                else:
                    return 'Probable Reporting Error'

            # If value exists for all the elements
            else:

                lhs_value = float(df['col_30'])
                rhs_value = float(df['col_22'])

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

        # 2.1.2(49) <= 2.1.1.a(47) + 2.1.1.b(48)
        def res6(df):
            if pd.isnull(df['col_49']) and pd.isnull(df['col_47']) and pd.isnull(df['col_48']):
                return 'Blank'
            elif pd.isnull(df['col_49']) or pd.isnull(df['col_47']) or pd.isnull(df['col_48']):
                if pd.isnull(df['col_49']):
                    return 'Probable Reporting Error(2.1.2 is blank)'
                elif pd.isnull(float(df['col_47']) + float(df['col_48'])):
                    return 'Inconsistent'
            elif float(df['col_49']) > float(df['col_47']) + float(df['col_48']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 2.1.3(50) <= 2.1.1.a(47) + 2.1.1.b(48)
        def res7(df):
            if pd.isnull(df['col_50']) and pd.isnull(df['col_47']) and pd.isnull(df['col_48']):
                return 'Blank'
            elif pd.isnull(df['col_50']) or pd.isnull(df['col_47']) or pd.isnull(df['col_48']):
                if pd.isnull(df['col_50']) and not pd.isnull(float(df['col_47'])) and pd.isnull(float(df['col_48'])):
                    return 'Probable Reporting Error'
                else:
                    return 'Probable Reporting Error'

            # If value exists for all the elements
            else:

                lhs_value = float(df['col_47'])
                rhs_value = float(df['col_48'])

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

        # 2.2.1(52) <= 2.2(51)
        def res8(df):
            if pd.isnull(df['col_52']) and pd.isnull(df['col_51']):
                return 'Blank'
            elif pd.isnull(df['col_52']) or pd.isnull(df['col_51']):
                if pd.isnull(df['col_52']):
                    return 'Probable Reporting Error(2.2.1 is blank)'
                elif pd.isnull(df['col_56']):
                    return 'Inconsistent'
            elif float(df['col_103']) > float(df['col_56']) + float(df['col_57']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 2.2(51) >= 1.3.2(34)
        def res9(df):
            if pd.isnull(df['col_51']) and pd.isnull(df['col_34']):
                return 'Blank'
            elif pd.isnull(df['col_51']) or pd.isnull(df['col_34']):
                if pd.isnull(df['col_51']):
                    return 'Probable Reporting Error(2.2 is blank)'
                elif pd.isnull(df['col_34']):
                    return 'Inconsistent'
            elif float(df['col_51']) < float(df['col_34']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.4.4(38) >= 1.4.3(37)
        def res10(df):
            if pd.isnull(df['col_38']) and pd.isnull(df['col_37']):
                return 'Blank'
            elif pd.isnull(df['col_38']) or pd.isnull(df['col_37']):
                if pd.isnull(df['col_38']) and not pd.isnull(float(df['col_37'])):
                    return 'Probable Reporting Error'
                else:
                    return 'Probable Reporting Error'

            # If value exists for all the elements
            else:

                lhs_value = float(df['col_38'])
                rhs_value = float(df['col_37'])

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

        # 1.5.1(39) <= 1.1(22)
        def res11(df):
            if pd.isnull(df['col_39']) and pd.isnull(df['col_22']):
                return 'Blank'
            elif pd.isnull(df['col_39']) or pd.isnull(df['col_22']):
                if pd.isnull(df['col_39']):
                    return 'Probable Reporting Error(1.5.1 is blank)'
                elif pd.isnull(df['col_22']):
                    return 'Inconsistent'
            elif float(df['col_39']) < float(df['col_22']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.5.2(40) <= 1.5.1(39)
        def res12(df):
            if pd.isnull(df['col_40']) and pd.isnull(df['col_39']):
                return 'Blank'
            elif pd.isnull(df['col_40']) or pd.isnull(df['col_39']):
                if pd.isnull(df['col_40']):
                    return 'Probable Reporting Error(1.5.1 is blank)'
                elif pd.isnull(df['col_39']):
                    return 'Inconsistent'
            elif float(df['col_40']) < float(df['col_39']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.5.3(41) <= 1.5.2(40)
        def res13(df):
            if pd.isnull(df['col_41']) and pd.isnull(df['col_40']):
                return 'Blank'
            elif pd.isnull(df['col_41']) or pd.isnull(df['col_40']):
                if pd.isnull(df['col_41']):
                    return 'Probable Reporting Error(1.5.3 is blank)'
                elif pd.isnull(df['col_40']):
                    return 'Inconsistent'
            elif float(df['col_41']) < float(df['col_40']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.6.1.a(42) <= 1.1(22)
        def res14(df):
            if pd.isnull(df['col_42']) and pd.isnull(df['col_22']):
                return 'Blank'
            elif pd.isnull(df['col_42']) or pd.isnull(df['col_22']):
                if pd.isnull(df['col_42']):
                    return 'Probable Reporting Error(1.6.1.a is blank)'
                elif pd.isnull(df['col_22']):
                    return 'Inconsistent'
            elif float(df['col_42']) < float(df['col_22']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.6.1.b(43) <= 1.6.1.a(42)
        def res15(df):
            if pd.isnull(df['col_43']) and pd.isnull(df['col_42']):
                return 'Blank'
            elif pd.isnull(df['col_43']) or pd.isnull(df['col_42']):
                if pd.isnull(df['col_43']):
                    return 'Probable Reporting Error(1.6.1.a is blank)'
                elif pd.isnull(df['col_42']):
                    return 'Inconsistent'
            elif float(df['col_43']) < float(df['col_42']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.6.1.c(44) <= 1.6.1.b(43)
        def res16(df):
            if pd.isnull(df['col_44']) and pd.isnull(df['col_43']):
                return 'Blank'
            elif pd.isnull(df['col_44']) or pd.isnull(df['col_43']):
                if pd.isnull(df['col_44']):
                    return 'Probable Reporting Error(1.6.1.a is blank)'
                elif pd.isnull(df['col_43']):
                    return 'Inconsistent'
            elif float(df['col_44']) > float(df['col_43']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.6.1.e(46) <= 1.6.1.d(45)
        def res17(df):
            if pd.isnull(df['col_46']) and pd.isnull(df['col_45']):
                return 'Blank'
            elif pd.isnull(df['col_46']) or pd.isnull(df['col_45']):
                if pd.isnull(df['col_46']):
                    return 'Probable Reporting Error(1.6.1.e is blank)'
                elif pd.isnull(df['col_45']):
                    return 'Inconsistent'
            elif float(df['col_46']) > float(df['col_45']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 3.1.1(55) <= 2.2(51)
        def res18(df):
            if pd.isnull(df['col_55']) and pd.isnull(df['col_51']):
                return 'Blank'
            elif pd.isnull(df['col_55']) or pd.isnull(df['col_51']):
                if pd.isnull(df['col_55']):
                    return 'Probable Reporting Error(3.1.1 is blank)'
                elif pd.isnull(df['col_51']):
                    return 'Inconsistent'
            elif float(df['col_55']) < float(df['col_51']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 3.1(54) <= 2.2(51)
        def res19(df):
            if pd.isnull(df['col_54']) and pd.isnull(df['col_51']):
                return 'Blank'
            elif pd.isnull(df['col_54']) or pd.isnull(df['col_51']):
                if pd.isnull(df['col_54']):
                    return 'Probable Reporting Error(1.6.1.a is blank)'
                elif pd.isnull(df['col_51']):
                    return 'Inconsistent'
            elif float(df['col_54']) < float(df['col_51']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 4.1.2(58) <= 4.1.1.a(56) + 4.1.1.b(57)
        def res20(df):
            if pd.isnull(df['col_58']) and pd.isnull(df['col_56']) and pd.isnull(df['col_57']):
                return 'Blank'
            elif pd.isnull(df['col_58']) or pd.isnull(df['col_56']) or pd.isnull(df['col_57']):
                if pd.isnull(df['col_58']):
                    return 'Probable Reporting Error(4.1.2 is blank)'
                elif pd.isnull(float(df['col_56']) + float(df['col_57'])):
                    return 'Inconsistent'
            elif float(df['col_58']) > float(df['col_56']) + float(df['col_57']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 4.1.1.a(56) + 4.1.1.b(57) + 4.1.3(59) >= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)
        def res21(df):
            if pd.isnull(df['col_56']) and pd.isnull(df['col_57']) and pd.isnull(df['col_59']) and pd.isnull(df['col_47']) and pd.isnull(df['col_48']) and pd.isnull(df['col_51']):
                return 'Blank'
            elif pd.isnull(df['col_56']) or pd.isnull(df['col_57']) or pd.isnull(df['col_59']) or pd.isnull(df['col_47']) or pd.isnull(df['col_48']) or pd.isnull(df['col_51']):
                if pd.isnull(df['col_56']) + pd.isnull(df['col_57']) + pd.isnull(df['col_59']):
                    return 'Inconsistent'
                elif pd.isnull(float(df['col_47']) + float(df['col_48']) + float(df['col_51'])):
                    return 'Probable Reporting Error'
            elif float(df['col_56']) + float(df['col_57']) + float(df['col_59']) <  float(df['col_47']) + float(df['col_48']) + float(df['col_51']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 4.3.2.a(63) <= 4.3.1.a(61) + 4.3.1.b(62) + 4.2(60)
        def res22(df):
            if pd.isnull(df['col_63']) and pd.isnull(df['col_61']) and pd.isnull(df['col_62']) and pd.isnull(df['col_60']):
                return 'Blank'
            elif pd.isnull(df['col_63']) or pd.isnull(df['col_61']) or pd.isnull(df['col_62']) or pd.isnull(df['col_60']):
                if pd.isnull(df['col_63']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_61']) + float(df['col_62']) + float(df['col_60']))):
                    return 'Inconsistent'
            elif float(df['col_63']) > float(df['col_61']) + float(df['col_62']) + float(df['col_60']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 4.3.2.b(64) <= 4.3.2.a(63)
        def res23(df):
            if pd.isnull(df['col_64']) and pd.isnull(df['col_63']):
                return 'Blank'
            elif pd.isnull(df['col_64']) or pd.isnull(df['col_63']):
                if pd.isnull(df['col_64']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_63']):
                    return 'Inconsistent'
            elif float(df['col_64']) > float(df['col_63']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 4.3.3(65) <= 4.3.1.a(61) + 4.3.1.b(62) + 4.2(60)
        def res24(df):
            if pd.isnull(df['col_65']) and pd.isnull(df['col_61']) and pd.isnull(df['col_62']) and pd.isnull(df['col_60']):
                return 'Blank'
            elif pd.isnull(df['col_65']) or pd.isnull(df['col_61']) or pd.isnull(df['col_62']) or pd.isnull(df['col_60']):
                if pd.isnull(df['col_65']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_61']) + float(df['col_62']) + float(df['col_60']))):
                    return 'Inconsistent'
            elif float(df['col_65']) > float(df['col_61']) + float(df['col_62']) + float(df['col_60']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 4.4.1(66) <= 4.1.1.a(56) + 4.1.1.b(57)
        def res25(df):
            if pd.isnull(df['col_66']) and pd.isnull(df['col_56']) and pd.isnull(df['col_57']):
                return 'Blank'
            elif pd.isnull(df['col_66']) or pd.isnull(df['col_56']) or pd.isnull(df['col_57']):
                if pd.isnull(df['col_66']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_56']) + float(df['col_57']))):
                    return 'Inconsistent'
            elif float(df['col_66']) > float(df['col_56']) + float(df['col_57']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 4.4.2(67) <= 4.4.1(66)
        def res26(df):
            if pd.isnull(df['col_67']) and pd.isnull(df['col_66']):
                return 'Blank'
            elif pd.isnull(df['col_67']) or pd.isnull(df['col_66']):
                if pd.isnull(df['col_67']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_66']):
                    return 'Inconsistent'
            elif float(df['col_67']) > float(df['col_66']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 4.4.3(68) <= 4.1.1.a(56) + 4.1.1.b(57)
        def res27(df):
            if pd.isnull(df['col_68']) and pd.isnull(df['col_56']) and pd.isnull(df['col_57']):
                return 'Blank'
            elif pd.isnull(df['col_68']) or pd.isnull(df['col_56']) or pd.isnull(df['col_57']):
                if pd.isnull(df['col_68']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_56']) + float(df['col_57']))):
                    return 'Inconsistent'
            elif float(df['col_68']) > float(df['col_56']) + float(df['col_57']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 6.1(70) <= 2.1.1.a(47) + 2.1.1.b(48)
        def res28(df):
            if pd.isnull(df['col_70']) and pd.isnull(df['col_47']) and pd.isnull(df['col_48']):
                return 'Blank'
            elif pd.isnull(df['col_70']) or pd.isnull(df['col_47']) or pd.isnull(df['col_48']):
                if pd.isnull(df['col_70']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_47'])) + (float(df['col_48']))):
                    return 'Inconsistent'
            elif float(df['col_70']) > float(df['col_47']) + float(df['col_48']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 6.3(72) <= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)
        def res29(df):
            if pd.isnull(df['col_72']) and pd.isnull(df['col_47']) and pd.isnull(df['col_48']) and pd.isnull(df['col_51']):
                return 'Blank'
            elif pd.isnull(df['col_72']) or pd.isnull(df['col_47']) or pd.isnull(df['col_48']) or pd.isnull(df['col_51']):
                if pd.isnull(df['col_72']) and not pd.isnull(float(df['col_47'])) and pd.isnull(float(df['col_48'])) and pd.isnull(float(df['col_51'])):
                    return 'Probable Reporting Error'
                else:
                    return 'Probable Reporting Error'

            # If value exists for all the elements
            else:

                lhs_value = float(df['col_72'])
                rhs_value = float(df['col_47']) + float(df['col_48']) + float(df['col_51']) 

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

        # 6.4(73) <= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)
        def res30(df):
            if pd.isnull(df['col_73']) and pd.isnull(df['col_47']) and pd.isnull(df['col_48']) and pd.isnull(df['col_51']):
                return 'Blank'
            elif pd.isnull(df['col_73']) or pd.isnull(df['col_47']) or pd.isnull(df['col_48']) or pd.isnull(df['col_51']):
                if pd.isnull(df['col_73']) and not pd.isnull(float(df['col_47'])) and pd.isnull(float(df['col_48'])) and pd.isnull(float(df['col_51'])):
                    return 'Probable Reporting Error'
                else:
                    return 'Probable Reporting Error'

            # If value exists for all the elements
            else:

                lhs_value = float(df['col_73'])
                rhs_value = float(df['col_47']) + float(df['col_48']) + float(df['col_51']) 

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

        # 7.2.1(76) <= 7.1.1(74)
        def res31(df):
            if pd.isnull(df['col_76']) and pd.isnull(df['col_74']):
                return 'Blank'
            elif pd.isnull(df['col_76']) or pd.isnull(df['col_74']):
                if pd.isnull(df['col_76']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_74']):
                    return 'Inconsistent'
            elif float(df['col_76']) > float(df['col_74']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 7.2.2(77) <= 7.1.2(75)
        def res32(df):
            if pd.isnull(df['col_77']) and pd.isnull(df['col_75']):
                return 'Blank'
            elif pd.isnull(df['col_77']) or pd.isnull(df['col_75']):
                if pd.isnull(df['col_77']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_75']):
                    return 'Inconsistent'
            elif float(df['col_77']) > float(df['col_75']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 8.2.3(81) <= 2.2(51)
        def res33(df):
            if pd.isnull(df['col_81']) and pd.isnull(df['col_51']):
                return 'Blank'
            elif pd.isnull(df['col_81']) or pd.isnull(df['col_51']):
                if pd.isnull(df['col_81']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_51']):
                    return 'Inconsistent'
            elif float(df['col_81']) > float(df['col_51']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 8.4(84) <= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)
        def res34(df):
            if pd.isnull(df['col_84']) and pd.isnull(df['col_61']) and pd.isnull(df['col_62']) and pd.isnull(df['col_60']):
                return 'Blank'
            elif pd.isnull(df['col_84']) or pd.isnull(df['col_61']) or pd.isnull(df['col_62']) or pd.isnull(df['col_60']):
                if pd.isnull(df['col_84']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_61']) + float(df['col_62']) + float(df['col_60']))):
                    return 'Inconsistent'
            elif float(df['col_84']) > float(df['col_61']) + float(df['col_62']) + float(df['col_60']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 8.7(87) <= 8.3(83) + 8.4(84) + 8.5(85)
        def res35(df):
            if pd.isnull(df['col_87']) and pd.isnull(df['col_83']) and pd.isnull(df['col_84']) and pd.isnull(df['col_85']):
                return 'Blank'
            elif pd.isnull(df['col_87']) or pd.isnull(df['col_83']) or pd.isnull(df['col_84']) or pd.isnull(df['col_85']):
                if pd.isnull(df['col_87']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_83']) + float(df['col_84']) + float(df['col_85']))):
                    return 'Inconsistent'
            elif float(df['col_87']) > float(df['col_83']) + float(df['col_84']) + float(df['col_85']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 8.17.1(97) <= 8.1.1(78)
        def res36(df):
            if pd.isnull(df['col_97']) and pd.isnull(df['col_78']):
                return 'Blank'
            elif pd.isnull(df['col_97']) or pd.isnull(df['col_78']):
                if pd.isnull(df['col_97']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_78']):
                    return 'Inconsistent'
            elif float(df['col_97']) > float(df['col_78']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # # 8.17.2(98) <= 8.2.1(79) + 8.2.2(80) + 8.2.3(81) + 8.2.4(82)
        # def res37(df):
        #     if pd.isnull(df['col_98']) and pd.isnull(df['col_79']) and pd.isnull(df['col_80']) and pd.isnull(df['col_81']) and pd.isnull(df['col_82']):
        #         return 'Blank'
        #     elif pd.isnull(df['col_98']) or pd.isnull(df['col_79']) or pd.isnull(df['col_80']) or pd.isnull(df['col_81']) or pd.isnull(df['col_82']):
        #         if pd.isnull(df['col_98']):
        #             return 'Probable Reporting Error'
        #         elif pd.isnull((float(df['col_79']) + float(df['col_80']) + float(df['col_81']) + float(df['col_82']))):
        #             return 'Inconsistent'
        #     elif float(df['col_98']) > float(df['col_79']) + float(df['col_80']) + float(df['col_81'] + + float(df['col_82'])):
        #         return 'Inconsistent'
        #     else:
        #         return 'consistent'
        #     return df

        # 9.1.9(111) <= 4.1.1.a(56) + 4.1.1.b(57)
        def res38(df):
            if pd.isnull(df['col_111']) and pd.isnull(df['col_56']) and pd.isnull(df['col_57']):
                return 'Blank'
            elif pd.isnull(df['col_111']) or pd.isnull(df['col_56']) or pd.isnull(df['col_57']):
                if pd.isnull(df['col_111']):
                    return 'Probable Reporting Error'
                elif pd.isnull(float(df['col_56']) + float(df['col_57'])):
                    return 'Inconsistent'
            elif float(df['col_111']) > float(df['col_56']) + float(df['col_57']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 9.1.13(115) <= 4.1.1.a(56) + 4.1.1.b(57)
        def res39(df):
            if pd.isnull(df['col_115']) and pd.isnull(df['col_56']) and pd.isnull(df['col_57']):
                return 'Blank'
            elif pd.isnull(df['col_115']) or pd.isnull(df['col_56']) or pd.isnull(df['col_57']):
                if pd.isnull(df['col_115']):
                    return 'Probable Reporting Error'
                elif pd.isnull(float(df['col_56']) + float(df['col_57'])):
                    return 'Inconsistent'
            elif float(df['col_115']) > float(df['col_56']) + float(df['col_57']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 9.2.4.a(127) + 9.2.4.b(128) <= 9.2.1(124) + 9.2.2(125)
        def res40(df):
            if pd.isnull(df['col_127']) and pd.isnull(df['col_128']) and pd.isnull(df['col_124']) and pd.isnull(df['col_125']):
                return 'Blank'
            elif pd.isnull(df['col_127']) or pd.isnull(df['col_128']) or pd.isnull(df['col_124']) or pd.isnull(df['col_125']):
                if pd.isnull(float(df['col_127']) + float(df['col_128'])):
                    return 'Probable Reporting Error'
                elif pd.isnull(float(df['col_124']) + float(df['col_125'])):
                    return 'Inconsistent'
            elif float(df['col_127']) + float(df['col_128']) > float(df['col_124']) + float(df['col_125']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 11.2.2(175) <= 11.2.1(174)
        def res41(df):
            if pd.isnull(df['col_175']) and pd.isnull(df['col_174']):
                return 'Blank'
            elif pd.isnull(df['col_175']) or pd.isnull(df['col_174']):
                if pd.isnull(df['col_175']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_174']):
                    return 'Inconsistent'
            elif float(df['col_175']) > float(df['col_174']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 12.1.2.a(180) <= 12.1.1.a(178)
        def res42(df):
            if pd.isnull(df['col_180']) and pd.isnull(df['col_178']):
                return 'Blank'
            elif pd.isnull(df['col_180']) or pd.isnull(df['col_178']):
                if pd.isnull(df['col_180']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_178']):
                    return 'Inconsistent'
            elif float(df['col_180']) > float(df['col_178']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 12.1.2.b(181) <= 12.1.1.b(179)
        def res43(df):
            if pd.isnull(df['col_181']) and pd.isnull(df['col_179']):
                return 'Blank'
            elif pd.isnull(df['col_181']) or pd.isnull(df['col_179']):
                if pd.isnull(df['col_181']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_179']):
                    return 'Inconsistent'
            elif float(df['col_181']) > float(df['col_179']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 12.1.3.a(182) <= 12.1.1.a(178)
        def res44(df):
            if pd.isnull(df['col_182']) and pd.isnull(df['col_178']):
                return 'Blank'
            elif pd.isnull(df['col_182']) or pd.isnull(df['col_178']):
                if pd.isnull(df['col_182']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_178']):
                    return 'Inconsistent'
            elif float(df['col_182']) > float(df['col_178']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 12.1.3.b(183) <= 12.1.1.b(179)
        def res45(df):
            if pd.isnull(df['col_183']) and pd.isnull(df['col_179']):
                return 'Blank'
            elif pd.isnull(df['col_183']) or pd.isnull(df['col_179']):
                if pd.isnull(df['col_183']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_179']):
                    return 'Inconsistent'
            elif float(df['col_183']) > float(df['col_179']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.2.1(194) + 14.2.2(195) >= 14.1.1(186) + 14.1.2(187) + 14.1.3(188) + 14.1.4(189) + 14.1.5(190) + 14.1.6(191) + 14.1.7(192) + 14.1.8(193)
        def res46(df):
            if pd.isnull(df['col_194']) and pd.isnull(df['col_195']) and pd.isnull(df['col_186']) and pd.isnull(df['col_187']) and pd.isnull(df['col_188']) and pd.isnull(df['col_189']) and pd.isnull(df['col_190']) and pd.isnull(df['col_191']) and pd.isnull(df['col_192']) and pd.isnull(df['col_193']):
                return 'Blank'
            elif pd.isnull(df['col_194']) or pd.isnull(df['col_195']) or pd.isnull(df['col_186']) or pd.isnull(df['col_187']) or pd.isnull(df['col_188']) or pd.isnull(df['col_189']) or pd.isnull(df['col_190']) or pd.isnull(df['col_191']) or pd.isnull(df['col_192']) or pd.isnull(df['col_193']):
                if pd.isnull(float(df['col_194']) + float(df['col_195'])):
                    return 'Inconsistent'
                elif pd.isnull(float(df['col_186']) + float(df['col_187']) + float(df['col_188']) + float(df['col_189']) + float(df['col_190']) + float(df['col_191']) + float(df['col_192']) + float(df['col_193'])):
                    return 'Probable Reporting Error'
            elif float(df['col_194']) + float(df['col_195']) < float(df['col_186']) + float(df['col_187']) + float(df['col_188']) + float(df['col_189']) + float(df['col_190']) + float(df['col_191']) + float(df['col_192']) + float(df['col_193']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.3.3(200) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)
        def res47(df):
            if pd.isnull(df['col_200']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']) and pd.isnull(df['col_199']):
                return 'Blank'
            elif pd.isnull(df['col_200']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']) or pd.isnull(df['col_82']):
                if pd.isnull(df['col_200']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199']))):
                    return 'Inconsistent'
            elif float(df['col_200']) > (float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.5.2(210) <= 14.5.1(209)
        def res48(df):
            if pd.isnull(df['col_210']) and pd.isnull(df['col_209']):
                return 'Blank'
            elif pd.isnull(df['col_210']) or pd.isnull(df['col_209']):
                if pd.isnull(df['col_210']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_209']):
                    return 'Inconsistent'
            elif float(df['col_210']) > float(df['col_209']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 15.3.3.b(230) <= 15.3.3.a(229)
        def res49(df):
            if pd.isnull(df['col_230']) and pd.isnull(df['col_229']):
                return 'Blank'
            elif pd.isnull(df['col_230']) or pd.isnull(df['col_229']):
                if pd.isnull(df['col_230']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_229']):
                    return 'Inconsistent'
            elif float(df['col_230']) > float(df['col_229']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 15.3.3.c(231) <= 15.3.3.b(230)
        def res50(df):
            if pd.isnull(df['col_231']) and pd.isnull(df['col_230']):
                return 'Blank'
            elif pd.isnull(df['col_231']) or pd.isnull(df['col_230']):
                if pd.isnull(df['col_231']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_230']):
                    return 'Inconsistent'
            elif float(df['col_231']) > float(df['col_230']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 15.4.2(237) <= 15.4.1(236)
        def res51(df):
            if pd.isnull(df['col_237']) and pd.isnull(df['col_236']):
                return 'Blank'
            elif pd.isnull(df['col_237']) or pd.isnull(df['col_236']):
                if pd.isnull(df['col_237']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_236']):
                    return 'Inconsistent'
            elif float(df['col_237']) > float(df['col_236']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 9.6.1(142) <= 9.1.1(103) + 9.1.2(104) + 9.1.3(105) + 9.1.4(106) + 9.1.5(107) + 9.1.6(108) +9.1.7(109) + 9.1.8(110) + 9.1.13(115) + 9.1.14(116) + 9.1.15(117) + 9.1.16(118) + 9.1.17(119) + 9.1.18(120) + 9.1.19(121) + 9.1.20(122) + 9.1.21(123) + 9.2.1(124) + 9.2.2(125) + 9.2.3(126) + 9.3.1(129) + 9.3.2(130) + 9.3.3(131) + 9.4.1(132) + 9.4.2(133) + 9.4.3(134) + 9.4.5(136) + 9.4.6(137) + 9.5.1(138) + 9.5.2(139) + 9.5.3(140) + 9.5.4(141)
        def res52(df):
            if pd.isnull(df['col_142']) and pd.isnull(df['col_103']) and pd.isnull(df['col_104']) and pd.isnull(df['col_105']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']) and pd.isnull(df['col_115']) and pd.isnull(df['col_116']) and pd.isnull(df['col_117']) and pd.isnull(df['col_118']) and pd.isnull(df['col_119']) and pd.isnull(df['col_120']) and pd.isnull(df['col_121']) and pd.isnull(df['col_122']) and pd.isnull(df['col_123']) and pd.isnull(df['col_124']) and pd.isnull(df['col_125']) and pd.isnull(df['col_126']) and pd.isnull(df['col_129']) and pd.isnull(df['col_130']) and pd.isnull(df['col_131']) and pd.isnull(df['col_132']) and pd.isnull(df['col_133']) and pd.isnull(df['col_134']) and pd.isnull(df['col_136']) and pd.isnull(df['col_137']) and pd.isnull(df['col_138']) and pd.isnull(df['col_139']) and pd.isnull(df['col_140']) and pd.isnull(df['col_141']) :
                return 'Blank'
            elif pd.isnull(df['col_142']) or pd.isnull(df['col_103']) or pd.isnull(df['col_104']) or pd.isnull(df['col_105']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']) or pd.isnull(df['col_115']) or pd.isnull(df['col_116']) or pd.isnull(df['col_117']) or pd.isnull(df['col_118']) or pd.isnull(df['col_119']) or pd.isnull(df['col_120']) or pd.isnull(df['col_121']) or pd.isnull(df['col_122']) or pd.isnull(df['col_123']) or pd.isnull(df['col_124']) or pd.isnull(df['col_125']) or pd.isnull(df['col_126']) or pd.isnull(df['col_129']) or pd.isnull(df['col_130']) or pd.isnull(df['col_131']) or pd.isnull(df['col_132']) or pd.isnull(df['col_133']) or pd.isnull(df['col_134']) or pd.isnull(df['col_136']) or pd.isnull(df['col_137']) or pd.isnull(df['col_138']) or pd.isnull(df['col_139']) or pd.isnull(df['col_140']) or pd.isnull(df['col_141']) :
                if pd.isnull(df['col_142']):
                    return 'Probable Reporting Error'
                elif pd.isnull(float(df['col_103']) + float(df['col_104']) + float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_129']) + float(df['col_130']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141'])):
                    return 'Inconsistent'
            elif float(df['col_142']) > float(df['col_103']) + float(df['col_104']) + float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_129']) + float(df['col_130']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df


        # 9.6.2(143) <= 9.1.1(103) + 9.1.2(104) + 9.1.3(105) + 9.1.4(106) + 9.1.5(107) + 9.1.6(108) +9.1.7(109) + 9.1.8(110) + 9.1.13(115) + 9.1.14(116) + 9.1.15(117) + 9.1.16(118) + 9.1.17(119) + 9.1.18(120) + 9.1.19(121) + 9.1.20(122) + 9.1.21(123) + 9.2.1(124) + 9.2.2(125) + 9.2.3(126) + 9.3.1(129) + 9.3.2(130) + 9.3.3(131) + 9.4.1(132) + 9.4.2(133) + 9.4.3(134) + 9.4.5(136) + 9.4.6(137) + 9.5.1(138) + 9.5.2(139) + 9.5.3(140) + 9.5.4(141)
        def res53(df):
            if pd.isnull(df['col_143']) and pd.isnull(df['col_103']) and pd.isnull(df['col_104']) and pd.isnull(df['col_105']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']) and pd.isnull(df['col_115']) and pd.isnull(df['col_116']) and pd.isnull(df['col_117']) and pd.isnull(df['col_118']) and pd.isnull(df['col_119']) and pd.isnull(df['col_120']) and pd.isnull(df['col_121']) and pd.isnull(df['col_122']) and pd.isnull(df['col_123']) and pd.isnull(df['col_124']) and pd.isnull(df['col_125']) and pd.isnull(df['col_126']) and pd.isnull(df['col_129']) and pd.isnull(df['col_130']) and pd.isnull(df['col_131']) and pd.isnull(df['col_132']) and pd.isnull(df['col_133']) and pd.isnull(df['col_134']) and pd.isnull(df['col_136']) and pd.isnull(df['col_137']) and pd.isnull(df['col_138']) and pd.isnull(df['col_139']) and pd.isnull(df['col_140']) and pd.isnull(df['col_141']) :
                return 'Blank'
            elif pd.isnull(df['col_143']) or pd.isnull(df['col_103']) or pd.isnull(df['col_104']) or pd.isnull(df['col_105']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']) or pd.isnull(df['col_115']) or pd.isnull(df['col_116']) or pd.isnull(df['col_117']) or pd.isnull(df['col_118']) or pd.isnull(df['col_119']) or pd.isnull(df['col_120']) or pd.isnull(df['col_121']) or pd.isnull(df['col_122']) or pd.isnull(df['col_123']) or pd.isnull(df['col_124']) or pd.isnull(df['col_125']) or pd.isnull(df['col_126']) or pd.isnull(df['col_129']) or pd.isnull(df['col_130']) or pd.isnull(df['col_131']) or pd.isnull(df['col_132']) or pd.isnull(df['col_133']) or pd.isnull(df['col_134']) or pd.isnull(df['col_136']) or pd.isnull(df['col_137']) or pd.isnull(df['col_138']) or pd.isnull(df['col_139']) or pd.isnull(df['col_140']) or pd.isnull(df['col_141']) :
                if pd.isnull(df['col_143']):
                    return 'Probable Reporting Error'
                elif pd.isnull(float(df['col_103']) + float(df['col_104']) + float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_129']) + float(df['col_130']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141'])):
                    return 'Inconsistent'
            elif float(df['col_143']) > float(df['col_103']) + float(df['col_104']) + float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_129']) + float(df['col_130']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 9.6.3(144) <= 9.1.1(103) + 9.1.2(104) + 9.1.3(105) + 9.1.4(106) + 9.1.5(107) + 9.1.6(108) +9.1.7(109) + 9.1.8(110) + 9.1.13(115) + 9.1.14(116) + 9.1.15(117) + 9.1.16(118) + 9.1.17(119) + 9.1.18(120) + 9.1.19(121) + 9.1.20(122) + 9.1.21(123) + 9.2.1(124) + 9.2.2(125) + 9.2.3(126) + 9.3.1(129) + 9.3.2(130) + 9.3.3(131) + 9.4.1(132) + 9.4.2(133) + 9.4.3(134) + 9.4.5(136) + 9.4.6(137) + 9.5.1(138) + 9.5.2(139) + 9.5.3(140) + 9.5.4(141)
        def res54(df):
            if pd.isnull(df['col_144']) and pd.isnull(df['col_103']) and pd.isnull(df['col_104']) and pd.isnull(df['col_105']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']) and pd.isnull(df['col_115']) and pd.isnull(df['col_116']) and pd.isnull(df['col_117']) and pd.isnull(df['col_118']) and pd.isnull(df['col_119']) and pd.isnull(df['col_120']) and pd.isnull(df['col_121']) and pd.isnull(df['col_122']) and pd.isnull(df['col_123']) and pd.isnull(df['col_124']) and pd.isnull(df['col_125']) and pd.isnull(df['col_126']) and pd.isnull(df['col_129']) and pd.isnull(df['col_130']) and pd.isnull(df['col_131']) and pd.isnull(df['col_132']) and pd.isnull(df['col_133']) and pd.isnull(df['col_134']) and pd.isnull(df['col_136']) and pd.isnull(df['col_137']) and pd.isnull(df['col_138']) and pd.isnull(df['col_139']) and pd.isnull(df['col_140']) and pd.isnull(df['col_141']) :
                return 'Blank'
            elif pd.isnull(df['col_144']) or pd.isnull(df['col_103']) or pd.isnull(df['col_104']) or pd.isnull(df['col_105']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']) or pd.isnull(df['col_115']) or pd.isnull(df['col_116']) or pd.isnull(df['col_117']) or pd.isnull(df['col_118']) or pd.isnull(df['col_119']) or pd.isnull(df['col_120']) or pd.isnull(df['col_121']) or pd.isnull(df['col_122']) or pd.isnull(df['col_123']) or pd.isnull(df['col_124']) or pd.isnull(df['col_125']) or pd.isnull(df['col_126']) or pd.isnull(df['col_129']) or pd.isnull(df['col_130']) or pd.isnull(df['col_131']) or pd.isnull(df['col_132']) or pd.isnull(df['col_133']) or pd.isnull(df['col_134']) or pd.isnull(df['col_136']) or pd.isnull(df['col_137']) or pd.isnull(df['col_138']) or pd.isnull(df['col_139']) or pd.isnull(df['col_140']) or pd.isnull(df['col_141']) :
                if pd.isnull(df['col_144']):
                    return 'Probable Reporting Error'
                elif pd.isnull(float(df['col_103']) + float(df['col_104']) + float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_129']) + float(df['col_130']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141'])):
                    return 'Inconsistent'
            elif float(df['col_144']) > float(df['col_103']) + float(df['col_104']) + float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_129']) + float(df['col_130']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.3.1.a(33) <= 1.3.1(32)
        def res55(df):
            if pd.isnull(df['col_33']) and pd.isnull(df['col_32']):
                return 'Blank'
            elif pd.isnull(df['col_33']) or pd.isnull(df['col_32']):
                if pd.isnull(df['col_33']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_32']):
                    return 'Inconsistent'
            elif float(df['col_33']) > float(df['col_32']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 9.7.2(146) <= 9.7.1(145)
        def res56(df):
            if pd.isnull(df['col_146']) and pd.isnull(df['col_145']):
                return 'Blank'
            elif pd.isnull(df['col_146']) or pd.isnull(df['col_145']):
                if pd.isnull(df['col_146']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_145']):
                    return 'Inconsistent'
            elif float(df['col_146']) > float(df['col_145']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 9.7.3(147) <= 9.7.2(146)
        def res57(df):
            if pd.isnull(df['col_147']) and pd.isnull(df['col_146']):
                return 'Blank'
            elif pd.isnull(df['col_147']) or pd.isnull(df['col_146']):
                if pd.isnull(df['col_147']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_146']):
                    return 'Inconsistent'
            elif float(df['col_147']) > float(df['col_146']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 11.1.1.b(169) <= 11.1.1.a(168)
        def res58(df):
            if pd.isnull(df['col_169']) and pd.isnull(df['col_168']):
                return 'Blank'
            elif pd.isnull(df['col_169']) or pd.isnull(df['col_168']):
                if pd.isnull(df['col_169']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_168']):
                    return 'Inconsistent'
            elif float(df['col_169']) > float(df['col_168']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 11.1.1.c(170) <= 11.1.1.a(168)
        def res59(df):
            if pd.isnull(df['col_170']) and pd.isnull(df['col_168']):
                return 'Blank'
            elif pd.isnull(df['col_170']) or pd.isnull(df['col_168']):
                if pd.isnull(df['col_170']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_168']):
                    return 'Inconsistent'
            elif float(df['col_170']) > float(df['col_168']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 11.1.2.b(171) <= 11.1.1.a(168)
        def res60(df):
            if pd.isnull(df['col_170']) and pd.isnull(df['col_168']):
                return 'Blank'
            elif pd.isnull(df['col_170']) or pd.isnull(df['col_168']):
                if pd.isnull(df['col_170']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_168']):
                    return 'Inconsistent'
            elif float(df['col_170']) > float(df['col_168']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 11.1.2.c(173) <= 11.1.2.a(171)
        def res61(df):
            if pd.isnull(df['col_173']) and pd.isnull(df['col_171']):
                return 'Blank'
            elif pd.isnull(df['col_173']) or pd.isnull(df['col_171']):
                if pd.isnull(df['col_173']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_171']):
                    return 'Inconsistent'
            elif float(df['col_173']) > float(df['col_171']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.4.1(201) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)
        def res62(df):
            if pd.isnull(df['col_201']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']) and pd.isnull(df['col_199']):
                return 'Blank'
            elif pd.isnull(df['col_201']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']) or pd.isnull(df['col_199']):
                if pd.isnull(df['col_201']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199']))):
                    return 'Inconsistent'
            elif float(df['col_201']) > (float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.4.2(202) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)
        def res63(df):
            if pd.isnull(df['col_202']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']) and pd.isnull(df['col_199']):
                return 'Blank'
            elif pd.isnull(df['col_202']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']) or pd.isnull(df['col_199']):
                if pd.isnull(df['col_202']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199']))):
                    return 'Inconsistent'
            elif float(df['col_202']) > (float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.4.3(203) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)
        def res64(df):
            if pd.isnull(df['col_203']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']) and pd.isnull(df['col_199']):
                return 'Blank'
            elif pd.isnull(df['col_203']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']) or pd.isnull(df['col_199']):
                if pd.isnull(df['col_203']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199']))):
                    return 'Inconsistent'
            elif float(df['col_203']) > (float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.4.4(204) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)
        def res65(df):
            if pd.isnull(df['col_204']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']) and pd.isnull(df['col_199']):
                return 'Blank'
            elif pd.isnull(df['col_204']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']) or pd.isnull(df['col_199']):
                if pd.isnull(df['col_204']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199']))):
                    return 'Inconsistent'
            elif float(df['col_204']) > (float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.4.5(205) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)
        def res66(df):
            if pd.isnull(df['col_205']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']) and pd.isnull(df['col_199']):
                return 'Blank'
            elif pd.isnull(df['col_205']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']) or pd.isnull(df['col_199']):
                if pd.isnull(df['col_205']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199']))):
                    return 'Inconsistent'
            elif float(df['col_205']) > (float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.4.6(206) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)
        def res67(df):
            if pd.isnull(df['col_206']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']) and pd.isnull(df['col_199']):
                return 'Blank'
            elif pd.isnull(df['col_206']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']) or pd.isnull(df['col_199']):
                if pd.isnull(df['col_206']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199']))):
                    return 'Inconsistent'
            elif float(df['col_206']) > (float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.4.7(207) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199))
        def res68(df):
            if pd.isnull(df['col_207']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']) and pd.isnull(df['col_199']):
                return 'Blank'
            elif pd.isnull(df['col_207']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']) or pd.isnull(df['col_199']):
                if pd.isnull(df['col_207']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199']))):
                    return 'Inconsistent'
            elif float(df['col_207']) > (float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.4.8(208) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)
        def res69(df):
            if pd.isnull(df['col_208']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']) and pd.isnull(df['col_199']):
                return 'Blank'
            elif pd.isnull(df['col_208']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']) or pd.isnull(df['col_199']):
                if pd.isnull(df['col_208']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199']))):
                    return 'Inconsistent'
            elif float(df['col_208']) > (float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.6.1(214) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)
        def res70(df):
            if pd.isnull(df['col_214']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']) and pd.isnull(df['col_199']):
                return 'Blank'
            elif pd.isnull(df['col_214']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']) or pd.isnull(df['col_199']):
                if pd.isnull(df['col_214']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199']))):
                    return 'Inconsistent'
            elif float(df['col_214']) > (float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.6.2(215) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)
        def res71(df):
            if pd.isnull(df['col_215']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']) and pd.isnull(df['col_199']):
                return 'Blank'
            elif pd.isnull(df['col_215']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']) or pd.isnull(df['col_199']):
                if pd.isnull(df['col_215']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199']))):
                    return 'Inconsistent'
            elif float(df['col_215']) > (float(df['col_196']) + float(df['col_197']) + float(df['col_198']) + float(df['col_199'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 14.9.2(219) <= 14.9.1(218)
        def res72(df):
            if pd.isnull(df['col_219']) and pd.isnull(df['col_218']):
                return 'Blank'
            elif pd.isnull(df['col_219']) or pd.isnull(df['col_218']):
                if pd.isnull(df['col_219']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_218']):
                    return 'Inconsistent'
            elif float(df['col_219']) > float(df['col_218']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 15.2.2(224) <= 15.2.1(223)
        def res73(df):
            if pd.isnull(df['col_224']) and pd.isnull(df['col_223']):
                return 'Blank'
            elif pd.isnull(df['col_224']) or pd.isnull(df['col_223']):
                if pd.isnull(df['col_224']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_223']):
                    return 'Inconsistent'
            elif float(df['col_224']) > float(df['col_223']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 15.3.1.b(226) <= 15.3.1.a(225)
        def res74(df):
            if pd.isnull(df['col_226']) and pd.isnull(df['col_225']):
                return 'Blank'
            elif pd.isnull(df['col_226']) or pd.isnull(df['col_225']):
                if pd.isnull(df['col_226']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_225']):
                    return 'Inconsistent'
            elif float(df['col_226']) > float(df['col_225']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 15.3.2.b(228) <= 15.3.2.a(227)
        def res75(df):
            if pd.isnull(df['col_228']) and pd.isnull(df['col_227']):
                return 'Blank'
            elif pd.isnull(df['col_228']) or pd.isnull(df['col_227']):
                if pd.isnull(df['col_228']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_227']):
                    return 'Inconsistent'
            elif float(df['col_228']) > float(df['col_227']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 15.3.4.b(233) <= 15.3.4.a(232)
        def res76(df):
            if pd.isnull(df['col_233']) and pd.isnull(df['col_232']):
                return 'Blank'
            elif pd.isnull(df['col_233']) or pd.isnull(df['col_232']):
                if pd.isnull(df['col_233']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_232']):
                    return 'Inconsistent'
            elif float(df['col_232']) > float(df['col_233']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 15.3.4.d(235) <= 15.3.4.c(234)
        def res77(df):
            if pd.isnull(df['col_235']) and pd.isnull(df['col_234']):
                return 'Blank'
            elif pd.isnull(df['col_235']) or pd.isnull(df['col_234']):
                if pd.isnull(df['col_235']):
                    return 'Probable Reporting Error'
                elif pd.isnull(df['col_234']):
                    return 'Inconsistent'
            elif float(df['col_235']) > float(df['col_234']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 9.1.2(104) <= 4.1.1.a(56) + 4.1.1.b(57)
        def res78(df):
            if pd.isnull(df['col_104']) and pd.isnull(df['col_56']) and pd.isnull(df['col_57']):
                return 'Blank'
            elif pd.isnull(df['col_104']) or pd.isnull(df['col_56']) or pd.isnull(df['col_57']):
                if pd.isnull(df['col_104']):
                    return 'Probable Reporting Error'
                elif pd.isnull((float(df['col_56']) + float(df['col_57']))):
                    return 'Inconsistent'
            elif float(df['col_104']) > (float(df['col_56']) + float(df['col_57'])):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df



        # To count summary of the Modified Checks
        # =======================================

        df['9.1.1(103) <= 4.1.1.a(56) + 4.1.1.b(57)'] = df.apply(res1, axis=1)
        df['1.1.1(23) <= 1.1(22)'] = df.apply(res2, axis=1)
        df['1.2.4(27) <= 1.1(22)'] = df.apply(res3, axis=1)
        df['1.2.5(28) <= 1.1(22)'] = df.apply(res4, axis=1)
        df['1.2.7(30) <= 1.1(22)'] = df.apply(res5, axis=1)
        df['2.1.2(49) <= 2.1.1.a(47) + 2.1.1.b(48)'] = df.apply(res6, axis=1)
        df['2.1.3(50) <= 2.1.1.a(47) + 2.1.1.b(48)'] = df.apply(res7, axis=1)
        df['2.2.1(52) <= 2.2(51)'] = df.apply(res8, axis=1)
        df['2.2(51) >= 1.3.2(34)'] = df.apply(res9, axis=1)
        df['1.4.4(38) >= 1.4.3(37)'] = df.apply(res10, axis=1)
        df['1.5.1(39) <= 1.1(22)'] = df.apply(res11, axis=1)
        df['1.5.2(40) <= 1.5.1(39)'] = df.apply(res12, axis=1)
        df['1.5.3(41) <= 1.5.2(40)'] = df.apply(res13, axis=1)
        df['1.6.1.a(42) <= 1.1(22)'] = df.apply(res14, axis=1)
        df['1.6.1.b(43) <= 1.6.1.a(42)'] = df.apply(res15, axis=1)
        df['1.6.1.c(44) <= 1.6.1.b(43))'] = df.apply(res16, axis=1)
        df['1.6.1.e(46) <= 1.6.1.d(45)'] = df.apply(res17, axis=1)
        df['3.1.1(55) <= 2.2(51)'] = df.apply(res18, axis=1)
        df['3.1(54) <= 2.2(51)'] = df.apply(res19, axis=1)
        df['4.1.2(58) <= 4.1.1.a(56) + 4.1.1.b(57)'] = df.apply(res20, axis=1)
        df['4.1.1.a(56) + 4.1.1.b(57) + 4.1.3(59) >= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)'] = df.apply(res21, axis=1)
        df['4.3.2.a(63) <= 4.3.1.a(61) + 4.3.1.b(62) + 4.2(60)'] = df.apply(res22, axis=1)
        df['4.3.2.b(64) <= 4.3.2.a(63)'] = df.apply(res23, axis=1)
        df['4.3.3(65) <= 4.3.1.a(61) + 4.3.1.b(62) + 4.2(60)'] = df.apply(res24, axis=1)
        df['4.4.1(66) <= 4.1.1.a(56) + 4.1.1.b(57)'] = df.apply(res25, axis=1)
        df['4.4.2(67) <= 4.4.1(66)'] = df.apply(res26, axis=1)
        df['4.4.3(68) <= 4.1.1.a(56) + 4.1.1.b(57)'] = df.apply(res27, axis=1)
        df['6.1(70) <= 2.1.1.a(47) + 2.1.1.b(48)'] = df.apply(res28, axis=1)
        df['6.3(72) <= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)'] = df.apply(res29, axis=1)
        df['6.4(73) <= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)'] = df.apply(res30, axis=1)
        df['7.2.1(76) <= 7.1.1(74)'] = df.apply(res31, axis=1)
        df['7.2.2(77) <= 7.1.2(75)'] = df.apply(res32, axis=1)
        df['8.2.3(81) <= 2.2(51)'] = df.apply(res33, axis=1)
        df['8.4(84) <= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)'] = df.apply(res34, axis=1)
        df['8.7(87) <= 8.3(83) + 8.4(84) + 8.5(85)'] = df.apply(res35, axis=1)
        df['8.17.1(97) <= 8.1.1(78)'] = df.apply(res36, axis=1)
        #df['8.17.2(98) <= 8.2.1(79) + 8.2.2(80) + 8.2.3(81) + 8.2.4(82)'] = df.apply(res37, axis=1)
        df['9.1.9(111) <= 4.1.1.a(56) + 4.1.1.b(57)'] = df.apply(res38, axis=1)
        df['9.1.13(115) <= 4.1.1.a(56) + 4.1.1.b(57)'] = df.apply(res39, axis=1)
        df['9.2.4.a(127) + 9.2.4.b(128) <= 9.2.1(124) + 9.2.2(125)'] = df.apply(res40, axis=1)
        df['11.2.2(175) <= 11.2.1(174)'] = df.apply(res41, axis=1)
        df['12.1.2.a(180) <= 12.1.1.a(178)'] = df.apply(res42, axis=1)
        df['12.1.2.b(181) <= 12.1.1.b(179)'] = df.apply(res43, axis=1)
        df['12.1.3.a(182) <= 12.1.1.a(178)'] = df.apply(res44, axis=1)
        df['12.1.3.b(183) <= 12.1.1.b(179)'] = df.apply(res45, axis=1)
        df['14.2.1(194) + 14.2.2(195) >= 14.1.1(186) + 14.1.2(187) + 14.1.3(188) + 14.1.4(189) + 14.1.5(190) + 14.1.6(191) + 14.1.7(192) + 14.1.8(193)'] = df.apply(res46, axis=1)
        df['14.3.3(200) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'] = df.apply(res47, axis=1)
        df['14.5.2(210) <= 14.5.1(209)'] = df.apply(res48, axis=1)
        df['15.3.3.b(230) <= 15.3.3.a(229)'] = df.apply(res49, axis=1)
        df['15.3.3.c(231) <= 15.3.3.b(230))'] = df.apply(res50, axis=1)
        df['15.4.2(237) <= 15.4.1(236)'] = df.apply(res51, axis=1)
        df['9.6.1(142) <= 9.1.1(103) + 9.1.2(104) + 9.1.3(105) + 9.1.4(106) + 9.1.5(107) + 9.1.6(108) +9.1.7(109) + 9.1.8(110) + 9.1.13(115) + 9.1.14(116) + 9.1.15(117) + 9.1.16(118) + 9.1.17(119) + 9.1.18(120) + 9.1.19(121) + 9.1.20(122) + 9.1.21(123) + 9.2.1(124) + 9.2.2(125) + 9.2.3(126) + 9.3.1(129) + 9.3.2(130) + 9.3.3(131) + 9.4.1(132) + 9.4.2(133) + 9.4.3(134) + 9.4.5(136) + 9.4.6(137) + 9.5.1(138) + 9.5.2(139) + 9.5.3(140) + 9.5.4(141)'] = df.apply(res52, axis=1)
        df['9.6.2(143) <= 9.1.1(103) + 9.1.2(104) + 9.1.3(105) + 9.1.4(106) + 9.1.5(107) + 9.1.6(108) +9.1.7(109) + 9.1.8(110) + 9.1.13(115) + 9.1.14(116) + 9.1.15(117) + 9.1.16(118) + 9.1.17(119) + 9.1.18(120) + 9.1.19(121) + 9.1.20(122) + 9.1.21(123) + 9.2.1(124) + 9.2.2(125) + 9.2.3(126) + 9.3.1(129) + 9.3.2(130) + 9.3.3(131) + 9.4.1(132) + 9.4.2(133) + 9.4.3(134) + 9.4.5(136) + 9.4.6(137) + 9.5.1(138) + 9.5.2(139) + 9.5.3(140) + 9.5.4(141)'] = df.apply(res53, axis=1)
        df['9.6.3(144) <= 9.1.1(103) + 9.1.2(104) + 9.1.3(105) + 9.1.4(106) + 9.1.5(107) + 9.1.6(108) +9.1.7(109) + 9.1.8(110) + 9.1.13(115) + 9.1.14(116) + 9.1.15(117) + 9.1.16(118) + 9.1.17(119) + 9.1.18(120) + 9.1.19(121) + 9.1.20(122) + 9.1.21(123) + 9.2.1(124) + 9.2.2(125) + 9.2.3(126) + 9.3.1(129) + 9.3.2(130) + 9.3.3(131) + 9.4.1(132) + 9.4.2(133) + 9.4.3(134) + 9.4.5(136) + 9.4.6(137) + 9.5.1(138) + 9.5.2(139) + 9.5.3(140) + 9.5.4(141)'] = df.apply(res54, axis=1)
        df['1.3.1.a(33) <= 1.3.1(32)'] = df.apply(res55, axis=1)
        df['9.7.2(146) <= 9.7.1(145)'] = df.apply(res56, axis=1)
        df['9.7.3(147) <= 9.7.2(146)'] = df.apply(res57, axis=1)
        df['11.1.1.b(169) <= 11.1.1.a(168)'] = df.apply(res58, axis=1)
        df['11.1.1.c(170) <= 11.1.1.a(168)'] = df.apply(res59, axis=1)
        df['11.1.2.b(171) <= 11.1.1.a(168)'] = df.apply(res60, axis=1)
        df['11.1.2.c(173) <= 11.1.2.a(171)'] = df.apply(res61, axis=1)
        df['14.4.1(201) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'] = df.apply(res62, axis=1)
        df['14.4.2(202) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199))'] = df.apply(res63, axis=1)
        df['14.4.3(203) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'] = df.apply(res64, axis=1)
        df['14.4.4(204) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'] = df.apply(res65, axis=1)
        df['14.4.5(205) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'] = df.apply(res66, axis=1)
        df['14.4.6(206) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'] = df.apply(res67, axis=1)
        df['14.4.7(207) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'] = df.apply(res68, axis=1)
        df['14.4.8(208) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'] = df.apply(res69, axis=1)
        df['14.6.1(214) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'] = df.apply(res70, axis=1)
        df['14.6.2(215) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'] = df.apply(res71, axis=1)
        df['14.9.2(219) <= 14.9.1(218)'] = df.apply(res72, axis=1)
        df['15.2.2(224) <= 15.2.1(223)'] = df.apply(res73, axis=1)
        df['15.3.1.b(226) <= 15.3.1.a(225)'] = df.apply(res74, axis=1)
        df['15.3.2.b(228) <= 15.3.2.a(227))'] = df.apply(res75, axis=1)
        df['15.3.4.b(233) <= 15.3.4.a(232)'] = df.apply(res76, axis=1)
        df['15.3.4.d(235) <= 15.3.4.c(234)'] = df.apply(res77, axis=1)
        df['9.1.2(104) <= 4.1.1.a(56) + 4.1.1.b(57)'] = df.apply(res78, axis=1)

        # Concatenating above renamed columns
        # ===================================
        df = pd.concat([df['9.1.1(103) <= 4.1.1.a(56) + 4.1.1.b(57)'],
                        df['1.1.1(23) <= 1.1(22)'],
                        df['1.2.4(27) <= 1.1(22)'],
                        df['1.2.5(28) <= 1.1(22)'],
                        df['1.2.7(30) <= 1.1(22)'],
                        df['2.1.2(49) <= 2.1.1.a(47) + 2.1.1.b(48)'],
                        df['2.1.3(50) <= 2.1.1.a(47) + 2.1.1.b(48)'],
                        df['2.2.1(52) <= 2.2(51)'],
                        df['2.2(51) >= 1.3.2(34)'],
                        df['1.4.4(38) >= 1.4.3(37)'],
                        df['1.5.1(39) <= 1.1(22)'],
                        df['1.5.2(40) <= 1.5.1(39)'],
                        df['1.5.3(41) <= 1.5.2(40)'],
                        df['1.6.1.a(42) <= 1.1(22)'],
                        df['1.6.1.b(43) <= 1.6.1.a(42)'],
                        df['1.6.1.c(44) <= 1.6.1.b(43))'],
                        df['1.6.1.e(46) <= 1.6.1.d(45)'],
                        df['3.1.1(55) <= 2.2(51)'],
                        df['3.1(54) <= 2.2(51)'],
                        df['4.1.2(58) <= 4.1.1.a(56) + 4.1.1.b(57)'],
                        df['4.1.1.a(56) + 4.1.1.b(57) + 4.1.3(59) >= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)'],
                        df['4.3.2.a(63) <= 4.3.1.a(61) + 4.3.1.b(62) + 4.2(60)'],
                        df['4.3.2.b(64) <= 4.3.2.a(63)'],
                        df['4.3.3(65) <= 4.3.1.a(61) + 4.3.1.b(62) + 4.2(60)'],
                        df['4.4.1(66) <= 4.1.1.a(56) + 4.1.1.b(57)'],
                        df['4.4.2(67) <= 4.4.1(66)'],
                        df['4.4.3(68) <= 4.1.1.a(56) + 4.1.1.b(57)'],
                        df['6.1(70) <= 2.1.1.a(47) + 2.1.1.b(48)'],
                        df['6.3(72) <= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)'],
                        df['6.4(73) <= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)'],
                        df['7.2.1(76) <= 7.1.1(74)'],
                        df['7.2.2(77) <= 7.1.2(75)'],
                        df['8.2.3(81) <= 2.2(51)'],
                        df['8.4(84) <= 2.1.1.a(47) + 2.1.1.b(48) + 2.2(51)'],
                        df['8.7(87) <= 8.3(83) + 8.4(84) + 8.5(85)'],
                        df['8.17.1(97) <= 8.1.1(78)'],
                        #df['8.17.2(98) <= 8.2.1(79) + 8.2.2(80) + 8.2.3(81) + 8.2.4(82)'],
                        df['9.1.9(111) <= 4.1.1.a(56) + 4.1.1.b(57)'],
                        df['9.1.13(115) <= 4.1.1.a(56) + 4.1.1.b(57)'],
                        df['9.2.4.a(127) + 9.2.4.b(128) <= 9.2.1(124) + 9.2.2(125)'],
                        df['11.2.2(175) <= 11.2.1(174)'],
                        df['12.1.2.a(180) <= 12.1.1.a(178)'],
                        df['12.1.2.b(181) <= 12.1.1.b(179)'],
                        df['12.1.3.a(182) <= 12.1.1.a(178)'],
                        df['12.1.3.b(183) <= 12.1.1.b(179)'],
                        df['14.2.1(194) + 14.2.2(195) >= 14.1.1(186) + 14.1.2(187) + 14.1.3(188) + 14.1.4(189) + 14.1.5(190) + 14.1.6(191) + 14.1.7(192) + 14.1.8(193)'],
                        df['14.3.3(200) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'],
                        df['14.5.2(210) <= 14.5.1(209)'],
                        df['15.3.3.b(230) <= 15.3.3.a(229)'],
                        df['15.3.3.c(231) <= 15.3.3.b(230))'],
                        df['15.4.2(237) <= 15.4.1(236)'],
                        df['9.6.1(142) <= 9.1.1(103) + 9.1.2(104) + 9.1.3(105) + 9.1.4(106) + 9.1.5(107) + 9.1.6(108) +9.1.7(109) + 9.1.8(110) + 9.1.13(115) + 9.1.14(116) + 9.1.15(117) + 9.1.16(118) + 9.1.17(119) + 9.1.18(120) + 9.1.19(121) + 9.1.20(122) + 9.1.21(123) + 9.2.1(124) + 9.2.2(125) + 9.2.3(126) + 9.3.1(129) + 9.3.2(130) + 9.3.3(131) + 9.4.1(132) + 9.4.2(133) + 9.4.3(134) + 9.4.5(136) + 9.4.6(137) + 9.5.1(138) + 9.5.2(139) + 9.5.3(140) + 9.5.4(141)'],
                        df['9.6.2(143) <= 9.1.1(103) + 9.1.2(104) + 9.1.3(105) + 9.1.4(106) + 9.1.5(107) + 9.1.6(108) +9.1.7(109) + 9.1.8(110) + 9.1.13(115) + 9.1.14(116) + 9.1.15(117) + 9.1.16(118) + 9.1.17(119) + 9.1.18(120) + 9.1.19(121) + 9.1.20(122) + 9.1.21(123) + 9.2.1(124) + 9.2.2(125) + 9.2.3(126) + 9.3.1(129) + 9.3.2(130) + 9.3.3(131) + 9.4.1(132) + 9.4.2(133) + 9.4.3(134) + 9.4.5(136) + 9.4.6(137) + 9.5.1(138) + 9.5.2(139) + 9.5.3(140) + 9.5.4(141)'],
                        df['9.6.3(144) <= 9.1.1(103) + 9.1.2(104) + 9.1.3(105) + 9.1.4(106) + 9.1.5(107) + 9.1.6(108) +9.1.7(109) + 9.1.8(110) + 9.1.13(115) + 9.1.14(116) + 9.1.15(117) + 9.1.16(118) + 9.1.17(119) + 9.1.18(120) + 9.1.19(121) + 9.1.20(122) + 9.1.21(123) + 9.2.1(124) + 9.2.2(125) + 9.2.3(126) + 9.3.1(129) + 9.3.2(130) + 9.3.3(131) + 9.4.1(132) + 9.4.2(133) + 9.4.3(134) + 9.4.5(136) + 9.4.6(137) + 9.5.1(138) + 9.5.2(139) + 9.5.3(140) + 9.5.4(141)'],
                        df['1.3.1.a(33) <= 1.3.1(32)'],
                        df['9.7.2(146) <= 9.7.1(145)'],
                        df['9.7.3(147) <= 9.7.2(146)'],
                        df['11.1.1.b(169) <= 11.1.1.a(168)'],
                        df['11.1.1.c(170) <= 11.1.1.a(168)'],
                        df['11.1.2.b(171) <= 11.1.1.a(168)'],
                        df['11.1.2.c(173) <= 11.1.2.a(171)'],
                        df['14.4.1(201) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'],
                        df['14.4.2(202) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199))'],
                        df['14.4.3(203) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'],
                        df['14.4.4(204) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'],
                        df['14.4.5(205) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'],
                        df['14.4.6(206) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'],
                        df['14.4.7(207) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'],
                        df['14.4.8(208) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'],
                        df['14.6.1(214) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'],
                        df['14.6.2(215) <= 14.3.1.a(196) + 14.3.1.b(197) + 14.3.2.a(198) + 14.3.2.b(199)'],
                        df['14.9.2(219) <= 14.9.1(218)'],
                        df['15.2.2(224) <= 15.2.1(223)'],
                        df['15.3.1.b(226) <= 15.3.1.a(225)'],
                        df['15.3.2.b(228) <= 15.3.2.a(227))'],
                        df['15.3.4.b(233) <= 15.3.4.a(232)'],
                        df['15.3.4.d(235) <= 15.3.4.c(234)'],
                        df['9.1.2(104) <= 4.1.1.a(56) + 4.1.1.b(57)']], axis=1)

        # Mergining current result of modified checks with original dataframe and displaying it on screen
        frames = [df_, df]
        print(frames)
        df = pd.concat(frames, axis=1, sort=False)
        #df = df.dropna(axis=0, subset=['col_2'])
        self.tableView.setModel(PandasModel(df))

        msg = QMessageBox()
        msg.setWindowTitle("Validation Completion Message")
        msg.setText("Validation Complete")
        msg.exec()

        return df



    # Validation for HSC
    def HSC_Validate(self):
        global df, table_result

        filterString = self.comboBox.currentText()
        
        df = df_.loc[df_['col_12'] == filterString]
        print(df)
       
        print('Entered HSC_Validate')

        # Modified Checks of HSC

        # 4.3 (56) <= 2.1.1.a (39) + 2.1.1.b (40) + 2.2 (43) (For recurring data items)
        def res1(df):

            # If all elements are null
            if pd.isnull(df['col_56']) and pd.isnull(df['col_39']) and pd.isnull(df['col_40']) and pd.isnull(df['col_43']):
                return 'Blank'

            # If any one element is null
            elif pd.isnull(df['col_56']) or pd.isnull(df['col_39']) or pd.isnull(df['col_40']) or pd.isnull(df['col_43']):
                if pd.isnull(df['col_56']) and not pd.isnull(float(df['col_39']) + float(df['col_40']) + float(df['col_43'])):
                    return 'Probable Reporting Error'
                else:
                    if pd.isnull(float(df['col_39']) + float(df['col_40']) + float(df['col_43'])) and not pd.isnull(df['col_56']):
                        return 'Probable Reporting Error'
                    else:
                        return 'Probable Reporting Error'

            # If value exists for all the elements
            else:
                lhs_value = float(df['col_56'])
                rhs_value = float(df['col_39']) + \
                    float(df['col_40']) + float(df['col_43'])

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

        # 1.1(col_22) >= 1.1.1(col_23) (for related data items)
        def res2(df):
            if pd.isnull(df['col_22']) and pd.isnull(df['col_23']):
                return 'Blank'
            elif pd.isnull(df['col_22']) or pd.isnull(df['col_23']):
                if pd.isnull(df['col_22']):
                    return 'Inconsistent'
                elif pd.isnull(df['col_23']):
                    return 'Probable Reporting Error (1.1.1 is blank)'
            elif df['col_22'] < df['col_23']:
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.3.1.a(col_33) <= 1.3.1(col_32) (for related data items)

        def res3(df):
            if (df['col_33'] is None) and (df['col_32'] is None):
                return 'Blank'
            elif (df['col_33'] is None) or (df['col_32'] is None):
                if (df['col_33'] is None):
                    return 'Inconsistent'
                elif (df['col_32'] is None):
                    return 'Probable Reporting Error (1.3.1 is blank)'
            if (df['col_33'] is None) > (df['col_32'] is None):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        #  1.2.7 (30) <= 1.1(22) (For recurring data items)
        def res4(df):
            if pd.isnull(float(df['col_30'])) and pd.isnull(float(df['col_22'])):
                return 'Blank'
            elif pd.isnull(float(df['col_30'])) or pd.isnull(float(df['col_22'])):
                if pd.isnull(df['col_30']):
                    return 'Inconsistent'
                elif pd.isnull(df['col_22']):
                    return 'Probable Reporting Error (1.1 is blank)'
            # If value exists for all the elements
            else:

                lhs_value = float(df['col_30'])
                rhs_value = float(df['col_22'])

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

        # # 1.5.1.a (37) <= 1.1 (22) (for unrelated data items)
        def res5(df):
            if pd.isnull(float(df['col_37'])) and pd.isnull(float(df['col_22'])):
                return 'Blank'
            elif pd.isnull(float(df['col_37'])) or pd.isnull(float(df['col_22'])):
                if pd.isnull(df['col_37']):
                    return 'Probable Reporting Error(1.5.1.a is blank)'
                elif pd.isnull(df['col_22']):
                    return 'Inconsistent (1.1 is blank)'
            elif float(df['col_37']) > float(df['col_22']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 1.5.1.b (col_38) <= 1.5.1.a (col_37) (for related data items)
        def res6(df):

            if pd.isnull(float(df['col_38'])) and pd.isnull(float(df['col_37'])):
                return 'Blank'
            elif pd.isnull(float(df['col_38'])) or pd.isnull(float(df['col_37'])):
                if pd.isnull(df['col_38']):
                    return 'Probable Reporting Error (1.5.1.b is blank)'
                elif pd.isnull(df['col_37']):
                    return 'Inconsistent (1.5.1.a is blank)'
            elif float(df['col_38']) > float(df['col_37']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

          # 2.1.2 (col_41) <= 2.1.1.a(col_39) + 2.1.1.b(col_40) (for unrelated data items)
        def res7(df):
            if pd.isnull(df['col_41']) and pd.isnull(df['col_39']) and pd.isnull(df['col_40']):
                return 'Blank'
            elif pd.isnull(df['col_41']) or pd.isnull(df['col_39']) or pd.isnull(df['col_40']):
                if pd.isnull(df['col_41']):
                    return 'Probable Reporting Error (2.1.2 is blank)'
                elif pd.isnull(df['col_39']):
                    return 'Inconsistent 2.1.1.a is null'
                elif pd.isnull(df['col_40']):
                    return 'Inconsistent 2.1.1.b is null'
            elif float(df['col_41']) > float(df['col_39']) + float(df['col_40']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

            # 2.1.3 (col_42) <= 2.1.1.a(col_39) + 2.1.1.b(col_40) (For recurring data items)
        def res8(df):

            if pd.isnull(df['col_42']) and pd.isnull(df['col_39']) and pd.isnull(df['col_40']):
                return 'Blank'
            elif pd.isnull(df['col_42']) or pd.isnull(df['col_39']) or pd.isnull(df['col_40']):
                if pd.isnull(df['col_42']) and not pd.isnull(float(df['col_39']) + float(df['col_40'])):
                    return 'Probable Reporting Error'
                else:
                    if pd.isnull(float(df['col_39']) + float(df['col_40'])) and not pd.isnull(df['col_42']):
                        return 'Probable Reporting Error'
                    else:
                        return 'Probable Reporting Error'

            # If value exists for all the elements
            else:

                lhs_value = float(df['col_42'])
                rhs_value = float(df['col_39']) + float(df['col_40'])

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

        # 2.2.2(col_45) <= 2.2 (col_43) (For recurring data items) ----------need update
        def res9(df):
            if pd.isnull(df['col_45']) and pd.isnull(df['col_43']):
                return 'Blank'
            elif pd.isnull(df['col_45']) or pd.isnull(df['col_43']):
                if pd.isnull(df['col_45']) and not pd.isnull(float(df['col_43'])):
                    return 'Probable Reporting Error'
                else:
                    if pd.isnull(float(df['col_43'])) and not pd.isnull(df['col_45']):
                        return 'Probable Reporting Error'
                    else:
                        return 'Probable Reporting Error'

            # If value exists for all the elements
            else:

                lhs_value = float(df['col_45'])
                rhs_value = float(df['col_43'])

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

        # 4.4(col_57)<= 2.1.1.a(col_39) + 2.1.1.b(col_40) + 2.2(col_43) (For recurring data items)
        def res10(df):
            if pd.isnull(df['col_57']) and pd.isnull(df['col_39']) and pd.isnull(df['col_40']) and pd.isnull(df['col_43']):
                return 'Blank'
            elif pd.isnull(df['col_57']) and pd.isnull(df['col_39']) and pd.isnull(df['col_40']) and pd.isnull(df['col_43']):
                if pd.isnull(df['col_57']) and not pd.isnull(float(df['col_39']) + float(df['col_40']) + float(df['col_43'])):
                    return 'Probable Reporting Error'
                else:
                    if pd.isnull(float(df['col_39']) + float(df['col_40']) + float(df['col_43'])) and not pd.isnull(df['col_42']):
                        return 'Probable Reporting Error'
                    else:
                        return 'Probable Reporting Error'

            # If value exists for all the elements
            else:

                lhs_value = float(df['col_57'])
                rhs_value = float(df['col_39']) + \
                    float(df['col_40']) + float(df['col_43'])

                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'
            return df

         # 6.1.1(col_73) <= 3.1.1.a(col_46) + 3.1.1.b(col_47)
        def res11(df):
            if pd.isnull(df['col_73']) and pd.isnull(df['col_46']) and pd.isnull(df['col_47']):
                return 'Blank'
            elif pd.isnull(df['col_73']) or pd.isnull(df['col_46']) or pd.isnull(df['col_47']):
                if pd.isnull(df['col_73']):
                    return 'Probable Reporting Error (6.1.1 is blank)'
                elif pd.isnull(df['col_46']):
                    return 'Inconsistent (3.1.1.a is blank)'
                elif pd.isnull(df['col_47']):
                    return 'Inconsistent (3.1.1.b is blank)'
            elif float(df['col_73']) > float(df['col_46']) + float(df['col_47']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 6.1.9(col_81) <= 3.1.1.a(col_46) + 3.1.1.b(col_47)
        def res12(df):

            if pd.isnull(df['col_81']) and pd.isnull(df['col_46']) and pd.isnull(df['col_47']):
                return 'Blank'
            elif pd.isnull(df['col_81']) or pd.isnull(df['col_46']) or pd.isnull(df['col_47']):
                if pd.isnull(df['col_81']):
                    return 'Probable Reporting Error (6.1.9 is blank)'
                elif pd.isnull(df['col_46']):
                    return 'Inconsistent (3.1.1.a is blank)'
                elif pd.isnull(df['col_47']):
                    return 'Inconsistent (3.1.1.b is blank)'
            elif float(df['col_81']) > float(df['col_46']) + float(df['col_47']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 6.1.13(col_85) <= 3.1.1.a(col_46) + 3.1.1.b(col_47)
        def res13(df):
            if pd.isnull(df['col_85']) and pd.isnull(df['col_46']) and pd.isnull(df['col_47']):
                return 'Blank'
            elif pd.isnull(df['col_85']) or pd.isnull(df['col_46']) or pd.isnull(df['col_47']):
                if pd.isnull(df['col_85']):
                    return 'Probable Reporting Error  (6.1.13 is blank)'
                elif pd.isnull(df['col_46']):
                    return 'Inconsistent (6.1.13 is blank)'
                elif pd.isnull(df['col_47']):
                    return 'Inconsistent (6.1.13 is blank)'
            elif float(df['col_85']) > float(df['col_46']) + float(df['col_47']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 2.2.1(col_44) <= 2.2(col_43)
        def res14(df):
            if pd.isnull(df['col_44']) and pd.isnull(df['col_43']):
                return 'Blank'
            elif pd.isnull(df['col_44']) or pd.isnull(df['col_43']):
                if pd.isnull(df['col_44']):
                    return 'Probable Reporting Error (2.2.1 is blank)'
                elif pd.isnull(df['col_43']):
                    return 'Inconsistent (2.2 is blank)'
            elif float(df['col_44']) > float(df['col_43']):
                return 'Inconsistent (check fails)'
            else:
                return 'consistent'
            return df

         # 3.1.2(col_48) <= 3.1.1.a(col_46)+ 3.1.1.b(col_47)
        def res15(df):
            if pd.isnull(df['col_48']) and pd.isnull(df['col_46']) and pd.isnull(df['col_47']):
                return 'Blank'
            elif pd.isnull(df['col_48']) or pd.isnull(df['col_46']) or pd.isnull(df['col_47']):
                if pd.isnull(df['col_48']):
                    return 'Probable Reporting Error (3.1.2 is blank)'
                elif pd.isnull(df['col_46']):
                    return 'Inconsistent(3.1.1.a is blank)'
                elif pd.isnull(df['col_47']):
                    return 'Inconsistent (3.1.1.b is blank)'
            elif float(df['col_48']) > float(df['col_46']) + float(df['col_47']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

         # 3.3.1 <= 3.1.1.a + 3.1.1.b
        def res16(df):

            if pd.isnull(df['col_51']) and pd.isnull(df['col_46']) and pd.isnull(df['col_47']):
                return 'Blank'
            elif pd.isnull(df['col_51']) or pd.isnull(df['col_46']) or pd.isnull(df['col_47']):
                if pd.isnull(df['col_51']):
                    return 'Probable Reporting Error (3.3.1 is blank)'
                elif pd.isnull(df['col_46']):
                    return 'Inconsistent (3.3.1.a is blank)'
                elif pd.isnull(df['col_47']):
                    return 'Inconsistent (3.3.1.b is blank)'
            elif float(df['col_51']) > float(df['col_46']) + float(df['col_47']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

         # 3.3.2 <= 3.3.1
        def res17(df):
            if pd.isnull(df['col_52']) and pd.isnull(df['col_51']):
                return 'Blank'
            elif pd.isnull(df['col_52']) or pd.isnull(df['col_51']):
                if pd.isnull(df['col_52']):
                    return 'Probable Reporting Error (3.3.2 is blank)'
                elif pd.isnull(df['col_67']):
                    return 'Inconsistent (3.3.1 is blank)'
            if float(df['col_52']) > float(df['col_51']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 3.3.3<=3.1.1.a+3.1.1.b
        def res18(df):

            if pd.isnull(df['col_53']) and pd.isnull(df['col_46']) and pd.isnull(df['col_47']):
                return 'Blank'
            elif pd.isnull(df['col_53']) or pd.isnull(df['col_46']) or pd.isnull(df['col_47']):
                if pd.isnull(df['col_53']):
                    return 'Probable Reporting Error (3.3.3 is blank)'
                elif pd.isnull(float(df['col_46']) + float(df['col_47'])):
                    return 'Inconsistent'
            elif float(df['col_53']) > float(df['col_46']) + float(df['col_47']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

         # 4.1 <= 2.1.1.a + 2.1.1.b
        def res19(df):

            if pd.isnull(df['col_54']) and pd.isnull(df['col_39']) and pd.isnull(df['col_40']):
                return 'Blank'
            elif pd.isnull(df['col_54']) or pd.isnull(df['col_39']) or pd.isnull(df['col_40']):
                if pd.isnull(df['col_54']):
                    return 'Probable Reporting Error(4.1 is blank)'
                elif pd.isnull(float(df['col_39']) + float(df['col_40'])):
                    return 'Inconsistent'
            elif float(df['col_54']) > float(df['col_39']) + float(df['col_40']):
                return 'Inconsistent (check fails)'
            else:
                return 'consistent'
            return df

        # 5.2 <= 2.1.1.a + 2.1.1.b + 2.2
        def res20(df):

            if pd.isnull(df['col_59']) and pd.isnull(df['col_39']) and pd.isnull(df['col_40']) and pd.isnull(df['col_43']):
                return 'Blank'
            elif pd.isnull(df['col_59']) or pd.isnull(df['col_39']) or pd.isnull(df['col_40']) or pd.isnull(df['col_43']):
                if pd.isnull(df['col_59']):
                    return 'Probable Reporting Error(5.2 is blank)'
                elif pd.isnull(float(df['col_39']) + float(df['col_40']) + float(df['col_43'])):
                    return 'Inconsistent'
            elif float(df['col_59']) > float(df['col_39']) + float(df['col_40']) + float(df['col_43']):
                return 'Inconsistent (check fails)'
            else:
                return 'consistent'
            return df

         # 6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2
        def res21(df):

            if pd.isnull(df['col_97']) and pd.isnull(df['col_98']) and pd.isnull(df['col_94']) and pd.isnull(df['col_95']):
                return 'Blank'
            elif pd.isnull(df['col_97']) or pd.isnull(df['col_98']) or pd.isnull(df['col_94']) or pd.isnull(df['col_95']):
                if pd.isnull(df['col_97']):
                    return 'Probable Reporting Error (6.2.4.a is blank)'
                elif pd.isnull(float(df['col_94']) + float(df['col_95'])):
                    return 'Probable Reporting Error'
            elif float(df['col_97']) + float(df['col_98']) > float(df['col_94']) + float(df['col_95']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4
        def res22(df):

            if pd.isnull(df['col_112']) and pd.isnull(df['col_73']) and pd.isnull(df['col_74']) and pd.isnull(df['col_75']) and pd.isnull(df['col_76']) and pd.isnull(df['col_77']) and pd.isnull(df['col_78']) and pd.isnull(df['col_79']) and pd.isnull(df['col_80']) and pd.isnull(df['col_85']) and pd.isnull(df['col_86']) and pd.isnull(df['col_87']) and pd.isnull(df['col_88']) and pd.isnull(df['col_89']) and pd.isnull(df['col_90']) and pd.isnull(df['col_91']) and pd.isnull(df['col_92']) and pd.isnull(df['col_93']) and pd.isnull(df['col_94']) and pd.isnull(df['col_95']) and pd.isnull(df['col_96']) and pd.isnull(df['col_99']) and pd.isnull(df['col_100']) and pd.isnull(df['col_101']) and pd.isnull(df['col_102']) and pd.isnull(df['col_103']) and pd.isnull(df['col_104']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']):
                return 'Blank'
            elif pd.isnull(df['col_112']) or pd.isnull(df['col_73']) or pd.isnull(df['col_74']) or pd.isnull(df['col_75']) or pd.isnull(df['col_76']) or pd.isnull(df['col_77']) or pd.isnull(df['col_78']) or pd.isnull(df['col_79']) or pd.isnull(df['col_80']) or pd.isnull(df['col_85']) or pd.isnull(df['col_86']) or pd.isnull(df['col_87']) or pd.isnull(df['col_88']) or pd.isnull(df['col_89']) or pd.isnull(df['col_90']) or pd.isnull(df['col_91']) or pd.isnull(df['col_92']) or pd.isnull(df['col_93']) or pd.isnull(df['col_122']) or pd.isnull(df['col_94']) or pd.isnull(df['col_96']) or pd.isnull(df['col_99']) or pd.isnull(df['col_100']) or pd.isnull(df['col_101']) or pd.isnull(df['col_102']) or pd.isnull(df['col_103']) or pd.isnull(df['col_104']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']):
                if pd.isnull(df['col_112']):
                    return 'Probable Reporting Error (6.6.1 is blank)'
                elif pd.isnull(float(df['col_73']) + float(df['col_74']) + float(df['col_75']) + float(df['col_76']) + float(df['col_77']) + float(df['col_78']) + float(df['col_79']) + float(df['col_80']) + float(df['col_85']) + float(df['col_86']) + float(df['col_87']) + float(df['col_88']) + float(df['col_89']) + float(df['col_90']) + float(df['col_91']) + float(df['col_92']) + float(df['col_93']) + float(df['col_94']) + float(df['col_95']) + float(df['col_96']) + float(df['col_99']) + float(df['col_100']) + float(df['col_101']) + float(df['col_102']) + float(df['col_103']) + float(df['col_104']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110'])):
                    return 'Inconsistent'
            elif float(df['col_112']) > float(df['col_73']) + float(df['col_74']) + float(df['col_75']) + float(df['col_76']) + float(df['col_77']) + float(df['col_78']) + float(df['col_79']) + float(df['col_80']) + float(df['col_85']) + float(df['col_86']) + float(df['col_87']) + float(df['col_88']) + float(df['col_89']) + float(df['col_90']) + float(df['col_91']) + float(df['col_92']) + float(df['col_93']) + float(df['col_94']) + float(df['col_95']) + float(df['col_96']) + float(df['col_99']) + float(df['col_100']) + float(df['col_101']) + float(df['col_102']) + float(df['col_103']) + float(df['col_104']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']):
                return 'Inconsistent (check fails)'
            else:
                return 'consistent'
            return df

        # 6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4
        def res23(df):

            if pd.isnull(df['col_113']) and pd.isnull(df['col_73']) and pd.isnull(df['col_74']) and pd.isnull(df['col_75']) and pd.isnull(df['col_76']) and pd.isnull(df['col_77']) and pd.isnull(df['col_78']) and pd.isnull(df['col_79']) and pd.isnull(df['col_80']) and pd.isnull(df['col_85']) and pd.isnull(df['col_86']) and pd.isnull(df['col_87']) and pd.isnull(df['col_88']) and pd.isnull(df['col_89']) and pd.isnull(df['col_90']) and pd.isnull(df['col_91']) and pd.isnull(df['col_92']) and pd.isnull(df['col_93']) and pd.isnull(df['col_94']) and pd.isnull(df['col_95']) and pd.isnull(df['col_96']) and pd.isnull(df['col_99']) and pd.isnull(df['col_100']) and pd.isnull(df['col_101']) and pd.isnull(df['col_102']) and pd.isnull(df['col_103']) and pd.isnull(df['col_104']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']):
                return 'Blank'
            elif pd.isnull(df['col_113']) or pd.isnull(df['col_73']) or pd.isnull(df['col_74']) or pd.isnull(df['col_75']) or pd.isnull(df['col_76']) or pd.isnull(df['col_77']) or pd.isnull(df['col_78']) or pd.isnull(df['col_79']) or pd.isnull(df['col_80']) or pd.isnull(df['col_85']) or pd.isnull(df['col_86']) or pd.isnull(df['col_87']) or pd.isnull(df['col_88']) or pd.isnull(df['col_89']) or pd.isnull(df['col_90']) or pd.isnull(df['col_91']) or pd.isnull(df['col_92']) or pd.isnull(df['col_93']) or pd.isnull(df['col_122']) or pd.isnull(df['col_94']) or pd.isnull(df['col_96']) or pd.isnull(df['col_99']) or pd.isnull(df['col_100']) or pd.isnull(df['col_101']) or pd.isnull(df['col_102']) or pd.isnull(df['col_103']) or pd.isnull(df['col_104']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']):
                if pd.isnull(df['col_113']):
                    return 'Probable Reporting Error (6.6.2 is blank)'
                elif pd.isnull(float(df['col_73']) + float(df['col_74']) + float(df['col_75']) + float(df['col_76']) + float(df['col_77']) + float(df['col_78']) + float(df['col_79']) + float(df['col_80']) + float(df['col_85']) + float(df['col_86']) + float(df['col_87']) + float(df['col_88']) + float(df['col_89']) + float(df['col_90']) + float(df['col_91']) + float(df['col_92']) + float(df['col_93']) + float(df['col_94']) + float(df['col_95']) + float(df['col_96']) + float(df['col_99']) + float(df['col_100']) + float(df['col_101']) + float(df['col_102']) + float(df['col_103']) + float(df['col_104']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110'])):
                    return 'Inconsistent'
            elif float(df['col_113']) > float(df['col_73']) + float(df['col_74']) + float(df['col_75']) + float(df['col_76']) + float(df['col_77']) + float(df['col_78']) + float(df['col_79']) + float(df['col_80']) + float(df['col_85']) + float(df['col_86']) + float(df['col_87']) + float(df['col_88']) + float(df['col_89']) + float(df['col_90']) + float(df['col_91']) + float(df['col_92']) + float(df['col_93']) + float(df['col_94']) + float(df['col_95']) + float(df['col_96']) + float(df['col_99']) + float(df['col_100']) + float(df['col_101']) + float(df['col_102']) + float(df['col_103']) + float(df['col_104']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']):
                return 'Inconsistent (check fails)'
            else:
                return 'consistent'
            return df

         # 6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4
        def res24(df):

            if pd.isnull(df['col_114']) and pd.isnull(df['col_73']) and pd.isnull(df['col_74']) and pd.isnull(df['col_75']) and pd.isnull(df['col_76']) and pd.isnull(df['col_77']) and pd.isnull(df['col_78']) and pd.isnull(df['col_79']) and pd.isnull(df['col_80']) and pd.isnull(df['col_85']) and pd.isnull(df['col_86']) and pd.isnull(df['col_87']) and pd.isnull(df['col_88']) and pd.isnull(df['col_89']) and pd.isnull(df['col_90']) and pd.isnull(df['col_91']) and pd.isnull(df['col_92']) and pd.isnull(df['col_93']) and pd.isnull(df['col_94']) and pd.isnull(df['col_95']) and pd.isnull(df['col_96']) and pd.isnull(df['col_99']) and pd.isnull(df['col_100']) and pd.isnull(df['col_101']) and pd.isnull(df['col_102']) and pd.isnull(df['col_103']) and pd.isnull(df['col_104']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']):
                return 'Blank'
            elif pd.isnull(df['col_114']) or pd.isnull(df['col_73']) or pd.isnull(df['col_74']) or pd.isnull(df['col_75']) or pd.isnull(df['col_76']) or pd.isnull(df['col_77']) or pd.isnull(df['col_78']) or pd.isnull(df['col_79']) or pd.isnull(df['col_80']) or pd.isnull(df['col_85']) or pd.isnull(df['col_86']) or pd.isnull(df['col_87']) or pd.isnull(df['col_88']) or pd.isnull(df['col_89']) or pd.isnull(df['col_90']) or pd.isnull(df['col_91']) or pd.isnull(df['col_92']) or pd.isnull(df['col_93']) or pd.isnull(df['col_122']) or pd.isnull(df['col_94']) or pd.isnull(df['col_96']) or pd.isnull(df['col_99']) or pd.isnull(df['col_100']) or pd.isnull(df['col_101']) or pd.isnull(df['col_102']) or pd.isnull(df['col_103']) or pd.isnull(df['col_104']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']):
                if pd.isnull(df['col_114']):
                    return 'Probable Reporting Error (6.6.1 is blank)'
                elif pd.isnull(float(df['col_73']) + float(df['col_74']) + float(df['col_75']) + float(df['col_76']) + float(df['col_77']) + float(df['col_78']) + float(df['col_79']) + float(df['col_80']) + float(df['col_85']) + float(df['col_86']) + float(df['col_87']) + float(df['col_88']) + float(df['col_89']) + float(df['col_90']) + float(df['col_91']) + float(df['col_92']) + float(df['col_93']) + float(df['col_94']) + float(df['col_95']) + float(df['col_96']) + float(df['col_99']) + float(df['col_100']) + float(df['col_101']) + float(df['col_102']) + float(df['col_103']) + float(df['col_104']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110'])):
                    return 'Inconsistent'
            elif float(df['col_114']) > float(df['col_73']) + float(df['col_74']) + float(df['col_75']) + float(df['col_76']) + float(df['col_77']) + float(df['col_78']) + float(df['col_79']) + float(df['col_80']) + float(df['col_85']) + float(df['col_86']) + float(df['col_87']) + float(df['col_88']) + float(df['col_89']) + float(df['col_90']) + float(df['col_91']) + float(df['col_92']) + float(df['col_93']) + float(df['col_94']) + float(df['col_95']) + float(df['col_96']) + float(df['col_99']) + float(df['col_100']) + float(df['col_101']) + float(df['col_102']) + float(df['col_103']) + float(df['col_104']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']):
                return 'Inconsistent (check fails)'
            else:
                return 'consistent'
            return df

        # 6.7.3<=6.7.2
        def res25(df):

            if pd.isnull(df['col_117']) and pd.isnull(df['col_116']):
                return 'Blank'
            elif pd.isnull(df['col_117']) or pd.isnull(df['col_116']):
                if pd.isnull(df['col_117']):
                    return 'Probable Reporting Error (6.7.3 is blank)'
            elif pd.isnull(df['col_116']):
                return 'Inconsistent (6.7.2 is blank)'
            elif float(df['col_117']) > float(df['col_116']):
                return 'Inconsistent (check fails)'
            else:
                return 'consistent'
            return df

        # 10.1.2<=10.1.1
        def res26(df):
            if pd.isnull(df['col_144']) and pd.isnull(df['col_143']):
                return 'Blank'
            elif pd.isnull(df['col_144']) or pd.isnull(df['col_143']):
                if pd.isnull(df['col_144']):
                    return 'Probable Reporting Error (10.1.2 is blank)'
                elif pd.isnull(df['col_143']):
                    return 'Inconsistent (10.1.1 is blank)'
            elif float(df['col_144']) > float(df['col_143']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 10.2.1.b<=10.2.1.a
        def res27(df):

            if pd.isnull(df['col_146']) and pd.isnull(df['col_145']):
                return 'Blank'
            elif pd.isnull(df['col_146']) or pd.isnull(df['col_145']):
                if pd.isnull(df['col_146']):
                    return 'Probable Reporting Error (10.2.1.b is blank)'
                elif pd.isnull(df['col_145']):
                    return 'Inconsistent (10.2.1.a is blank)'
            elif float(df['col_146']) > float(df['col_145']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2
        def res28(df):

            if pd.isnull(df['col_46']) and pd.isnull(df['col_47']) and pd.isnull(df['col_49']) and pd.isnull(df['col_39']) and pd.isnull(df['col_40']) and pd.isnull(df['col_43']):
                return 'Blank'
            elif pd.isnull(df['col_46']) or pd.isnull(df['col_47']) or pd.isnull(df['col_49']) or pd.isnull(df['col_39']) or pd.isnull(df['col_40']) or pd.isnull(df['col_43']):
                if pd.isnull(df['col_46']):
                    return 'Inconsistent  (3.1.1.a is blank)'
                elif pd.isnull(df['col_47']):
                    return 'Inconsistent (3.1.1.b is blank)'
                elif pd.isnull(df['col_49']):
                    return 'Inconsistent (3.1.3 is blank)'
                elif pd.isnull(float(df['col_39']) + float(df['col_40']) + float(df['col_43'])):
                    return 'Probable Reporting Error'
            elif float(df['col_46']) + float(df['col_47']) + float(df['col_49']) < float(df['col_39']) + float(df['col_40']) + float(df['col_43']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 8.1.1.c<=8.1.1.a
        def res29(df):

            if pd.isnull(df['col_131']) and pd.isnull(df['col_129']):
                return 'Blank'
            elif pd.isnull(df['col_131']) or pd.isnull(df['col_129']):
                if pd.isnull(df['col_131']):
                    return 'Probable Reporting Error (8.1.1.c is blank)'
                elif pd.isnull(df['col_129']):
                    return 'Inconsistent (8.1.1.a is blank)'
            elif float(df['col_131']) > float(df['col_129']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8
        def res30(df):

            if pd.isnull(df['col_140']) and pd.isnull(df['col_141']) and pd.isnull(df['col_132']) and pd.isnull(df['col_133']) and pd.isnull(df['col_134']) and pd.isnull(df['col_135']) and pd.isnull(df['col_136']) and pd.isnull(df['col_137']) and pd.isnull(df['col_138']) and pd.isnull(df['col_139']):
                return 'Blank'
            elif pd.isnull(df['col_140']) or pd.isnull(df['col_141']) or pd.isnull(df['col_132']) or pd.isnull(df['col_133']) or pd.isnull(df['col_134']) or pd.isnull(df['col_135']) or pd.isnull(df['col_136']) or pd.isnull(df['col_137']) or pd.isnull(df['col_138']) or pd.isnull(df['col_139']):
                if pd.isnull(df['col_140']):
                    return 'Inconsistent (9.2.1 is blank)'
                elif pd.isnull(df['col_141']):
                    return 'Inconsistent (9.2.2 is blank)'
                elif pd.isnull(float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139'])):
                    return 'Probable Reporting Error'
            elif float(df['col_140']) + float(df['col_141']) < float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # 8.1.1.b<=8.1.1.a
        def res31(df):

            if pd.isnull(df['col_130']) and pd.isnull(df['col_129']):
                return 'Blank'
            elif pd.isnull(df['col_130']) or pd.isnull(df['col_129']):
                if pd.isnull(df['col_130']):
                    return 'Probable Reporting Error (8.1.1.b is blank)'
                elif pd.isnull(df['col_129']):
                    return 'Inconsistent (8.1.1.a is blank)'
            elif float(df['col_130']) > float(df['col_129']):
                return 'Inconsistent'
            else:
                return 'consistent'
            return df

        # Renaming column names
        # =====================
        df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res1, axis=1)

        df['1.1 <= 1.1.1'] = df.apply(res2, axis=1)

        df['1.3.1.a <= 1.3.1'] = df.apply(res3, axis=1)

        df['1.2.7 <= 1.1'] = df.apply(res4, axis=1)

        df['1.5.1.a <= 1.1'] = df.apply(res5, axis=1)

        df['1.5.1.b <= 1.5.1.a'] = df.apply(res6, axis=1)

        df['2.1.2 <= 2.1.1.a + 2.1.1.b'] = df.apply(res7, axis=1)

        df['2.1.3 <= 2.1.1.a + 2.1.1.b'] = df.apply(res8, axis=1)

        df['2.2.2 <= 2.2'] = df.apply(res9, axis=1)

        df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res10, axis=1)

        df['6.1.1 <= 3.1.1.a + 3.1.1.b'] = df.apply(res11, axis=1)

        df['6.1.9 <= 3.1.1.a + 3.1.1.b'] = df.apply(res12, axis=1)

        df['6.1.13 <= 3.1.1.a + 3.1.1.b'] = df.apply(res13, axis=1)

        df['2.2.1 <= 2.2'] = df.apply(res14, axis=1)

        df['3.1.2 <= 3.1.1.a + 3.1.1.b'] = df.apply(res15, axis=1)

        df['3.3.1 <= 3.1.1.a + 3.1.1.b'] = df.apply(res16, axis=1)

        df['3.3.2 <= 3.3.1'] = df.apply(res17, axis=1)

        df['3.3.3 <= 3.1.1.a + 3.1.1.b'] = df.apply(res18, axis=1)

        df['4.1 <= 2.1.1.a + 2.1.1.b'] = df.apply(res19, axis=1)

        df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res20, axis=1)

        df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'] = df.apply(res21, axis=1)

        df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(
            res22, axis=1)

        df['6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(
            res23, axis=1)

        df['6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(
            res24, axis=1)

        df['6.7.3<=6.7.2'] = df.apply(res25, axis=1)

        df['10.1.2<=10.1.1'] = df.apply(res26, axis=1)

        df['10.2.1.b<=10.2.1.a'] = df.apply(res27, axis=1)

        df['3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2'] = df.apply(
            res28, axis=1)

        df['8.1.1.c<=8.1.1.a'] = df.apply(res29, axis=1)

        df['9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8'] = df.apply(
            res30, axis=1)

        df['8.1.1.b<=8.1.1.a'] = df.apply(res31, axis=1)

        # Merging all the renamed columns
        # ===============================
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
                        df['3.3.3 <= 3.1.1.a + 3.1.1.b'],
                        df['4.1 <= 2.1.1.a + 2.1.1.b'],
                        df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'],
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



        # Mergining current result of modified checks with original dataframe and displaying it on screen
        frames = [df_, df]
        print(frames)
        df = pd.concat(frames, axis=1, sort=False)
        #df = df.dropna(axis=0, subset=['col_2'])
        self.tableView.setModel(PandasModel(df))

        msg = QMessageBox()
        msg.setWindowTitle("Validation Completion Message")
        msg.setText("Validation Complete")
        msg.exec()

        return df

    # Filter to decide which filter button user clicked
    def eventFilter(self, target, event):
        if target == self.pushButton_4 and event.type() == QtCore.QEvent.MouseButtonPress:
            print("Checked State")
            self.pushButton_4.clicked.connect(self.onSelectState)
            return True

        elif target == self.pushButton_5 and event.type() == QtCore.QEvent.MouseButtonPress:
            print("Checked District")
            self.pushButton_5.clicked.connect(self.onSelectDistrict)
            return True

        elif target == self.pushButton_6 and event.type() == QtCore.QEvent.MouseButtonPress:
            print("Checked Facility Name")
            self.pushButton_6.clicked.connect(self.onSelectFacilityName)
            return True

        elif target == self.pushButton_7 and event.type() == QtCore.QEvent.MouseButtonPress:
            print("Checked Month")
            self.pushButton_7.clicked.connect(self.onSelectMonth)
            return True

        elif target == self.pushButton_8 and event.type() == QtCore.QEvent.MouseButtonPress:
            print("Checked Year")
            self.pushButton_8.clicked.connect(self.onSelectYear)
            return True

        return False

    ################################################################################
    # Select State

    # Filter State Functionality

    def onSelectState(self, index):
        global list_set
        self.keywords = dict([(i, []) for i in range(df.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 200 }')
        font = self.menu.font()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.menu.setFont(font)

        index = 3
        self.col = index

        data_unique = []

        self.checkBoxs = []

        # list storing state data
        item = df['col_3'].to_list()

        ''' Adding search regex filter '''
        model = QtGui.QStandardItemModel(len(item), 1)
        model.setHorizontalHeaderLabels(['States'])
        for row, state in enumerate(item):
            itm = QtGui.QStandardItem(state)
            model.setItem(row, 0, itm)

        filter_proxy_model = QtCore.QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(3)

        search_field = QtWidgets.QLineEdit()
        search_field.setStyleSheet(
            'font-size: 15px; height: 20px; width: 240px')
        search_field.textChanged.connect(self.onTextChanged)

        searchAction = QWidgetAction(self.menu)
        searchAction.setDefaultWidget(search_field)
        self.menu.addAction(searchAction)

        ''''''

        # Selectall added into Dropdown
        checkBox = QtWidgets.QCheckBox("Select all", self.menu)

        # All the checkboxes are enabled to check
        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(checkBox)
        self.menu.addAction(checkableAction)
        checkBox.setChecked(True)
        checkBox.stateChanged.connect(self.slotSelect)

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
                                         QtCore.Qt.Vertical, self.menu)

        # ok selected
        btn.accepted.connect(self.menuClose)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)
        self.pushButton_4.setMenu(self.menu)

    def onTextChanged(self):
        print('working//////////////////')

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
        global df
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(df['col_3'].shape[0])])

        # for i in range(df.shape[0]):
        j = 0
        for j in range(df.shape[0]):
            item = df['col_3'].to_list()

            print(self.keywords[self.col])
            # if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()]
        print(final_lst, 'this is final list of Select State')
        df = df[final_lst]
        self.tableView.setModel(PandasModel(df))
        return df

    ################################################################################
    # Select District

        # Select District Functionality
    def onSelectDistrict(self, index):
        self.keywords = dict([(i, []) for i in range(df.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 200 }')
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
        list_set = df['col_5'].to_list()

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
                                         QtCore.Qt.Vertical, self.menu)

        # ok selected
        btn.accepted.connect(self.menuCloseDistrict)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)
        self.pushButton_5.setMenu(self.menu)

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
        global df
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(df['col_5'].shape[0])])
        print(columnsShow)

        j = 0
        for j in range(df['col_5'].shape[0]):
            item = df['col_5'].to_list()

            # if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()]
        print(final_lst, 'this is final list of Select Month')
        df = df[final_lst]
        print(df)
        self.tableView.setModel(PandasModel(df))
        return df

    ################################################################################
    # Select Facility Name

    # Select FacilityName Functionality

    def onSelectFacilityName(self, index):
        self.keywords = dict([(i, []) for i in range(df.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: 20; width: 400 }')
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

        # list storing Facility Name data
        list_set = df['col_14'].to_list()

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
                                         QtCore.Qt.Vertical, self.menu)

        # ok selected
        btn.accepted.connect(self.menuCloseFacilityName)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)

        ############# Always set Pushbutton ####################
        self.pushButton_6.setMenu(self.menu)

        self.scrollbar = QtWidgets.QScrollArea(widgetResizable=False)
        self.scrollbar.setWidget(self.menu)

        self.tabwidget = QtWidgets.QTabWidget()
        self.tabwidget.addTab(self.scrollbar, "Tab1")
        self.layout = QtWidgets.QVBoxLayout(Dialog)
        self.layout.addWidget(self.tabwidget)
        self.tabwidget.setTabBarAutoHide(True)
        self.tabwidget.tabCloseRequested.connect(self.close_tab)
        

    # close tab
    def close_tab(self,index):
        self.tabwidget.removeTab(index)


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
        
        self.scrollbar.close()
        self.layout.deleteLater()


    # Filter data columnwise
    def filterdataFacilityName(self):
        global df
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(df['col_14'].shape[0])])
        print(columnsShow)

        j = 0
        for j in range(df['col_14'].shape[0]):
            item = df['col_14'].to_list()

            # if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()]
        print(final_lst, 'this is final list of Select District')

        # matching list of facility type with col of dataframe returned by onSelectDistrict fun
        df = df[final_lst]
        print(df)
        self.tableView.setModel(PandasModel(df))
        return df

    ################################################################################
    # Select Month

    # Select Month Filter

    def onSelectMonth(self, index):
        self.keywords = dict([(i, []) for i in range(df.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 200 }')
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

        # list storing Facility Name data
        list_set = df['col_1'].to_list()

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
                                         QtCore.Qt.Vertical, self.menu)

        # ok selected
        btn.accepted.connect(self.menuCloseMonth)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)

        ############# Always set Pushbutton ####################
        self.pushButton_7.setMenu(self.menu)

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
        print(self.keywords[self.col])
        self.filterdataMonth()
        self.menu.close()

    # Filter data columnwise
    def filterdataMonth(self):
        global df
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(df['col_1'].shape[0])])
        print(columnsShow)

        j = 0
        for j in range(df['col_1'].shape[0]):
            item = df['col_1'].to_list()

            # if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()]
        print(final_lst, 'this is final list of Select Month')

        # matching list of facility type with col of dataframe returned by onSelectDistrict fun
        df = df[final_lst]
        print(df)
        self.tableView.setModel(PandasModel(df))
        return df

    ################################################################################
    # Select Year

    # Select Year Filter
    def onSelectYear(self, index):
        self.keywords = dict([(i, []) for i in range(df.shape[0])])
        print(self.keywords)
        self.menu = QtWidgets.QMenu(Dialog)
        self.menu.setStyleSheet('QMenu { menu-scrollable: true; width: 200 }')
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

        # list storing Facility Name data
        list_set = df['col_2'].to_list()

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
                                         QtCore.Qt.Vertical, self.menu)

        # ok selected
        btn.accepted.connect(self.menuCloseYear)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)

        ############# Always set Pushbutton ####################
        self.pushButton_8.setMenu(self.menu)

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
        print(self.keywords[self.col])
        self.filterdataYear()
        self.menu.close()

    # Filter data columnwise
    def filterdataYear(self):
        global df
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(df['col_2'].shape[0])])
        print(columnsShow)

        j = 0
        for j in range(df['col_2'].shape[0]):
            item = df['col_2'].to_list()

            # if self.keywords[self.col]:
            if item[j] not in self.keywords[self.col]:
                columnsShow[j] = False

        # for key, value in columnsShow.items():
        final_lst = [i for i in columnsShow.values()]
        print(final_lst, 'this is final list of Select Year')

        # matching list of facility type with col of dataframe returned by onSelectDistrict fun
        df = df[final_lst]
        print(df)
        self.tableView.setModel(PandasModel(df))
        return df


    # To count summary of the Modified Checks
    # =======================================
    def summaryReport(self):
        global final_result_summ1, final_result_summ2

        # For Health Sub Centre
        if FType == 'Health Sub Centre':
            df_SummReport = df.iloc[:, 200:]     ## Taking columns after 200th


        # For Primary Health Centre
        elif FType == 'Primary Health Centre':
            df_SummReport = df.iloc[:, 305:]     ## Taking columns after 305th


        ## First Summary Report
        ## ---------------------
        count_Consistent = []
        count_Inconsistent = []
        # count_Blank = []
        count_ProbableRErr = []
        Columns = list(df_SummReport.columns.values.tolist())

        for col_name in Columns:

            c1 = df_SummReport[col_name].str.count("consistent").sum()
            count_Consistent.append(c1)

            c2 = df_SummReport[col_name].str.count("Inconsistent").sum()
            count_Inconsistent.append(c2)

            # c3 = df_SummReport[col_name].str.count("Blank").sum()
            # count_Blank.append(c3)

            c4 = df_SummReport[col_name].str.count("Probable Reporting Error").sum()
            count_ProbableRErr.append(c4)

        final_result_summ1 = pd.DataFrame({"Conditions": df_SummReport.columns,
                                            "Consistent": count_Consistent,
                                                "Inconsistent": count_Inconsistent,
                                                    "Probable Reporting Error": count_ProbableRErr})


        ## Second Summary Report
        ## --------------------

        summ2_countInconsistent = []
        summ2_countProbableRErr = []

        # Iterating over indices of each row and calculating number of Blanks for each Facility Name 
        for index in range(len(df_SummReport)):
            '''   For no. of Blanks   '''
            inconsistent = df_SummReport.iloc[index, :].str.count("Inconsistent").sum()
            summ2_countInconsistent.append(inconsistent)
            
            '''   For no. of Probable Reporting Errors   '''
            probableRErr = df_SummReport.iloc[index, :].str.count('Probable Reporting Error').sum()
            summ2_countProbableRErr.append(probableRErr)

        final_result_summ2 = pd.DataFrame({ "Facility Name": df['col_14'].tolist(),
                                                "Inconsistent": summ2_countInconsistent,
                                                    "Probable Reporting Error": summ2_countProbableRErr})

        final_result_summ2['PercentileInc'] = final_result_summ2['Inconsistent'].rank(pct=True)
        final_result_summ2['PercentilePRErr'] = final_result_summ2['Probable Reporting Error'].rank(pct=True)
        
        # # Top 10 percentile of Inconsistent values
        # df_2 = final_result_summ2[final_result_summ2['Inconsistent'].ge(final_result_summ2['Inconsistent'].quantile(0.9))]
        # print(df_2)

        lst1 = final_result_summ2['Inconsistent'].to_numpy().tolist()
        lst2 = final_result_summ2['PercentileInc'].to_numpy().tolist()
        print(lst1, lst2)
        color_dict = dict(zip(lst1, lst2))
        print(color_dict)

        def select_col(x):
            c = ['background-color: #ef5350',
                    'background-color: #ffb74d',
                        'background-color: #ffee58',
                            'background-color: #8bc34a',
                                '']

            #compare columns
            mask_4 = x['PercentilePRErr'] > 0.75
            mask_5 = (x['PercentilePRErr'] < 0.75) & (x['PercentilePRErr'] >= 0.5)
            mask_6 = (x['PercentilePRErr'] < 0.5) & (x['PercentilePRErr'] >= 0.25)
            mask_7 = x['PercentilePRErr'] < 0.25


            mask = x['PercentileInc'] > 0.75
            mask_1 = (x['PercentileInc'] < 0.75) & (x['PercentileInc'] >= 0.5)
            mask_2 = (x['PercentileInc'] < 0.5) & (x['PercentileInc'] >= 0.25)
            mask_3 = x['PercentileInc'] < 0.25

            
            #DataFrame with same index and columns names as original filled empty strings
            df1 =  pd.DataFrame(c[4], x.index, columns=x.columns)

            #modify values of df1 column by boolean mask
            df1.loc[mask, 'Inconsistent'] = c[0]
            df1.loc[mask_1, 'Inconsistent'] = c[1]
            df1.loc[mask_2, 'Inconsistent'] = c[2]
            df1.loc[mask_3, 'Inconsistent'] = c[3]

            df1.loc[mask_4, 'Probable Reporting Error'] = c[0]
            df1.loc[mask_5, 'Probable Reporting Error'] = c[1]
            df1.loc[mask_6, 'Probable Reporting Error'] = c[2]
            df1.loc[mask_7, 'Probable Reporting Error'] = c[3]

            df1.sort_values(by=["Inconsistent", "Probable Reporting Error"], ascending=[False, False])

            return df1

        final_result_summ2 = final_result_summ2.style.apply(select_col, axis=None)

        ## Third Summary Report
        ## --------------------
        summ3_countConsistent = []

        # Iterating over indices of each row and calculating number of Consistent 
        for index in range(len(df_SummReport)):
            '''   For no. of consistent   '''
            consistent = df_SummReport.iloc[index, :].str.count("consistent").sum()
            summ3_countConsistent.append(consistent)

        final_result_summ3 = pd.DataFrame({ "Facility Name": df['col_14'].tolist(),
                                                    "Consistent": summ3_countConsistent})


        return final_result_summ1, final_result_summ2, final_result_summ3

    # To calculate Summary Report for complete Blank for each Facility Name
    # =====================================================================
    def Summary_RowCount(self):
        pass


    def export(self):
        table_result1, table_result2, table_result3 = self.summaryReport()

        # Rename orignal headers
        df.rename(res_dict , axis=1, inplace=True)

        # Save file dialog
        filename = QFileDialog.getSaveFileName(Dialog, "Save to Excel", "Validation_table",
                                               "Excel Spreadsheet (*.xlsx);;"
                                               "All Files (*)")[0]


        with pd.ExcelWriter(filename) as writer:  # doctest: +SKIP
            df.to_excel(writer, sheet_name='Validated_Data')
            table_result1.to_excel(writer, sheet_name='Summary Report-1', engine='openpyxl')
            table_result2.to_excel(writer, sheet_name='Summary Report-2', engine='openpyxl')
            table_result3.to_excel(writer, sheet_name='Summary Report-3', engine='openpyxl')



        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setText(("{}\n \n\n exported to the file location you have chosen".format(filename)))
        msg.exec()

    def reset(self):
        self.comboBox.clear()
        self.pushButton.setEnabled(True)
        products = {'_': [' ']}
        blank_df = pd.DataFrame(products, columns=['_'])
        self.tableView.setModel(PandasModel(blank_df))


################################### Main Function ############################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
