import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import sys, re


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
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.pushButton_2.clicked.connect(self.HSC_Validate)
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
        # self.pushButton_4.setText(_translate("Dialog", "Nothing Selected"))
        # self.pushButton_5.setText(_translate("Dialog", "Nothing Selected"))
        # self.pushButton_6.setText(_translate("Dialog", "Nothing Selected"))
        # self.pushButton_7.setText(_translate("Dialog", "Nothing Selected"))
        # self.pushButton_8.setText(_translate("Dialog", "Nothing Selected"))
        self.pushButton_9.setText(_translate("Dialog", "Reset"))

    def upload(self):
        global df_, df_OrgHeaders

        # Validation for uploaded valid excel file
        try:
            # Upload file by opening filedialog
            fileName, _ = QFileDialog.getOpenFileName(Dialog, "Open Excel",(QtCore.QDir.homePath()), "Excel (*.xls *.xlsx)")
    
            # Read uploaded excel file
            df_ = pd.read_excel(fileName)

            # Converted again to csv file
            df_.to_csv("FileName.csv")

            # Read converted csv file
            df_ = pd.read_csv("FileName.csv")
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Uploaded File Error Message")
            msg.setText("The file which you have uploaded is not in the valid format of excel, Please upload valid excel file")
            msg.exec()

            try:
                # Upload file by opening filedialog
                fileName, _ = QFileDialog.getOpenFileName(Dialog, "Open Excel",(QtCore.QDir.homePath()), "Excel (*.xls *.xlsx)")
    
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
        self.comboBox.addItems(['-select-'])
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
                
                # Signaling HSC_Validate function i.e function where validation checks are present
                self.pushButton_2.clicked.connect(self.HSC_Validate)

            elif ((FType == 'DH')):
                print(FType)
                # self.DH_Validate()

            elif ((FType == 'SDH')):
                print(FType)
                # self.SDH_Validate()

            elif ((FType == 'CHC')):
                print(FType)
                # self.CHC_Validate()

            elif ((FType == 'PHC')):
                print(FType)
                # self.PHC_Validate()
        except:
            raise Exception('Facility Type Name is not matching')


    # Upload file button functionality
    def loadFile(self, df_):   
        return df_

    # Validation for HSC 
    def HSC_Validate(self):
        # df = self.loadFile(df_)
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
                rhs_value = float(df['col_39']) + float(df['col_40']) + float(df['col_43'])
                
                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'

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
                        return 'Consistent'
                else:
                    if lhs_value > (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Inconsistent'

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
                        return 'Consistent'
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
                        return 'Consistent'
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
                rhs_value = float(df['col_39']) + float(df['col_40']) + float(df['col_43']) 
                
                if lhs_value <= rhs_value:
                    if lhs_value < (0.5*rhs_value):
                        return 'Probable Reporting Error'
                    else:
                        return 'Consistent'
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
                elif pd.isnull(float(df['col_46'])+ float(df['col_47'])):
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
                elif pd.isnull(float(df['col_39'])+ float(df['col_40'])):
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
                return 'Consistent'
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
                return 'Consistent'
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
                return 'Consistent'
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
                return 'Consistent'
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
                return 'Consistent'
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
                return 'Consistent'
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
                return 'Consistent'
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
                return 'Consistent'
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
                return 'Consistent'
            return df

        df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res1, axis=1)
        count_condition_1_consistent = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "consistent").sum()
        count_condition_1_inconsistent = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Inconsistent").sum()
        count_condition_1_blank = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Blank").sum()
        count_condition_1_Probable_Reporting_Error = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Probable Reporting Error").sum()

        df['1.1 <= 1.1.1'] = df.apply(res2, axis=1)
        count_condition_2_consistent = df['1.1 <= 1.1.1'].str.count(
            "consistent").sum()
        count_condition_2_inconsistent = df['1.1 <= 1.1.1'].str.count(
            "Inconsistent").sum()
        count_condition_2_blank = df['1.1 <= 1.1.1'].str.count("Blank").sum()
        count_condition_2_Probable_Reporting_Error = df['1.1 <= 1.1.1'].str.count(
            "Probable Reporting Error").sum()

        df['1.3.1.a <= 1.3.1'] = df.apply(res3, axis=1)
        count_condition_3_consistent = df['1.3.1.a <= 1.3.1'].str.count(
            "consistent").sum()
        count_condition_3_inconsistent = df['1.3.1.a <= 1.3.1'].str.count(
            "Inconsistent").sum()
        count_condition_3_blank = df['1.3.1.a <= 1.3.1'].str.count(
            "Blank").sum()
        count_condition_3_Probable_Reporting_Error = df['1.3.1.a <= 1.3.1'].str.count(
            "Probable Reporting Error").sum()

        df['1.2.7 <= 1.1'] = df.apply(res4, axis=1)
        count_condition_4_consistent = df['1.2.7 <= 1.1'].str.count(
            "consistent").sum()
        count_condition_4_inconsistent = df['1.2.7 <= 1.1'].str.count(
            "Inconsistent").sum()
        count_condition_4_blank = df['1.2.7 <= 1.1'].str.count("Blank").sum()
        count_condition_4_Probable_Reporting_Error = df['1.2.7 <= 1.1'].str.count(
            "Probable Reporting Error").sum()

        df['1.5.1.a <= 1.1'] = df.apply(res5, axis=1)
        count_condition_5_consistent = df['1.5.1.a <= 1.1'].str.count(
            "consistent").sum()
        count_condition_5_inconsistent = df['1.5.1.a <= 1.1'].str.count(
            "Inconsistent").sum()
        count_condition_5_blank = df['1.5.1.a <= 1.1'].str.count("Blank").sum()
        count_condition_5_Probable_Reporting_Error = df['1.5.1.a <= 1.1'].str.count(
            "Probable Reporting Error").sum()

        df['1.5.1.b <= 1.5.1.a'] = df.apply(res6, axis=1)
        count_condition_6_consistent = df['1.5.1.b <= 1.5.1.a'].str.count(
            "consistent").sum()
        count_condition_6_inconsistent = df['1.5.1.b <= 1.5.1.a'].str.count(
            "Inconsistent").sum()
        count_condition_6_blank = df['1.5.1.b <= 1.5.1.a'].str.count(
            "Blank").sum()
        count_condition_6_Probable_Reporting_Error = df['1.5.1.b <= 1.5.1.a'].str.count(
            "Probable Reporting Error").sum()

        df['2.1.2 <= 2.1.1.a + 2.1.1.b'] = df.apply(res7, axis=1)
        count_condition_7_consistent = df['2.1.2 <= 2.1.1.a + 2.1.1.b'].str.count(
            "consistent").sum()
        count_condition_7_inconsistent = df['2.1.2 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_7_blank = df['2.1.2 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Blank").sum()
        count_condition_7_Probable_Reporting_Error = df['2.1.2 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Probable Reporting Error").sum()

        df['2.1.3 <= 2.1.1.a + 2.1.1.b'] = df.apply(res8, axis=1)
        count_condition_8_consistent = df['2.1.3 <= 2.1.1.a + 2.1.1.b'].str.count(
            "consistent").sum()
        count_condition_8_inconsistent = df['2.1.3 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_8_blank = df['2.1.3 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Blank").sum()
        count_condition_8_Probable_Reporting_Error = df['2.1.3 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Probable Reporting Error").sum()

        df['2.2.2 <= 2.2'] = df.apply(res9, axis=1)
        count_condition_9_consistent = df['2.2.2 <= 2.2'].str.count(
            "consistent").sum()
        count_condition_9_inconsistent = df['2.2.2 <= 2.2'].str.count(
            "Inconsistent").sum()
        count_condition_9_blank = df['2.2.2 <= 2.2'].str.count(
            "Blank").sum()
        count_condition_9_Probable_Reporting_Error = df['2.2.2 <= 2.2'].str.count(
            "Probable Reporting Error").sum()
        
        df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res10, axis=1)
        count_condition_10_consistent = df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "consistent").sum()
        count_condition_10_inconsistent = df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Inconsistent").sum()
        count_condition_10_blank = df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Blank").sum()
        count_condition_10_Probable_Reporting_Error = df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Probable Reporting Error").sum()

        df['6.1.1 <= 3.1.1.a + 3.1.1.b'] = df.apply(res11, axis=1)
        count_condition_11_consistent = df['6.1.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_11_inconsistent = df['6.1.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_11_blank = df['6.1.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_11_Probable_Reporting_Error = df['6.1.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Probable Reporting Error").sum()

        df['6.1.9 <= 3.1.1.a + 3.1.1.b'] = df.apply(res12, axis=1)
        count_condition_12_consistent = df['6.1.9 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_12_inconsistent = df['6.1.9 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_12_blank = df['6.1.9 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_12_Probable_Reporting_Error = df['6.1.9 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Probable Reporting Error").sum()

        df['6.1.13 <= 3.1.1.a + 3.1.1.b'] = df.apply(res13, axis=1)
        count_condition_13_consistent = df['6.1.13 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_13_inconsistent = df['6.1.13 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_13_blank = df['6.1.13 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_13_Probable_Reporting_Error = df['6.1.13 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Probable Reporting Error").sum()

        df['2.2.1 <= 2.2'] = df.apply(res14, axis=1)
        count_condition_14_consistent = df['2.2.1 <= 2.2'].str.count(
            "consistent").sum()
        count_condition_14_inconsistent = df['2.2.1 <= 2.2'].str.count(
            "Inconsistent").sum()
        count_condition_14_blank = df['2.2.1 <= 2.2'].str.count(
            "Blank").sum()
        count_condition_14_Probable_Reporting_Error = df['2.2.1 <= 2.2'].str.count(
            "Probable Reporting Error").sum()

        df['3.1.2 <= 3.1.1.a + 3.1.1.b'] = df.apply(res15, axis=1)
        count_condition_15_consistent = df['3.1.2 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_15_inconsistent = df['3.1.2 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_15_blank = df['3.1.2 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_15_Probable_Reporting_Error = df['3.1.2 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Probable Reporting Error").sum()

        df['3.3.1 <= 3.1.1.a + 3.1.1.b'] = df.apply(res16, axis=1)
        count_condition_16_consistent = df['3.3.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_16_inconsistent = df['3.3.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_16_blank = df['3.3.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_16_Probable_Reporting_Error = df['3.3.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Probable Reporting Error").sum()

        df['3.3.2 <= 3.3.1'] = df.apply(res17, axis=1)
        count_condition_17_consistent = df['3.3.2 <= 3.3.1'].str.count(
            "consistent").sum()
        count_condition_17_inconsistent = df['3.3.2 <= 3.3.1'].str.count(
            "Inconsistent").sum()
        count_condition_17_blank = df['3.3.2 <= 3.3.1'].str.count(
            "Blank").sum()
        count_condition_17_Probable_Reporting_Error = df['3.3.2 <= 3.3.1'].str.count(
            "Probable Reporting Error").sum()

        df['3.3.3 <= 3.1.1.a + 3.1.1.b'] = df.apply(res18, axis=1)
        count_condition_18_consistent = df['3.3.3 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_18_inconsistent = df['3.3.3 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_18_blank = df['3.3.3 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_18_Probable_Reporting_Error = df['3.3.3 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Probable Reporting Error").sum()

        df['4.1 <= 2.1.1.a + 2.1.1.b'] = df.apply(res19, axis=1)
        count_condition_19_consistent = df['4.1 <= 2.1.1.a + 2.1.1.b'].str.count(
            "consistent").sum()
        count_condition_19_inconsistent = df['4.1 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_19_blank = df['4.1 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Blank").sum()
        count_condition_19_Probable_Reporting_Error = df['4.1 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Probable Reporting Error").sum()

        df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res20, axis=1)
        count_condition_20_consistent = df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "consistent").sum()
        count_condition_20_inconsistent = df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Inconsistent").sum()
        count_condition_20_blank = df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Blank").sum()
        count_condition_20_Probable_Reporting_Error = df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Probable Reporting Error").sum()

        df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'] = df.apply(res21, axis=1)
        count_condition_21_consistent = df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'].str.count(
            "consistent").sum()
        count_condition_21_inconsistent = df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'].str.count(
            "Inconsistent").sum()
        count_condition_21_blank = df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'].str.count(
            "Blank").sum()
        count_condition_21_Probable_Reporting_Error = df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'].str.count(
            "Probable Reporting Error").sum()

        df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(res22, axis=1)
        count_condition_22_consistent = df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "consistent").sum()
        count_condition_22_inconsistent = df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Inconsistent").sum()
        count_condition_22_blank = df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Blank").sum()
        count_condition_22_Probable_Reporting_Error = df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Probable Reporting Error").sum()

        df['6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(res23, axis=1)
        count_condition_23_consistent = df['6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "consistent").sum()
        count_condition_23_inconsistent = df['6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Inconsistent").sum()
        count_condition_23_blank = df['6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Blank").sum()
        count_condition_23_Probable_Reporting_Error= df['6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Probable Reporting Error").sum()

        df['6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(res24, axis=1)
        count_condition_24_consistent = df['6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "consistent").sum()
        count_condition_24_inconsistent = df['6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Inconsistent").sum()
        count_condition_24_blank = df['6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Blank").sum()
        count_condition_24_Probable_Reporting_Error = df['6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Probable Reporting Error").sum()

        df['6.7.3<=6.7.2'] = df.apply(res25, axis=1)
        count_condition_25_consistent = df['6.7.3<=6.7.2'].str.count(
            "consistent").sum()
        count_condition_25_inconsistent = df['6.7.3<=6.7.2'].str.count(
            "Inconsistent").sum()
        count_condition_25_blank = df['6.7.3<=6.7.2'].str.count(
            "Blank").sum()
        count_condition_25_Probable_Reporting_Error = df['6.7.3<=6.7.2'].str.count(
            "Probable Reporting Error").sum()

        df['10.1.2<=10.1.1'] = df.apply(res26, axis=1)
        count_condition_26_consistent = df['10.1.2<=10.1.1'].str.count(
            "consistent").sum()
        count_condition_26_inconsistent = df['10.1.2<=10.1.1'].str.count(
            "Inconsistent").sum()
        count_condition_26_blank = df['10.1.2<=10.1.1'].str.count(
            "Blank").sum()
        count_condition_26_Probable_Reporting_Error = df['10.1.2<=10.1.1'].str.count(
            "Probable Reporting Error").sum()

        df['10.2.1.b<=10.2.1.a'] = df.apply(res27, axis=1)
        count_condition_27_consistent = df['10.2.1.b<=10.2.1.a'].str.count(
            "consistent").sum()
        count_condition_27_inconsistent = df['10.2.1.b<=10.2.1.a'].str.count(
            "Inconsistent").sum()
        count_condition_27_blank = df['10.2.1.b<=10.2.1.a'].str.count(
            "Blank").sum()
        count_condition_27_Probable_Reporting_Error = df['10.2.1.b<=10.2.1.a'].str.count(
            "Probable Reporting Error").sum()

        df['3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2'] = df.apply(res28, axis=1)
        count_condition_28_consistent = df['3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2'].str.count(
            "consistent").sum()
        count_condition_28_inconsistent = df['3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2'].str.count(
            "Inconsistent").sum()
        count_condition_28_blank = df['3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2'].str.count(
            "Blank").sum()
        count_condition_28_Probable_Reporting_Error = df['3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2'].str.count(
            "Probable Reporting Error").sum()

        df['8.1.1.c<=8.1.1.a'] = df.apply(res29, axis=1)
        count_condition_29_consistent = df['8.1.1.c<=8.1.1.a'].str.count(
            "consistent").sum()
        count_condition_29_inconsistent = df['8.1.1.c<=8.1.1.a'].str.count(
            "Inconsistent").sum()
        count_condition_29_blank = df['8.1.1.c<=8.1.1.a'].str.count(
            "Blank").sum()
        count_condition_29_Probable_Reporting_Error = df['8.1.1.c<=8.1.1.a'].str.count(
            "Probable Reporting Error").sum()

        df['9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8'] = df.apply(res30, axis=1)
        count_condition_30_consistent = df['9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8'].str.count(
            "consistent").sum()
        count_condition_30_inconsistent = df['9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8'].str.count(
            "Inconsistent").sum()
        count_condition_30_blank = df['9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8'].str.count(
            "Blank").sum()
        count_condition_30_Probable_Reporting_Error= df['9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8'].str.count(
            "Probable Reporting Error").sum()

        df['8.1.1.b<=8.1.1.a'] = df.apply(res31, axis=1)
        count_condition_31_consistent = df['8.1.1.b<=8.1.1.a'].str.count(
            "consistent").sum()
        count_condition_31_inconsistent = df['8.1.1.b<=8.1.1.a'].str.count(
            "Inconsistent").sum()
        count_condition_31_blank = df['8.1.1.b<=8.1.1.a'].str.count(
            "Blank").sum()
        count_condition_31_Probable_Reporting_Error = df['8.1.1.b<=8.1.1.a'].str.count(
            "Probable Reporting Error").sum()

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


        table_result = pd.DataFrame({"Conditions": ["4.3 <= 2.1.1.a + 2.1.1.b + 2.2", "1.1 <= 1.1.1", "1.3.1.a <= 1.3.1", "1.2.7 <= 1.1", "1.5.1.a <= 1.1", "1.5.1.b <= 1.5.1.a", "2.1.2 <= 2.1.1.a + 2.1.1.b", "2.1.3 <= 2.1.1.a + 2.1.1.b", "2.2.2 <= 2.2", "4.4 <= 2.1.1.a + 2.1.1.b + 2.2", "6.1.1 <= 3.1.1.a + 3.1.1.b", "6.1.9 <= 3.1.1.a + 3.1.1.b", "6.1.13 <= 3.1.1.a + 3.1.1.b", "2.2.1 <= 2.2", "3.1.2 <= 3.1.1.a + 3.1.1.b", "3.3.1 <= 3.1.1.a + 3.1.1.b", "3.3.2 <= 3.3.1", "3.3.3 <= 3.1.1.a + 3.1.1.b","4.1 <= 2.1.1.a + 2.1.1.b", "5.2 <= 2.1.1.a + 2.1.1.b + 2.2","6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2", "6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4", "6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4", "6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4","6.7.3<=6.7.2","10.1.2<=10.1.1","10.2.1.b<=10.2.1.a","3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2","8.1.1.c<=8.1.1.a","9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8","8.1.1.b<=8.1.1.a", "Total count"],
        #  "Conditions": ["4.3 <= 2.1.1.a + 2.1.1.b + 2.2", "1.1 <= 1.1.1", "1.3.1.a <= 1.3.1", "1.2.7 <= 1.1", "1.5.1.a <= 1.1", "1.5.1.b <= 1.5.1.a", "2.1.2 <= 2.1.1.a + 2.1.1.b", "2.1.3 <= 2.1.1.a + 2.1.1.b", "2.2.2 <= 2.2", "4.4 <= 2.1.1.a + 2.1.1.b + 2.2", "6.1.1 <= 3.1.1.a + 3.1.1.b", "6.1.9 <= 3.1.1.a + 3.1.1.b", "6.1.13 <= 3.1.1.a + 3.1.1.b", "2.2.1 <= 2.2", "3.1.2 <= 3.1.1.a + 3.1.1.b", "3.3.1 <= 3.1.1.a + 3.1.1.b", "3.3.2 <= 3.3.1", "3.3.3 <= 3.1.1.a + 3.1.1.b","4.1 <= 2.1.1.a + 2.1.1.b", "5.2 <= 2.1.1.a + 2.1.1.b + 2.2","6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2", "6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4", "6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4", "6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4","6.7.3<=6.7.2","10.1.2<=10.1.1","10.2.1.b<=10.2.1.a","3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2","8.1.1.c<=8.1.1.a","9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8","8.1.1.b<=8.1.1.a", "Total count"],
        "Consistent": [count_condition_1_consistent, count_condition_2_consistent, count_condition_3_consistent, count_condition_4_consistent, count_condition_5_consistent, count_condition_6_consistent, count_condition_7_consistent, count_condition_8_consistent, count_condition_9_consistent, count_condition_10_consistent, count_condition_11_consistent, count_condition_12_consistent, count_condition_13_consistent, count_condition_14_consistent, count_condition_15_consistent, count_condition_16_consistent, count_condition_17_consistent,count_condition_18_consistent,count_condition_19_consistent,count_condition_20_consistent,count_condition_21_consistent,count_condition_22_consistent,count_condition_23_consistent,count_condition_24_consistent, count_condition_25_consistent, count_condition_26_consistent, count_condition_27_consistent, count_condition_28_consistent, count_condition_29_consistent, count_condition_30_consistent, count_condition_31_consistent, (count_condition_1_consistent+count_condition_2_consistent+count_condition_3_consistent+count_condition_4_consistent+count_condition_5_consistent+count_condition_6_consistent+count_condition_7_consistent+count_condition_8_consistent+count_condition_9_consistent+count_condition_10_consistent+count_condition_11_consistent+count_condition_12_consistent+count_condition_13_consistent+count_condition_14_consistent+count_condition_15_consistent+count_condition_16_consistent+count_condition_17_consistent+count_condition_18_consistent+count_condition_19_consistent+count_condition_20_consistent+count_condition_21_consistent+count_condition_22_consistent+count_condition_23_consistent+count_condition_24_consistent+count_condition_25_consistent+count_condition_26_consistent+count_condition_27_consistent+count_condition_28_consistent+count_condition_29_consistent+count_condition_30_consistent+count_condition_31_consistent)],
        "Inconsistent": [count_condition_1_inconsistent, count_condition_2_inconsistent, count_condition_3_inconsistent, count_condition_4_inconsistent, count_condition_5_inconsistent, count_condition_6_inconsistent, count_condition_7_inconsistent, count_condition_8_inconsistent,count_condition_9_inconsistent, count_condition_10_inconsistent, count_condition_11_inconsistent, count_condition_12_inconsistent, count_condition_13_inconsistent, count_condition_14_inconsistent, count_condition_15_inconsistent,count_condition_16_inconsistent,count_condition_17_inconsistent,count_condition_18_inconsistent,count_condition_19_inconsistent,count_condition_20_inconsistent,count_condition_21_inconsistent,count_condition_22_inconsistent, count_condition_23_inconsistent, count_condition_24_inconsistent, count_condition_25_inconsistent, count_condition_26_inconsistent, count_condition_27_inconsistent, count_condition_28_inconsistent, count_condition_29_inconsistent, count_condition_30_inconsistent,count_condition_31_inconsistent,(count_condition_1_inconsistent+count_condition_2_inconsistent + count_condition_3_inconsistent+count_condition_4_inconsistent+count_condition_5_inconsistent+count_condition_6_inconsistent+count_condition_7_inconsistent+count_condition_8_inconsistent+count_condition_9_inconsistent+count_condition_10_inconsistent+count_condition_11_inconsistent+count_condition_12_inconsistent+count_condition_13_inconsistent+count_condition_14_inconsistent+count_condition_15_inconsistent+count_condition_16_inconsistent+count_condition_17_inconsistent+count_condition_18_inconsistent+count_condition_19_inconsistent+count_condition_20_inconsistent+count_condition_21_inconsistent+count_condition_22_inconsistent+count_condition_23_inconsistent+count_condition_24_inconsistent+count_condition_25_inconsistent+count_condition_26_inconsistent+count_condition_27_inconsistent+count_condition_28_inconsistent+count_condition_29_inconsistent+count_condition_30_inconsistent+count_condition_31_inconsistent)],
        "Blank": [count_condition_1_blank, count_condition_2_blank, count_condition_3_blank, count_condition_4_blank, count_condition_5_blank, count_condition_6_blank, count_condition_7_blank, count_condition_8_blank, count_condition_9_blank, count_condition_10_blank, count_condition_11_blank, count_condition_12_blank, count_condition_13_blank, count_condition_14_blank, count_condition_15_blank, count_condition_16_blank,count_condition_17_blank,count_condition_18_blank,count_condition_19_blank,count_condition_20_blank,count_condition_21_blank, count_condition_22_blank, count_condition_23_blank, count_condition_24_blank, count_condition_25_blank, count_condition_26_blank, count_condition_27_blank, count_condition_28_blank, count_condition_29_blank, count_condition_30_blank, count_condition_31_blank, (count_condition_1_blank+count_condition_2_blank+count_condition_3_blank+count_condition_4_blank+count_condition_5_blank+count_condition_6_blank+count_condition_7_blank+count_condition_8_blank+count_condition_9_blank+count_condition_10_blank+count_condition_11_blank+count_condition_12_blank+count_condition_13_blank+count_condition_14_blank+count_condition_15_blank+count_condition_16_blank+count_condition_17_blank+count_condition_18_blank+count_condition_19_blank+count_condition_20_blank+count_condition_21_blank+count_condition_22_blank+count_condition_23_blank+count_condition_24_blank+count_condition_25_blank+count_condition_26_blank+count_condition_27_blank+count_condition_28_blank+count_condition_29_blank+count_condition_30_blank+count_condition_31_blank)],
        "Probable Reporting Error": [count_condition_1_Probable_Reporting_Error, count_condition_2_Probable_Reporting_Error, count_condition_3_Probable_Reporting_Error, count_condition_4_Probable_Reporting_Error, count_condition_5_Probable_Reporting_Error, count_condition_6_Probable_Reporting_Error, count_condition_7_Probable_Reporting_Error, count_condition_8_Probable_Reporting_Error,count_condition_9_Probable_Reporting_Error, count_condition_10_Probable_Reporting_Error, count_condition_11_Probable_Reporting_Error, count_condition_12_Probable_Reporting_Error, count_condition_13_Probable_Reporting_Error, count_condition_14_Probable_Reporting_Error, count_condition_15_Probable_Reporting_Error,count_condition_16_Probable_Reporting_Error,count_condition_17_Probable_Reporting_Error,count_condition_18_Probable_Reporting_Error,count_condition_19_Probable_Reporting_Error,count_condition_20_Probable_Reporting_Error,count_condition_21_Probable_Reporting_Error,count_condition_22_Probable_Reporting_Error,count_condition_23_Probable_Reporting_Error,count_condition_24_Probable_Reporting_Error, count_condition_25_Probable_Reporting_Error, count_condition_26_Probable_Reporting_Error, count_condition_27_Probable_Reporting_Error, count_condition_28_Probable_Reporting_Error, count_condition_29_Probable_Reporting_Error, count_condition_30_Probable_Reporting_Error,count_condition_31_Probable_Reporting_Error, (count_condition_1_Probable_Reporting_Error+count_condition_2_Probable_Reporting_Error+count_condition_3_Probable_Reporting_Error+count_condition_4_Probable_Reporting_Error+count_condition_5_Probable_Reporting_Error+count_condition_6_Probable_Reporting_Error+count_condition_7_Probable_Reporting_Error+count_condition_8_Probable_Reporting_Error+count_condition_9_Probable_Reporting_Error+count_condition_10_Probable_Reporting_Error+count_condition_11_Probable_Reporting_Error+count_condition_12_Probable_Reporting_Error+count_condition_13_Probable_Reporting_Error+count_condition_14_Probable_Reporting_Error+count_condition_15_Probable_Reporting_Error+count_condition_16_Probable_Reporting_Error+count_condition_17_Probable_Reporting_Error+count_condition_18_Probable_Reporting_Error+count_condition_19_Probable_Reporting_Error+count_condition_20_Probable_Reporting_Error+count_condition_21_Probable_Reporting_Error+count_condition_22_Probable_Reporting_Error+count_condition_23_Probable_Reporting_Error+ count_condition_24_Probable_Reporting_Error+count_condition_25_Probable_Reporting_Error+count_condition_26_Probable_Reporting_Error+count_condition_27_Probable_Reporting_Error+count_condition_28_Probable_Reporting_Error+count_condition_29_Probable_Reporting_Error+count_condition_30_Probable_Reporting_Error+count_condition_31_Probable_Reporting_Error)]})
        
        
        # Mergining current result of modified checks with original dataframe and displaying it on screen
        frames =  [df_, df]
        print(frames)
        df = pd.concat(frames,axis=1, sort=False)
        #df = df.dropna(axis=0, subset=['col_2']) 
        self.tableView.setModel(PandasModel(df))
        
        return df


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

    # Select State Functionality
    def onSelectState(self, index):
        global list_set
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
        item = df['col_3'].to_list()
        
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
        self.pushButton_4.setMenu(self.menu)

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
        j=0 
        for j in range(df.shape[0]):
            item = df['col_3'].to_list()
            
            print(self.keywords[self.col])
            #if self.keywords[self.col]:
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
                                     QtCore.Qt.Horizontal, self.menu)

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

        j=0 
        for j in range(df['col_5'].shape[0]):
            item = df['col_5'].to_list()
            
            #if self.keywords[self.col]:
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
                                     QtCore.Qt.Horizontal, self.menu)

        # ok selected                             
        btn.accepted.connect(self.menuCloseFacilityName)
        # rejected , nothing selected
        btn.rejected.connect(self.menu.close)

        checkableAction = QtWidgets.QWidgetAction(self.menu)
        checkableAction.setDefaultWidget(btn)
        self.menu.addAction(checkableAction)

        ############# Always set Pushbutton ####################
        self.pushButton_6.setMenu(self.menu)

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
        global df
        #keywords = dict([(i, []) for i in range(self.filterall.columnCount())])
        columnsShow = dict([(i, True) for i in range(df['col_14'].shape[0])])
        print(columnsShow)

        j=0 
        for j in range(df['col_14'].shape[0]):
            item = df['col_14'].to_list()
            
            #if self.keywords[self.col]:
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
                                     QtCore.Qt.Horizontal, self.menu)

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

        j=0 
        for j in range(df['col_1'].shape[0]):
            item = df['col_1'].to_list()
            
            #if self.keywords[self.col]:
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
                                     QtCore.Qt.Horizontal, self.menu)

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

        j=0 
        for j in range(df['col_2'].shape[0]):
            item = df['col_2'].to_list()
            
            #if self.keywords[self.col]:
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

    def export(self):
        filename = QFileDialog.getSaveFileName(Dialog, "Save to CSV", "Validation_table",
                                               "Comma Separated Values Spreadsheet (*.csv);;"
                                               "All Files (*)")[0]
        
        filename = filename + ".csv"
        df.to_csv(filename, index=False)

        filename1 = filename + ' _Summary_Report ' + '.csv'
        table_result.to_csv(filename1, index=False)

        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setText(("{}\n\n and \n\n {}  \n\n exported to the file location you have chosen".format(filename, filename1)))
        msg.exec()

    def reset(self):
        self.comboBox.clear()
        self.pushButton.setEnabled(True)
        products = {'_': [' ']}
        blank_df = pd.DataFrame(products, columns= ['_'])
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
