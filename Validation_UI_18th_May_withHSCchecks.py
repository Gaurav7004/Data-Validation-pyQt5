from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
import sys

from pandas.core import frame


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
        self.comboBox.setPlaceholderText('Select Facility Type')
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

        fileName, _ = QFileDialog.getOpenFileName(Dialog, "Open CSV",(QtCore.QDir.homePath()), "CSV (*.csv)")
        #fileName, _ = QFileDialog.getOpenFileName(Dialog, "Open Excel",(QtCore.QDir.homePath()), "Excel (*.xlsx)")
        
        # displaying filename in display box
        self.lineEdit.setText(fileName)
        
        # reading csv files
        df_ = pd.read_csv(fileName)


        #grab the first row for the header
        new_header = df_.iloc[1] 

        #set the header row as the df header
        df_.columns = new_header 

        df_.columns = ['col_' + str(index) for index in range(1, len(df_.columns)+1)]

        # Original Headers
        df_OrgHeaders = df_.iloc[[0, 1]]
        
        # Dropping first two indexes
        df_.drop(df_.index[[0, 1]], inplace=True)
        
        
        # Splitting Date Column into two columns
        df_[["Date", "Month"]] = df_["col_1"].str.split(pat="_", expand=True)
        df_.drop('col_1', axis=1, inplace=True)
        df_1 = df_[["Date", "Month"]]
        
        Frames = [df_1, df_]
        df_ = pd.concat(Frames, axis=1)
        df_.rename(columns = {'Date':'col_1', 'Month':'col_2'}, inplace=True)
        
        # convert the set to the list and fill inside comboBox to select facility type
        list_set = df_['col_11'].tolist()
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

                # Signaling HSC_Validate function
                self.pushButton_2.clicked.connect(self.HSC_Validate)

                # Signaling onSelectState function i.e dropdown to select state
                self.pushButton_5.clicked.connect(self.onSelectState)

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
        self.model = PandasModel(df_)
        return df_


    # Validation for HSC 
    def HSC_Validate(self):
        global df
        df = self.loadFile(df_)
        print('Entered HSC_Validate')

        # Modified Checks of HSC

        # # 4.3 <= 2.1.1.a + 2.1.1.b + 2.2  (For recurring data items)
        # def res1(df):
            
        #     if float(df['col_74']) > float(df['col_48']) + float(df['col_49']) + float(df['col_52']):
        #         return 'Inconsistent'            
        #     elif pd.isnull(df['col_74']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']) and pd.isnull(df['col_52']):
        #         return 'Blank'
        #     elif pd.isnull(df['col_74']) or pd.isnull(df['col_48']) or pd.isnull(df['col_49']) or pd.isnull(df['col_52']):
        #         return 'Probable Reporting Error'            
        #     else:
        #         # Calculating percentage rate
        #         num = float(df['col_74'])
        #         den = float(df['col_48'] + df['col_49'] + df['col_52'])
                
        #         if den == 0:
        #             # Since if the numbers are 0 then denominator cannot be 0
        #             return 'Probable Reporting Error'
        #         else:
        #             per_value = float((num/den) * 100)                
        #             if per_value < float(50):
        #                 return 'Probable Reporting Error (Less than 50%)'
        #             else:
        #                 return 'Consistent'
        #             return df


        # 1.1(col_21) >= 1.1.1(col_22) (for related data items)
        def res2(df):
            if float(df['col_21']) < float(df['col_22']):
                return 'Inconsistent (Check Fails)'
            elif pd.isnull(float(df['col_21'])) and pd.isnull(float(df['col_22'])):
                return 'Blank'
            elif pd.isnull(float(df['col_21'])) or pd.isnull(float(df['col_22'])):
                if pd.isnull(df['col_21']):
                    return 'Inconsistent (Source is null)'
                elif pd.isnull(df['col_22']):
                    return 'Probable Reporting Error (1.1.1 is blank)' 
            elif float(df['col_21']) == 0 and float(df['col_22']) == 0 :     
                return 'consistent'
            else:
                return 'consistent'
            return df

        
        # 1.3.1.a <= 1.3.1 (for related data items) 
        def res3(df):
            if float(df['col_32']) > float(df['col_31']):
                return 'Inconsistent (Check Fails)'
            elif pd.isnull(float(df['col_32'])) and pd.isnull(float(df['col_31'])):
                return 'Blank'
            elif pd.isnull(float(df['col_32'])) or pd.isnull(float(df['col_31'])):
                if pd.isnull(df['col_32']):
                    return 'Inconsistent (Source is null)'
                elif pd.isnull(df['col_31']):
                    return 'Probable Reporting Error (1.3.1 is blank)' 
            elif float(df['col_32']) == 0 and float(df['col_31']) == 0 :     
                return 'consistent'
            else:
                return 'consistent'
            return df

        
        # # 1.2.7 <= 1.1 (For recurring data items)
        # def res4(df):
        #     if float(df['col_29']) > float(df['col_21']):
        #         return 'Inconsistent'
        #     elif pd.isnull(float(df['col_29'])) and pd.isnull(float(df['col_21'])):
        #         return 'Blank'
        #     elif pd.isnull(float(df['col_29'])) or pd.isnull(float(df['col_21'])):
        #         if pd.isnull(df['col_29']):
        #             return 'Blank Error (1.2.7 is blank)'
        #         elif pd.isnull(df['col_21']):
        #             return 'Blank Error (1.1 is blank)' 
        #     elif float(df['col_29']) == 0 and float(df['col_21']) == 0 :     
        #         return 'consistent'
        #     else:
        #         return 'consistent'
        #     return df

        # # 1.5.1.a <= 1.1 (for unrelated data items)
        def res5(df):
            if float(df['col_41']) > float(df['col_21']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(float(df['col_41'])) and pd.isnull(float(df['col_21'])):
                return 'Blank'
            elif pd.isnull(float(df['col_41'])) or pd.isnull(float(df['col_21'])):
                if pd.isnull(df['col_41']):
                    return 'Probable Reporting Error(1.5.1.a is blank)'
                elif pd.isnull(df['col_21']):
                    return 'Inconsistent (1.1 is blank)' 
            elif float(df['col_41']) == 0 and float(df['col_21']) == 0 :     
                return 'consistent'
            else:
                return 'consistent'
            return df

        # 1.5.1.b (col_42) <= 1.5.1.a (col_41) (for related data items) 
        def res6(df):
            if float(df['col_42']) > float(df['col_41']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(float(df['col_42'])) and pd.isnull(float(df['col_41'])):
                return 'Blank'
            elif pd.isnull(float(df['col_42'])) or pd.isnull(float(df['col_41'])):
                if pd.isnull(df['col_42']):
                    return 'Probable Reporting Error (1.5.1.b is blank)'
                elif pd.isnull(df['col_41']):
                    return 'Inconsistent (1.5.1.a is blank)' 
            elif float(df['col_41']) == 0 and float(df['col_21']) == 0 :     
                return 'consistent'
            else:
                return 'consistent'
            return df

          # 2.1.2 (col_50) <= 2.1.1.a(col_48) + 2.1.1.b(col_49) (for unrelated data items)
        def res7(df):
            if float(df['col_50']) > float(df['col_48']) + float(df['col_49']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_50']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']):
                return 'Blank'
            elif pd.isnull(df['col_50']) or pd.isnull(df['col_48']) or pd.isnull(df['col_49']):
                if pd.isnull(df['col_50']):
                    return 'Probable Reporting Error (2.1.2 is blank)'
                elif pd.isnull(df['col_48']):
                    return 'Inconsistent (2.1.1.a is blank)'
                elif pd.isnull(df['col_49']):
                    return 'Inconsistent (2.1.1.b is blank)'
            elif float(df['col_50']) == float(df['col_48']) + float(df['col_49']):
                return 'consistent'
            else:
                return 'consistent'
            return df

        #     # 2.1.3 (col_51) <= 2.1.1.a(col_48) + 2.1.1.b(col_49) (For recurring data items)
        # def res8(df):
        #     if float(df['col_51']) > float(df['col_48']) + float(df['col_49']):
        #         return 'Inconsistent'
        #     elif pd.isnull(df['col_51']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']):
        #         return 'Blank'
        #     elif pd.isnull(df['col_51']) or pd.isnull(df['col_48']) or pd.isnull(df['col_49']):
        #         if pd.isnull(df['col_51']):
        #             return 'Blank Error (2.1.3 is blank)'
        #         elif pd.isnull(df['col_48']):
        #             return 'Blank Error (2.1.1.a is blank)'
        #         elif pd.isnull(df['col_49']):
        #             return 'Blank Error (2.1.1.a is blank)'
        #     elif pd.isnull(df['col_51']) == pd.isnull(df['col_48']) + pd.isnull(df['col_49']):
        #         return 'consistent'
        #     else:
        #         return 'consistent'
        #     return df

        #     # 2.2.2(col_54) <= 2.2 (col_52) (For recurring data items)
        # def res9(df):
        #     if float(df['col_54']) > float(df['col_52']):
        #         return 'Inconsistent'
        #     elif pd.isnull(df['col_54']) and pd.isnull(df['col_52']):
        #         return 'Blank'
        #     elif pd.isnull(df['col_54']) or pd.isnull(df['col_52']):
        #         if pd.isnull(df['col_52']):
        #             return 'Blank Error (2.2.2 is blank)'
        #         elif pd.isnull(df['col_54']):
        #             return 'Blank Error (2.2 is blank)'
        #     elif pd.isnull(df['col_54']) == pd.isnull(df['col_52']):
        #         return 'consistent'
        #     else:
        #         return 'consistent'
        #     return df

        #      # 4.4(col_75)<= 2.1.1.a(col_48) + 2.1.1.b(col_49) + 2.2(col_52) (For recurring data items)
        # def res10(df):
        #     if float(df['col_75']) > float(df['col_48']) + float(df['col_49']) + float(df['col_52']):
        #         return 'Inconsistent'
        #     elif pd.isnull(df['col_75']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']) and pd.isnull(df['col_50']):
        #         return 'Blank'
        #     elif pd.isnull(df['col_75']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']) and pd.isnull(df['col_50']):
        #         if pd.isnull(df['col_75']):
        #             return 'Blank Error (4.4 is blank)'
        #         elif pd.isnull(df['col_48']):
        #             return 'Blank Error (2.1.1.a is blank)'
        #         elif pd.isnull(df['col_49']):
        #             return 'Blank Error (2.1.1.b is blank)'
        #         elif pd.isnull(df['col_52']):
        #             return 'Blank Error (2.2 is blank)'
        #     elif pd.isnull(df['col_75']) == pd.isnull(df['col_48']) + pd.isnull(df['col_49']) + pd.isnull(df['col_50']):
        #         return 'consistent'
        #     else:
        #         return 'consistent'
        #     return df

         # 6.1.1(col_105) <= 3.1.1.a(col_57) + 3.1.1.b(col_58)
        def res11(df):
            if float(df['col_105']) > float(df['col_57']) + float(df['col_58']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_105']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'Blank'
            elif pd.isnull(df['col_105']) or pd.isnull(df['col_57']) or pd.isnull(df['col_58']):
                if pd.isnull(df['col_105']):
                    return 'Probable Reporting Error (6.1.1 is blank)'
                elif pd.isnull(df['col_57']):
                    return 'Inconsistent (3.1.1.a is blank)'
                elif pd.isnull(df['col_58']):
                    return 'Inconsistent (3.1.1.b is blank)'
            elif pd.isnull(df['col_105']) == pd.isnull(df['col_57']) + pd.isnull(df['col_58']):
                return 'consistent'
            else:
                return 'consistent'
            return df

        # 6.1.9(col_113) <= 3.1.1.a(col_57) + 3.1.1.b(col_58)
        def res12(df):
            if float(df['col_113']) > float(df['col_57']) + float(df['col_58']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_113']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'Blank'
            elif pd.isnull(df['col_113']) or pd.isnull(df['col_57']) or pd.isnull(df['col_58']):
                if pd.isnull(df['col_113']):
                    return 'Probable Reporting Error (6.1.9 is blank)'
                elif pd.isnull(df['col_57']):
                    return 'Inconsistent (3.1.1.a is blank)'
                elif pd.isnull(df['col_58']):
                    return 'Inconsistent (3.1.1.b is blank)'
            elif pd.isnull(df['col_113']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'consistent'
            else:
                return 'consistent'
            return df

        # 6.1.13(col_113) <= 3.1.1.a(col_57) + 3.1.1.b(col_58)
        def res13(df):
            if float(df['col_113']) > float(df['col_57']) + float(df['col_58']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_113']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'Blank'
            elif pd.isnull(df['col_113']) or pd.isnull(df['col_57']) or pd.isnull(df['col_58']):
                if pd.isnull(df['col_113']):
                    return 'Probable Reporting Error  (6.1.13 is blank)'
                elif pd.isnull(df['col_57']):
                    return 'Inconsistent (6.1.13 is blank)'
                elif pd.isnull(df['col_58']):
                    return 'Inconsistent (6.1.13 is blank)'
            elif pd.isnull(df['col_113']) == pd.isnull(df['col_57']) + pd.isnull(df['col_58']):
                return 'consistent'
            else:
                return 'consistent'
            return df

        # 2.2.1(col_41) <= 2.2(col_42)
        def res14(df):
            if float(df['col_41']) > float(df['col_42']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_41']) and pd.isnull(df['col_42']):
                return 'Blank'
            elif pd.isnull(df['col_41']) or pd.isnull(df['col_42']):
                if pd.isnull(df['col_41']):
                    return 'Probable Reporting Error (2.2.1 is blank)'
                elif pd.isnull(df['col_42']):
                    return 'Inconsistent (2.2 is blank)'
            elif pd.isnull(df['col_41']) == pd.isnull(df['col_42']):
                return 'consistent'
            else:
                return 'consistent'
            return df

         # 3.1.2(col_59) <= 3.1.1.a(col_57)+ 3.1.1.b(col_58)
        def res15(df):
            if float(df['col_59']) > float(df['col_57']) + float(df['col_58']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_59']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'Blank'
            elif pd.isnull(df['col_59']) or pd.isnull(df['col_57']) or pd.isnull(df['col_58']):
                if pd.isnull(df['col_59']):
                    return 'Probable Reporting Error (3.1.2 is blank)'
                elif pd.isnull(df['col_57']):
                    return 'Inconsistent(3.1.1.a is blank)'
                elif pd.isnull(df['col_58']):
                    return 'Inconsistent (3.1.1.b is blank)'
            elif pd.isnull(df['col_59']) == pd.isnull(df['col_57']) + pd.isnull(df['col_58']):
                return 'consistent'
            else:
                return 'consistent'
            return df

         # 3.3.1 <= 3.1.1.a + 3.1.1.b
        def res16(df):
            if float(df['col_67']) > float(df['col_57']) + float(df['col_58']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_67']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'Blank'
            elif pd.isnull(df['col_67']) or pd.isnull(df['col_57']) or pd.isnull(df['col_58']):
                if pd.isnull(df['col_67']):
                    return 'Probable Reporting Error (3.3.1 is blank)'
                elif pd.isnull(df['col_57']):
                    return 'Inconsistent (3.3.1.a is blank)'
                elif pd.isnull(df['col_58']):
                    return 'Inconsistent (3.3.1.b is blank)'
            elif pd.isnull(df['col_67']) == pd.isnull(df['col_57']) + pd.isnull(df['col_58']):
                return 'consistent'
            else:
                return 'consistent'
            return df

         # 3.3.2 <= 3.3.1
        def res17(df):
            if float(df['col_68']) > float(df['col_67']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_68']) and pd.isnull(df['col_67']):
                return 'Blank'
            elif pd.isnull(df['col_68']) or pd.isnull(df['col_67']):
                if pd.isnull(df['col_68']):
                    return 'Probable Reporting Error (3.3.2 is blank)'
                elif pd.isnull(df['col_67']):
                    return 'Inconsistent (3.3.1 is blank)'
            elif pd.isnull(df['col_68']) == pd.isnull(df['col_67']):
                return 'consistent'
            else:
                return 'consistent'
            return df

        # 3.3.3<=3.1.1.a+3.1.1.b
        def res18(df):
            if float(df['col_69']) > float(df['col_57']) + float(df['col_58']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_69']) and pd.isnull(df['col_57']) and pd.isnull(df['col_58']):
                return 'Blank'
            elif pd.isnull(df['col_69']) or pd.isnull(df['col_57']) or pd.isnull(df['col_58']):
                if pd.isnull(df['col_69']):
                    return 'Probable Reporting Error (3.3.3 is blank)'
                elif pd.isnull(df['col_57']):
                    return 'Inconsistent (3.1.1.a is blank)'
                elif pd.isnull(df['col_58']):
                    return 'Inconsistent (3.1.1.b is blank)'
            elif pd.isnull(df['col_69']) == pd.isnull(df['col_57']) + pd.isnull(df['col_58']):
                return 'consistent'
            else:
                return 'consistent'
            return df

         # 4.1 <= 2.1.1.a + 2.1.1.b
        def res19(df):
            if float(df['col_72']) > float(df['col_48']) + float(df['col_49']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_72']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']):
                return 'Blank'
            elif pd.isnull(df['col_72']) or pd.isnull(df['col_48']) or pd.isnull(df['col_49']):
                if pd.isnull(df['col_72']):
                    return 'Probable Reporting Error(4.1 is blank)'
                elif pd.isnull(df['col_48']):
                    return 'Inconsistent (2.1.1.a is blank)'
                elif pd.isnull(df['col_49']):
                    return 'Inconsistent (2.1.1.b is blank)'
            elif pd.isnull(df['col_72']) == pd.isnull(df['col_48']) + pd.isnull(df['col_49']):
                return 'consistent'
            else:
                return 'consistent'
            return df

        # 5.2 <= 2.1.1.a + 2.1.1.b + 2.2
        def res20(df):
            if float(df['col_86']) > float(df['col_48']) + float(df['col_49']) + float(df['col_52']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_86']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']) and pd.isnull(df['col_49']):
                return 'Blank'
            elif pd.isnull(df['col_86']) or pd.isnull(df['col_48']) or pd.isnull(df['col_49']) or pd.isnull(df['col_49']):
                if pd.isnull(df['col_86']):
                    return 'Probable Reporting Error(5.2 is blank)'
                elif pd.isnull(df['col_48']):
                    return 'Inconsistent (2.1.1.a is blank)'
                elif pd.isnull(df['col_49']):
                    return 'Inconsistent (2.1.1.b is blank)'
                elif pd.isnull(df['col_52']):
                    return 'Inconsistent (2.2 is blank)'
            elif pd.isnull(df['col_86']) == pd.isnull(df['col_48']) + pd.isnull(df['col_49']) + pd.isnull(df['col_49']):
                return 'Consistent'
            else:
                return 'Consistent'
            return df

         # 6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2
        def res21(df):
            if float(df['col_129']) + float(df['col_130']) > float(df['col_126']) + float(df['col_127']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_129']) and pd.isnull(df['col_130']) and pd.isnull(df['col_126']) and pd.isnull(df['col_127']):
                return 'Blank'
            elif pd.isnull(df['col_129']) or pd.isnull(df['col_130']) or pd.isnull(df['col_126']) or pd.isnull(df['col_127']):
                if pd.isnull(df['col_129']):
                    return 'Probable Reporting Error (6.2.4.a is blank)'
                elif pd.isnull(df['col_130']):
                    return 'Probable Reporting Error (6.2.4.b is blank)'
                elif pd.isnull(df['col_126']):
                    return 'Inconsistent (6.2.1 is blank)'
                elif pd.isnull(df['col_127']):
                    return 'Inconsistent(6.2.2 is blank)'
            elif pd.isnull(df['col_129']) + pd.isnull(df['col_130']) == pd.isnull(df['col_126']) + pd.isnull(df['col_127']):
                return 'Consistent'
            else:
                return 'Consistent'
            return df

        # 6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4
        def res22(df):
            if float(df['col_144']) > float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_144']) and pd.isnull(df['col_105']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']) and pd.isnull(df['col_111']) and pd.isnull(df['col_112']) and pd.isnull(df['col_113']) and pd.isnull(df['col_114']) and pd.isnull(df['col_115']) and pd.isnull(df['col_116']) and pd.isnull(df['col_117']) and pd.isnull(df['col_118']) and pd.isnull(df['col_119']) and pd.isnull(df['col_120']) and pd.isnull(df['col_121']) and pd.isnull(df['col_122']) and pd.isnull(df['col_123']) and pd.isnull(df['col_124']) and pd.isnull(df['col_125']) and pd.isnull(df['col_126']) and pd.isnull(df['col_127']) and pd.isnull(df['col_128']) and pd.isnull(df['col_131']) and pd.isnull(df['col_132']) and pd.isnull(df['col_133']) and pd.isnull(df['col_134']) and pd.isnull(df['col_135']) and pd.isnull(df['col_136']) and pd.isnull(df['col_137']) and pd.isnull(df['col_138']) and pd.isnull(df['col_139']) and pd.isnull(df['col_140']) and pd.isnull(df['col_141']) and pd.isnull(df['col_142']) and pd.isnull(df['col_143']):
                return 'Blank'
            elif pd.isnull(df['col_144']) or pd.isnull(df['col_105']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']) or pd.isnull(df['col_111']) or pd.isnull(df['col_112']) or pd.isnull(df['col_113']) or pd.isnull(df['col_114']) or pd.isnull(df['col_115']) or pd.isnull(df['col_116']) or pd.isnull(df['col_117']) or pd.isnull(df['col_118']) or pd.isnull(df['col_119']) or pd.isnull(df['col_120']) or pd.isnull(df['col_121']) or pd.isnull(df['col_122']) or pd.isnull(df['col_123']) or pd.isnull(df['col_124']) or pd.isnull(df['col_125']) or pd.isnull(df['col_126']) or pd.isnull(df['col_127']) or pd.isnull(df['col_128']) or pd.isnull(df['col_131']) or pd.isnull(df['col_132']) or pd.isnull(df['col_133']) or pd.isnull(df['col_134']) or pd.isnull(df['col_135']) or pd.isnull(df['col_136']) or pd.isnull(df['col_137']) or pd.isnull(df['col_138']) or pd.isnull(df['col_139']) or pd.isnull(df['col_140']) or pd.isnull(df['col_141']) or pd.isnull(df['col_142']) or pd.isnull(df['col_143']):
                if pd.isnull(df['col_144']):
                    return 'Probable Reporting Error (6.6.1 is blank)'
                elif pd.isnull(df['col_105']):
                    return 'Inconsistent(6.1.1 is blank)'
                elif pd.isnull(df['col_106']):
                    return 'Inconsistent(6.1.2 is blank)'
                elif pd.isnull(df['col_107']):
                    return 'Inconsistent(6.1.3 is blank)'
                elif pd.isnull(df['col_108']):
                    return 'Inconsistent(6.1.4 is blank)'
                elif pd.isnull(df['col_109']):
                    return 'Inconsistent(6.1.5 is blank)'
                elif pd.isnull(df['col_110']):
                    return 'Inconsistent(6.1.6 is blank)'
                elif pd.isnull(df['col_111']):
                    return 'Inconsistent (6.1.7 is blank)'
                elif pd.isnull(df['col_112']):
                    return 'Inconsistent(6.1.8 is blank)'
                elif pd.isnull(df['col_113']):
                    return 'Inconsistent(6.1.9 is blank)'
                elif pd.isnull(df['col_114']):
                    return 'Inconsistent(6.1.10 is blank)'
                elif pd.isnull(df['col_115']):
                    return 'Inconsistent(6.1.11 is blank)'
                elif pd.isnull(df['col_116']):
                    return 'Inconsistent(6.1.12 is blank)'
                elif pd.isnull(df['col_117']):
                    return 'Inconsistent(6.1.13 is blank)'
                elif pd.isnull(df['col_118']):
                    return 'Inconsistent(6.1.14 is blank)'
                elif pd.isnull(df['col_119']):
                    return 'Inconsistent (6.1.15 is blank)'
                elif pd.isnull(df['col_120']):
                    return 'Inconsistent (6.1.16 is blank)'
                elif pd.isnull(df['col_121']):
                    return 'Inconsistent (6.1.17 is blank)'
                elif pd.isnull(df['col_122']):
                    return 'Inconsistent (6.1.18 is blank)'
                elif pd.isnull(df['col_123']):
                    return 'Inconsistent (6.1.19 is blank)'
                elif pd.isnull(df['col_124']):
                    return 'Inconsistent (6.1.20 is blank)'
                elif pd.isnull(df['col_125']):
                    return 'Inconsistent (6.1.21 is blank)'
                elif pd.isnull(df['col_126']):
                    return 'Inconsistent (6.2.1 is blank)'
                elif pd.isnull(df['col_127']):
                    return 'Inconsistent (6.2.2 is blank)'
                elif pd.isnull(df['col_128']):
                    return 'Inconsistent (6.2.3 is blank)'
                elif pd.isnull(df['col_131']):
                    return 'Inconsistent (6.3.1 is blank)'
                elif pd.isnull(df['col_132']):
                    return 'Inconsistent (6.3.2 is blank)'
                elif pd.isnull(df['col_133']):
                    return 'Inconsistent (6.3.3 is blank)'
                elif pd.isnull(df['col_134']):
                    return 'Inconsistent (6.4.1 is blank)'
                elif pd.isnull(df['col_135']):
                    return 'Inconsistent (6.4.2 is blank)'
                elif pd.isnull(df['col_136']):
                    return 'Inconsistent (6.4.3 is blank)'
                elif pd.isnull(df['col_137']):
                    return 'Inconsistent (6.4.4 is blank)'
                elif pd.isnull(df['col_138']):
                    return 'Inconsistent (6.4.5 is blank)'
                elif pd.isnull(df['col_139']):
                    return 'Inconsistent (6.4.6 is blank)'
                elif pd.isnull(df['col_140']):
                    return 'Inconsistent (6.5.1 is blank)'
                elif pd.isnull(df['col_141']):
                    return 'Inconsistent (6.5.2 is blank)'
                elif pd.isnull(df['col_142']):
                    return 'Inconsistent (6.5.3 is blank)'
                elif pd.isnull(df['col_142']):
                    return 'Inconsistent (6.5.4 is blank)'
            elif pd.isnull(df['col_144']) == pd.isnull(df['col_105'])+ pd.isnull(df['col_106'])+ pd.isnull(df['col_107']) + pd.isnull(df['col_108']) + pd.isnull(df['col_109']) + pd.isnull(df['col_110']) + pd.isnull(df['col_111']) + pd.isnull(df['col_112']) + pd.isnull(df['col_113']) + pd.isnull(df['col_114']) + pd.isnull(df['col_115']) + pd.isnull(df['col_116']) + pd.isnull(df['col_117']) + pd.isnull(df['col_118']) + pd.isnull(df['col_119']) + pd.isnull(df['col_120']) + pd.isnull(df['col_121']) + pd.isnull(df['col_122']) + pd.isnull(df['col_123']) + pd.isnull(df['col_124']) + pd.isnull(df['col_125']) + pd.isnull(df['col_126']) + pd.isnull(df['col_127']) + pd.isnull(df['col_128']) + pd.isnull(df['col_131']) + pd.isnull(df['col_132']) + pd.isnull(df['col_133']) + pd.isnull(df['col_134']) + pd.isnull(df['col_135']) + pd.isnull(df['col_136']) + pd.isnull(df['col_137']) + pd.isnull(df['col_138']) + pd.isnull(df['col_139']) + pd.isnull(df['col_140']) + pd.isnull(df['col_141']) + pd.isnull(df['col_142']) + pd.isnull(df['col_143']):
                return 'consistent'
            else:
                return 'consistent'
            return df

        # 6.6.2<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4
        def res23(df):
            if float(df['col_145']) > float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_145']) and pd.isnull(df['col_105']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']) and pd.isnull(df['col_111']) and pd.isnull(df['col_112']) and pd.isnull(df['col_113']) and pd.isnull(df['col_114']) and pd.isnull(df['col_115']) and pd.isnull(df['col_116']) and pd.isnull(df['col_117']) and pd.isnull(df['col_118']) and pd.isnull(df['col_119']) and pd.isnull(df['col_120']) and pd.isnull(df['col_121']) and pd.isnull(df['col_122']) and pd.isnull(df['col_123']) and pd.isnull(df['col_124']) and pd.isnull(df['col_125']) and pd.isnull(df['col_126']) and pd.isnull(df['col_127']) and pd.isnull(df['col_128']) and pd.isnull(df['col_131']) and pd.isnull(df['col_132']) and pd.isnull(df['col_133']) and pd.isnull(df['col_134']) and pd.isnull(df['col_135']) and pd.isnull(df['col_136']) and pd.isnull(df['col_137']) and pd.isnull(df['col_138']) and pd.isnull(df['col_139']) and pd.isnull(df['col_140']) and pd.isnull(df['col_141']) and pd.isnull(df['col_142']) and pd.isnull(df['col_143']):
                return 'Blank'
            elif pd.isnull(df['col_145']) or pd.isnull(df['col_105']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']) or pd.isnull(df['col_111']) or pd.isnull(df['col_112']) or pd.isnull(df['col_113']) or pd.isnull(df['col_114']) or pd.isnull(df['col_115']) or pd.isnull(df['col_116']) or pd.isnull(df['col_117']) or pd.isnull(df['col_118']) or pd.isnull(df['col_119']) or pd.isnull(df['col_120']) or pd.isnull(df['col_121']) or pd.isnull(df['col_122']) or pd.isnull(df['col_123']) or pd.isnull(df['col_124']) or pd.isnull(df['col_125']) or pd.isnull(df['col_126']) or pd.isnull(df['col_127']) or pd.isnull(df['col_128']) or pd.isnull(df['col_131']) or pd.isnull(df['col_132']) or pd.isnull(df['col_133']) or pd.isnull(df['col_134']) or pd.isnull(df['col_135']) or pd.isnull(df['col_136']) or pd.isnull(df['col_137']) or pd.isnull(df['col_138']) or pd.isnull(df['col_139']) or pd.isnull(df['col_140']) or pd.isnull(df['col_141']) or pd.isnull(df['col_142']) or pd.isnull(df['col_143']):
                if pd.isnull(df['col_145']):
                    return 'Probable Reporting Error (6.6.1 is blank)'
                elif pd.isnull(df['col_105']):
                    return 'Inconsistent(6.1.1 is blank)'
                elif pd.isnull(df['col_106']):
                    return 'Inconsistent(6.1.2 is blank)'
                elif pd.isnull(df['col_107']):
                    return 'Inconsistent(6.1.3 is blank)'
                elif pd.isnull(df['col_108']):
                    return 'Inconsistent(6.1.4 is blank)'
                elif pd.isnull(df['col_109']):
                    return 'Inconsistent(6.1.5 is blank)'
                elif pd.isnull(df['col_110']):
                    return 'Inconsistent(6.1.6 is blank)'
                elif pd.isnull(df['col_111']):
                    return 'Inconsistent (6.1.7 is blank)'
                elif pd.isnull(df['col_112']):
                    return 'Inconsistent(6.1.8 is blank)'
                elif pd.isnull(df['col_113']):
                    return 'Inconsistent(6.1.9 is blank)'
                elif pd.isnull(df['col_114']):
                    return 'Inconsistent(6.1.10 is blank)'
                elif pd.isnull(df['col_115']):
                    return 'Inconsistent(6.1.11 is blank)'
                elif pd.isnull(df['col_116']):
                    return 'Inconsistent(6.1.12 is blank)'
                elif pd.isnull(df['col_117']):
                    return 'Inconsistent(6.1.13 is blank)'
                elif pd.isnull(df['col_118']):
                    return 'Inconsistent(6.1.14 is blank)'
                elif pd.isnull(df['col_119']):
                    return 'Inconsistent (6.1.15 is blank)'
                elif pd.isnull(df['col_120']):
                    return 'Inconsistent (6.1.16 is blank)'
                elif pd.isnull(df['col_121']):
                    return 'Inconsistent (6.1.17 is blank)'
                elif pd.isnull(df['col_122']):
                    return 'Inconsistent (6.1.18 is blank)'
                elif pd.isnull(df['col_123']):
                    return 'Inconsistent (6.1.19 is blank)'
                elif pd.isnull(df['col_124']):
                    return 'Inconsistent (6.1.20 is blank)'
                elif pd.isnull(df['col_125']):
                    return 'Inconsistent (6.1.21 is blank)'
                elif pd.isnull(df['col_126']):
                    return 'Inconsistent (6.2.1 is blank)'
                elif pd.isnull(df['col_127']):
                    return 'Inconsistent (6.2.2 is blank)'
                elif pd.isnull(df['col_128']):
                    return 'Inconsistent (6.2.3 is blank)'
                elif pd.isnull(df['col_131']):
                    return 'Inconsistent (6.3.1 is blank)'
                elif pd.isnull(df['col_132']):
                    return 'Inconsistent (6.3.2 is blank)'
                elif pd.isnull(df['col_133']):
                    return 'Inconsistent (6.3.3 is blank)'
                elif pd.isnull(df['col_134']):
                    return 'Inconsistent (6.4.1 is blank)'
                elif pd.isnull(df['col_135']):
                    return 'Inconsistent (6.4.2 is blank)'
                elif pd.isnull(df['col_136']):
                    return 'Inconsistent (6.4.3 is blank)'
                elif pd.isnull(df['col_137']):
                    return 'Inconsistent (6.4.4 is blank)'
                elif pd.isnull(df['col_138']):
                    return 'Inconsistent (6.4.5 is blank)'
                elif pd.isnull(df['col_139']):
                    return 'Inconsistent (6.4.6 is blank)'
                elif pd.isnull(df['col_140']):
                    return 'Inconsistent (6.5.1 is blank)'
                elif pd.isnull(df['col_141']):
                    return 'Inconsistent (6.5.2 is blank)'
                elif pd.isnull(df['col_142']):
                    return 'Inconsistent (6.5.3 is blank)'
                elif pd.isnull(df['col_142']):
                    return 'Inconsistent (6.5.4 is blank)'
            elif pd.isnull(df['col_144']) == pd.isnull(df['col_105'])+ pd.isnull(df['col_106'])+ pd.isnull(df['col_107']) + pd.isnull(df['col_108']) + pd.isnull(df['col_109']) + pd.isnull(df['col_110']) + pd.isnull(df['col_111']) + pd.isnull(df['col_112']) + pd.isnull(df['col_113']) + pd.isnull(df['col_114']) + pd.isnull(df['col_115']) + pd.isnull(df['col_116']) + pd.isnull(df['col_117']) + pd.isnull(df['col_118']) + pd.isnull(df['col_119']) + pd.isnull(df['col_120']) + pd.isnull(df['col_121']) + pd.isnull(df['col_122']) + pd.isnull(df['col_123']) + pd.isnull(df['col_124']) + pd.isnull(df['col_125']) + pd.isnull(df['col_126']) + pd.isnull(df['col_127']) + pd.isnull(df['col_128']) + pd.isnull(df['col_131']) + pd.isnull(df['col_132']) + pd.isnull(df['col_133']) + pd.isnull(df['col_134']) + pd.isnull(df['col_135']) + pd.isnull(df['col_136']) + pd.isnull(df['col_137']) + pd.isnull(df['col_138']) + pd.isnull(df['col_139']) + pd.isnull(df['col_140']) + pd.isnull(df['col_141']) + pd.isnull(df['col_142']) + pd.isnull(df['col_143']):
                return 'consistent'
            else:
                return 'consistent'
            return df

         # 6.6.3<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4
        def res24(df):
            if float(df['col_146']) > float(df['col_105']) + float(df['col_106']) + float(df['col_107']) + float(df['col_108']) + float(df['col_109']) + float(df['col_110']) + float(df['col_111']) + float(df['col_112']) + float(df['col_113']) + float(df['col_114']) + float(df['col_115']) + float(df['col_116']) + float(df['col_117']) + float(df['col_118']) + float(df['col_119']) + float(df['col_120']) + float(df['col_121']) + float(df['col_122']) + float(df['col_123']) + float(df['col_124']) + float(df['col_125']) + float(df['col_126']) + float(df['col_127']) + float(df['col_128']) + float(df['col_131']) + float(df['col_132']) + float(df['col_133']) + float(df['col_134']) + float(df['col_135']) + float(df['col_136']) + float(df['col_137']) + float(df['col_138']) + float(df['col_139']) + float(df['col_140']) + float(df['col_141']) + float(df['col_142']) + float(df['col_143']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_146']) and pd.isnull(df['col_105']) and pd.isnull(df['col_106']) and pd.isnull(df['col_107']) and pd.isnull(df['col_108']) and pd.isnull(df['col_109']) and pd.isnull(df['col_110']) and pd.isnull(df['col_111']) and pd.isnull(df['col_112']) and pd.isnull(df['col_113']) and pd.isnull(df['col_114']) and pd.isnull(df['col_115']) and pd.isnull(df['col_116']) and pd.isnull(df['col_117']) and pd.isnull(df['col_118']) and pd.isnull(df['col_119']) and pd.isnull(df['col_120']) and pd.isnull(df['col_121']) and pd.isnull(df['col_122']) and pd.isnull(df['col_123']) and pd.isnull(df['col_124']) and pd.isnull(df['col_125']) and pd.isnull(df['col_126']) and pd.isnull(df['col_127']) and pd.isnull(df['col_128']) and pd.isnull(df['col_131']) and pd.isnull(df['col_132']) and pd.isnull(df['col_133']) and pd.isnull(df['col_134']) and pd.isnull(df['col_135']) and pd.isnull(df['col_136']) and pd.isnull(df['col_137']) and pd.isnull(df['col_138']) and pd.isnull(df['col_139']) and pd.isnull(df['col_140']) and pd.isnull(df['col_141']) and pd.isnull(df['col_142']) and pd.isnull(df['col_143']):
                return 'Blank'
            elif pd.isnull(df['col_146']) or pd.isnull(df['col_105']) or pd.isnull(df['col_106']) or pd.isnull(df['col_107']) or pd.isnull(df['col_108']) or pd.isnull(df['col_109']) or pd.isnull(df['col_110']) or pd.isnull(df['col_111']) or pd.isnull(df['col_112']) or pd.isnull(df['col_113']) or pd.isnull(df['col_114']) or pd.isnull(df['col_115']) or pd.isnull(df['col_116']) or pd.isnull(df['col_117']) or pd.isnull(df['col_118']) or pd.isnull(df['col_119']) or pd.isnull(df['col_120']) or pd.isnull(df['col_121']) or pd.isnull(df['col_122']) or pd.isnull(df['col_123']) or pd.isnull(df['col_124']) or pd.isnull(df['col_125']) or pd.isnull(df['col_126']) or pd.isnull(df['col_127']) or pd.isnull(df['col_128']) or pd.isnull(df['col_131']) or pd.isnull(df['col_132']) or pd.isnull(df['col_133']) or pd.isnull(df['col_134']) or pd.isnull(df['col_135']) or pd.isnull(df['col_136']) or pd.isnull(df['col_137']) or pd.isnull(df['col_138']) or pd.isnull(df['col_139']) or pd.isnull(df['col_140']) or pd.isnull(df['col_141']) or pd.isnull(df['col_142']) or pd.isnull(df['col_143']):
                if pd.isnull(df['col_146']):
                    return 'Probable Reporting Error (6.6.1 is blank)'
                elif pd.isnull(df['col_105']):
                    return 'Inconsistent(6.1.1 is blank)'
                elif pd.isnull(df['col_106']):
                    return 'Inconsistent(6.1.2 is blank)'
                elif pd.isnull(df['col_107']):
                    return 'Inconsistent(6.1.3 is blank)'
                elif pd.isnull(df['col_108']):
                    return 'Inconsistent(6.1.4 is blank)'
                elif pd.isnull(df['col_109']):
                    return 'Inconsistent(6.1.5 is blank)'
                elif pd.isnull(df['col_110']):
                    return 'Inconsistent(6.1.6 is blank)'
                elif pd.isnull(df['col_111']):
                    return 'Inconsistent (6.1.7 is blank)'
                elif pd.isnull(df['col_112']):
                    return 'Inconsistent(6.1.8 is blank)'
                elif pd.isnull(df['col_113']):
                    return 'Inconsistent(6.1.9 is blank)'
                elif pd.isnull(df['col_114']):
                    return 'Inconsistent(6.1.10 is blank)'
                elif pd.isnull(df['col_115']):
                    return 'Inconsistent(6.1.11 is blank)'
                elif pd.isnull(df['col_116']):
                    return 'Inconsistent(6.1.12 is blank)'
                elif pd.isnull(df['col_117']):
                    return 'Inconsistent(6.1.13 is blank)'
                elif pd.isnull(df['col_118']):
                    return 'Inconsistent(6.1.14 is blank)'
                elif pd.isnull(df['col_119']):
                    return 'Inconsistent (6.1.15 is blank)'
                elif pd.isnull(df['col_120']):
                    return 'Inconsistent (6.1.16 is blank)'
                elif pd.isnull(df['col_121']):
                    return 'Inconsistent (6.1.17 is blank)'
                elif pd.isnull(df['col_122']):
                    return 'Inconsistent (6.1.18 is blank)'
                elif pd.isnull(df['col_123']):
                    return 'Inconsistent (6.1.19 is blank)'
                elif pd.isnull(df['col_124']):
                    return 'Inconsistent (6.1.20 is blank)'
                elif pd.isnull(df['col_125']):
                    return 'Inconsistent (6.1.21 is blank)'
                elif pd.isnull(df['col_126']):
                    return 'Inconsistent (6.2.1 is blank)'
                elif pd.isnull(df['col_127']):
                    return 'Inconsistent (6.2.2 is blank)'
                elif pd.isnull(df['col_128']):
                    return 'Inconsistent (6.2.3 is blank)'
                elif pd.isnull(df['col_131']):
                    return 'Inconsistent (6.3.1 is blank)'
                elif pd.isnull(df['col_132']):
                    return 'Inconsistent (6.3.2 is blank)'
                elif pd.isnull(df['col_133']):
                    return 'Inconsistent (6.3.3 is blank)'
                elif pd.isnull(df['col_134']):
                    return 'Inconsistent (6.4.1 is blank)'
                elif pd.isnull(df['col_135']):
                    return 'Inconsistent (6.4.2 is blank)'
                elif pd.isnull(df['col_136']):
                    return 'Inconsistent (6.4.3 is blank)'
                elif pd.isnull(df['col_137']):
                    return 'Inconsistent (6.4.4 is blank)'
                elif pd.isnull(df['col_138']):
                    return 'Inconsistent (6.4.5 is blank)'
                elif pd.isnull(df['col_139']):
                    return 'Inconsistent (6.4.6 is blank)'
                elif pd.isnull(df['col_140']):
                    return 'Inconsistent (6.5.1 is blank)'
                elif pd.isnull(df['col_141']):
                    return 'Inconsistent (6.5.2 is blank)'
                elif pd.isnull(df['col_142']):
                    return 'Inconsistent (6.5.3 is blank)'
                elif pd.isnull(df['col_142']):
                    return 'Inconsistent (6.5.4 is blank)'
            elif pd.isnull(df['col_144']) == pd.isnull(df['col_105'])+ pd.isnull(df['col_106'])+ pd.isnull(df['col_107']) + pd.isnull(df['col_108']) + pd.isnull(df['col_109']) + pd.isnull(df['col_110']) + pd.isnull(df['col_111']) + pd.isnull(df['col_112']) + pd.isnull(df['col_113']) + pd.isnull(df['col_114']) + pd.isnull(df['col_115']) + pd.isnull(df['col_116']) + pd.isnull(df['col_117']) + pd.isnull(df['col_118']) + pd.isnull(df['col_119']) + pd.isnull(df['col_120']) + pd.isnull(df['col_121']) + pd.isnull(df['col_122']) + pd.isnull(df['col_123']) + pd.isnull(df['col_124']) + pd.isnull(df['col_125']) + pd.isnull(df['col_126']) + pd.isnull(df['col_127']) + pd.isnull(df['col_128']) + pd.isnull(df['col_131']) + pd.isnull(df['col_132']) + pd.isnull(df['col_133']) + pd.isnull(df['col_134']) + pd.isnull(df['col_135']) + pd.isnull(df['col_136']) + pd.isnull(df['col_137']) + pd.isnull(df['col_138']) + pd.isnull(df['col_139']) + pd.isnull(df['col_140']) + pd.isnull(df['col_141']) + pd.isnull(df['col_142']) + pd.isnull(df['col_143']):
                return 'consistent'
            else:
                return 'consistent'
            return df

        # 6.7.3<=6.7.2
        def res25(df):
            if float(df['col_149']) > float(df['col_148']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_148']) and pd.isnull(df['col_149']):
                return 'Blank'
            elif pd.isnull(df['col_148']) or pd.isnull(df['col_149']):
                if pd.isnull(df['col_148']):
                    return 'Probable Reporting Error (6.7.3 is blank)'
            elif pd.isnull(df['col_149']):
                return 'Inconsistent (6.7.2 is blank)'
            elif pd.isnull(df['col_250']) == pd.isnull(df['col_249']):
                return 'consistent'
            else:
                return 'Consistent'
            return df

        # 10.1.2<=10.1.1
        def res26(df):
            if float(df['col_250']) > float(df['col_249']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_250']) and pd.isnull(df['col_249']):
                return 'Blank'
            elif pd.isnull(df['col_250']) and pd.isnull(df['col_249']):
                if pd.isnull(df['col_250']):
                    return 'Probable Reporting Error (10.1.2 is blank)'
                elif pd.isnull(df['col_249']):
                    return 'Inconsistent (10.1.1 is blank)'
            elif pd.isnull(df['col_250']) and pd.isnull(df['col_249']):
                return 'Consistent'
            else:
                return 'Consistent'
            return df

        # 10.2.1.b<=10.2.1.a
        def res27(df):
            if float(df['col_256']) > float(df['col_255']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_256']) and pd.isnull(df['col_255']):
                return 'Blank'
            elif pd.isnull(df['col_256']) or pd.isnull(df['col_255']):
                if pd.isnull(df['col_256']):
                    return 'Probable Reporting Error (10.2.1.b is blank)'
                elif pd.isnull(df['col_255']):
                    return 'Inconsistent (10.2.1.a is blank)'
            elif pd.isnull(df['col_256']) == pd.isnull(df['col_255']):
                return 'Consistent'
            else:
                return 'Consistent'
            return df

        # 3.1.1.a+3.1.1.b+3.1.3 >= 2.1.1.a+2.1.1.b+2.2
        def res28(df):
            if float(df['col_57']) + float(df['col_58']) + float(df['col_60']) < float(df['col_48']) + float(df['col_49']) + float(df['col_52']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_57']) and pd.isnull(df['col_58']) and pd.isnull(df['col_60']) and pd.isnull(df['col_48']) and pd.isnull(df['col_49']) and pd.isnull(df['col_52']):
                return 'Blank'
            elif pd.isnull(df['col_57']) or pd.isnull(df['col_58']) or pd.isnull(df['col_60']) or pd.isnull(df['col_48']) or pd.isnull(df['col_49']) or pd.isnull(df['col_52']):
                if pd.isnull(df['col_57']):
                    return 'Probable Reporting Error (3.1.1.a is blank)'
                elif pd.isnull(df['col_58']):
                    return 'Probable Reporting Error (3.1.1.b is blank)'
                elif pd.isnull(df['col_60']):
                    return 'Probable Reporting Error (3.1.3 is blank)'
                elif pd.isnull(df['col_48']):
                    return 'Inconsistent (2.1.1.a is blank)'
                elif pd.isnull(df['col_49']):
                    return 'Inconsistent (2.1.1.b is blank)'
                elif pd.isnull(df['col_52']):
                    return 'Inconsistent (2.2 is blank)'
            elif pd.isnull(df['col_57']) + pd.isnull(df['col_58']) + pd.isnull(df['col_60']) == pd.isnull(df['col_48']) + pd.isnull(df['col_49']) + pd.isnull(df['col_52']):
                return 'Consistent'
            else:
                return 'Consistent'
            return df

        # 8.1.1.c<=8.1.1.a
        def res29(df):
            if float(df['col_175']) > float(df['col_173']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_175']) and pd.isnull(df['col_173']):
                return 'Blank'
            elif pd.isnull(df['col_175']) or pd.isnull(df['col_173']):
                if pd.isnull(df['col_175']):
                    return 'Probable Reporting Error (8.1.1.c is blank)'
                elif pd.isnull(df['col_173']):
                    return 'Inconsistent (8.1.1.a is blank)'
            elif pd.isnull(df['col_175']) == pd.isnull(df['col_173']):
                return 'Consistent'
            else:
                return 'Consistent'
            return df

        # 9.2.1 + 9.2.2>= 9.1.1+ 9.1.2+ 9.1.3+ 9.1.4+ 9.1.5+ 9.1.6+ 9.1.7+ 9.1.8
        def res30(df):
            if float(df['col_200']) + float(df['col_201']) < float(df['col_191']) + float(df['col_192']) + float(df['col_193']) + float(df['col_194']) + float(df['col_195']) + float(df['col_196']) + float(df['col_197']) + float(df['col_198']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_200']) and pd.isnull(df['col_201']) and pd.isnull(df['col_191']) and pd.isnull(df['col_192']) and pd.isnull(df['col_193']) and pd.isnull(df['col_194']) and pd.isnull(df['col_195']) and pd.isnull(df['col_196']) and pd.isnull(df['col_197']) and pd.isnull(df['col_198']):
                return 'Blank'
            elif pd.isnull(df['col_200']) or pd.isnull(df['col_201']) or pd.isnull(df['col_191']) or pd.isnull(df['col_192']) or pd.isnull(df['col_193']) or pd.isnull(df['col_194']) or pd.isnull(df['col_195']) or pd.isnull(df['col_196']) or pd.isnull(df['col_197']) or pd.isnull(df['col_198']):
                if pd.isnull(df['col_200']):
                    return 'Probable Reporting Error (9.2.1 is blank)'
                elif pd.isnull(df['col_201']):
                    return 'Probable Reporting Error (9.2.2 is blank)'
                elif pd.isnull(df['col_191']):
                    return 'Inconsistent (9.1.1 is blank)'
                elif pd.isnull(df['col_192']):
                    return 'Inconsistent (9.1.2 is blank)'
                elif pd.isnull(df['col_193']):
                    return 'Inconsistent (9.1.3 is blank)'
                elif pd.isnull(df['col_194']):
                    return 'Inconsistent (9.1.4 is blank)'
                elif pd.isnull(df['col_195']):
                    return 'Inconsistent (9.1.5 is blank)'
                elif pd.isnull(df['col_196']):
                    return 'Inconsistent (9.1.6 is blank)'
                elif pd.isnull(df['col_197']):
                    return 'Inconsistent (9.1.7 is blank)'
                elif pd.isnull(df['col_198']):
                    return 'Inconsistent (9.1.8 is blank)'
            elif pd.isnull(df['col_200']) + pd.isnull(df['col_201']) == pd.isnull(df['col_191']) + pd.isnull(df['col_192']) + pd.isnull(df['col_193']) + pd.isnull(df['col_194']) + pd.isnull(df['col_195']) + pd.isnull(df['col_196']) + pd.isnull(df['col_197']) + pd.isnull(df['col_198']):
                return 'Consistent'
            else:
                return 'Consistent'
            return df

        # 8.1.1.b<=8.1.1.a
        def res31(df):
            if float(df['col_174']) > float(df['col_173']):
                return 'Inconsistent (check fails)'
            elif pd.isnull(df['col_174']) and pd.isnull(df['col_173']):
                return 'Blank'
            elif pd.isnull(df['col_174']) or pd.isnull(df['col_173']):
                if pd.isnull(df['col_174']):
                    return 'Probable Reporting Error (8.1.1.b is blank)'
                elif pd.isnull(df['col_173']):
                    return 'Inconsistent (8.1.1.a is blank)'
            elif pd.isnull(df['col_174']) == pd.isnull(df['col_173']):
                return 'Consistent'
            else:
                return 'Consistent'
            return df

        # df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res1, axis=1)
        # count_condition_1_consistent = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
        #     "consistent").sum()
        # count_condition_1_inconsistent = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
        #     "Inconsistent").sum()
        # count_condition_1_blank = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
        #     "Blank").sum()
        # count_condition_1_blank_error = df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
        #     "Blank Error").sum()

        df['1.1 <= 1.1.1'] = df.apply(res2, axis=1)
        count_condition_2_consistent = df['1.1 <= 1.1.1'].str.count(
            "consistent").sum()
        count_condition_2_inconsistent = df['1.1 <= 1.1.1'].str.count(
            "Inconsistent").sum()
        count_condition_2_blank = df['1.1 <= 1.1.1'].str.count("Blank").sum()
        count_condition_2_blank_error = df['1.1 <= 1.1.1'].str.count(
            "Blank Error").sum()

        df['1.3.1.a <= 1.3.1'] = df.apply(res3, axis=1)
        count_condition_3_consistent = df['1.3.1.a <= 1.3.1'].str.count(
            "consistent").sum()
        count_condition_3_inconsistent = df['1.3.1.a <= 1.3.1'].str.count(
            "Inconsistent").sum()
        count_condition_3_blank = df['1.3.1.a <= 1.3.1'].str.count(
            "Blank").sum()
        count_condition_3_blank_error = df['1.3.1.a <= 1.3.1'].str.count(
            "Blank Error").sum()

        # df['1.2.7 <= 1.1'] = df.apply(res4, axis=1)
        # count_condition_4_consistent = df['1.2.7 <= 1.1'].str.count(
        #     "consistent").sum()
        # count_condition_4_inconsistent = df['1.2.7 <= 1.1'].str.count(
        #     "Inconsistent").sum()
        # count_condition_4_blank = df['1.2.7 <= 1.1'].str.count("Blank").sum()
        # count_condition_4_blank_error = df['1.2.7 <= 1.1'].str.count(
        #     "Blank Error").sum()

        df['1.5.1.a <= 1.1'] = df.apply(res5, axis=1)
        count_condition_5_consistent = df['1.5.1.a <= 1.1'].str.count(
            "consistent").sum()
        count_condition_5_inconsistent = df['1.5.1.a <= 1.1'].str.count(
            "Inconsistent").sum()
        count_condition_5_blank = df['1.5.1.a <= 1.1'].str.count("Blank").sum()
        count_condition_5_blank_error = df['1.5.1.a <= 1.1'].str.count(
            "Blank Error").sum()

        df['1.5.1.b <= 1.5.1.a'] = df.apply(res6, axis=1)
        count_condition_6_consistent = df['1.5.1.b <= 1.5.1.a'].str.count(
            "consistent").sum()
        count_condition_6_inconsistent = df['1.5.1.b <= 1.5.1.a'].str.count(
            "Inconsistent").sum()
        count_condition_6_blank = df['1.5.1.b <= 1.5.1.a'].str.count(
            "Blank").sum()
        count_condition_6_blank_error = df['1.5.1.b <= 1.5.1.a'].str.count(
            "Blank Error").sum()

        df['2.1.2 <= 2.1.1.a + 2.1.1.b'] = df.apply(res7, axis=1)
        count_condition_7_consistent = df['2.1.2 <= 2.1.1.a + 2.1.1.b'].str.count(
            "consistent").sum()
        count_condition_7_inconsistent = df['2.1.2 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_7_blank = df['2.1.2 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Blank").sum()
        count_condition_7_blank_error = df['2.1.2 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Blank Error").sum()

        # df['2.1.3 <= 2.1.1.a + 2.1.1.b'] = df.apply(res8, axis=1)
        # count_condition_8_consistent = df['2.1.3 <= 2.1.1.a + 2.1.1.b'].str.count(
        #     "consistent").sum()
        # count_condition_8_inconsistent = df['2.1.3 <= 2.1.1.a + 2.1.1.b'].str.count(
        #     "Inconsistent").sum()
        # count_condition_8_blank = df['2.1.3 <= 2.1.1.a + 2.1.1.b'].str.count(
        #     "Blank").sum()
        # count_condition_8_blank_error = df['2.1.3 <= 2.1.1.a + 2.1.1.b'].str.count(
        #     "Blank Error").sum()

        # df['2.2.2 <= 2.2'] = df.apply(res9, axis=1)
        # count_condition_9_consistent = df['2.2.2 <= 2.2'].str.count(
        #     "consistent").sum()
        # count_condition_9_inconsistent = df['2.2.2 <= 2.2'].str.count(
        #     "Inconsistent").sum()
        # count_condition_9_blank = df['2.2.2 <= 2.2'].str.count(
        #     "Blank").sum()
        # count_condition_9_blank_error = df['2.2.2 <= 2.2'].str.count(
        #     "Blank Error").sum()
        
        # df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res10, axis=1)
        # count_condition_10_consistent = df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
        #     "consistent").sum()
        # count_condition_10_inconsistent = df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
        #     "Inconsistent").sum()
        # count_condition_10_blank = df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
        #     "Blank").sum()
        # count_condition_10_blank_error = df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
        #     "Blank Error").sum()

        df['6.1.1 <= 3.1.1.a + 3.1.1.b'] = df.apply(res11, axis=1)
        count_condition_11_consistent = df['6.1.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_11_inconsistent = df['6.1.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_11_blank = df['6.1.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_11_blank_error = df['6.1.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank Error").sum()

        df['6.1.9 <= 3.1.1.a + 3.1.1.b'] = df.apply(res12, axis=1)
        count_condition_12_consistent = df['6.1.9 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_12_inconsistent = df['6.1.9 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_12_blank = df['6.1.9 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_12_blank_error = df['6.1.9 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank Error").sum()

        df['6.1.13 <= 3.1.1.a + 3.1.1.b'] = df.apply(res13, axis=1)
        count_condition_13_consistent = df['6.1.13 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_13_inconsistent = df['6.1.13 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_13_blank = df['6.1.13 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_13_blank_error = df['6.1.13 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank Error").sum()

        df['2.2.1 <= 2.2'] = df.apply(res14, axis=1)
        count_condition_14_consistent = df['2.2.1 <= 2.2'].str.count(
            "consistent").sum()
        count_condition_14_inconsistent = df['2.2.1 <= 2.2'].str.count(
            "Inconsistent").sum()
        count_condition_14_blank = df['2.2.1 <= 2.2'].str.count(
            "Blank").sum()
        count_condition_14_blank_error = df['2.2.1 <= 2.2'].str.count(
            "Blank Error").sum()

        df['3.1.2 <= 3.1.1.a + 3.1.1.b'] = df.apply(res15, axis=1)
        count_condition_15_consistent = df['3.1.2 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_15_inconsistent = df['3.1.2 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_15_blank = df['3.1.2 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_15_blank_error = df['3.1.2 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank Error").sum()

        df['3.3.1 <= 3.1.1.a + 3.1.1.b'] = df.apply(res16, axis=1)
        count_condition_16_consistent = df['3.3.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_16_inconsistent = df['3.3.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_16_blank = df['3.3.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_16_blank_error = df['3.3.1 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank Error").sum()

        df['3.3.2 <= 3.3.1'] = df.apply(res17, axis=1)
        count_condition_17_consistent = df['3.3.2 <= 3.3.1'].str.count(
            "consistent").sum()
        count_condition_17_inconsistent = df['3.3.2 <= 3.3.1'].str.count(
            "Inconsistent").sum()
        count_condition_17_blank = df['3.3.2 <= 3.3.1'].str.count(
            "Blank").sum()
        count_condition_17_blank_error = df['3.3.2 <= 3.3.1'].str.count(
            "Blank Error").sum()

        df['3.3.3 <= 3.1.1.a + 3.1.1.b'] = df.apply(res18, axis=1)
        count_condition_18_consistent = df['3.3.3 <= 3.1.1.a + 3.1.1.b'].str.count(
            "consistent").sum()
        count_condition_18_inconsistent = df['3.3.3 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_18_blank = df['3.3.3 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank").sum()
        count_condition_18_blank_error = df['3.3.3 <= 3.1.1.a + 3.1.1.b'].str.count(
            "Blank Error").sum()

        df['4.1 <= 2.1.1.a + 2.1.1.b'] = df.apply(res19, axis=1)
        count_condition_19_consistent = df['4.1 <= 2.1.1.a + 2.1.1.b'].str.count(
            "consistent").sum()
        count_condition_19_inconsistent = df['4.1 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Inconsistent").sum()
        count_condition_19_blank = df['4.1 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Blank").sum()
        count_condition_19_blank_error = df['4.1 <= 2.1.1.a + 2.1.1.b'].str.count(
            "Blank Error").sum()

        df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'] = df.apply(res20, axis=1)
        count_condition_20_consistent = df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "consistent").sum()
        count_condition_20_inconsistent = df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Inconsistent").sum()
        count_condition_20_blank = df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Blank").sum()
        count_condition_20_blank_error = df['5.2 <= 2.1.1.a + 2.1.1.b + 2.2'].str.count(
            "Blank Error").sum()

        df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'] = df.apply(res21, axis=1)
        count_condition_21_consistent = df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'].str.count(
            "consistent").sum()
        count_condition_21_inconsistent = df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'].str.count(
            "Inconsistent").sum()
        count_condition_21_blank = df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'].str.count(
            "Blank").sum()
        count_condition_21_blank_error = df['6.2.4.a + 6.2.4.b <= 6.2.1 + 6.2.2'].str.count(
            "Blank Error").sum()

        df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'] = df.apply(res22, axis=1)
        count_condition_22_consistent = df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "consistent").sum()
        count_condition_22_inconsistent = df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Inconsistent").sum()
        count_condition_22_blank = df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Blank").sum()
        count_condition_22_blank_error = df['6.6.1<=6.1.1+6.1.2+6.1.3+6.1.4+6.1.5+6.1.6+6.1.7+6.1.8+6.1.13+6.1.14+6.1.15+6.1.16+6.1.17+6.1.18+6.1.19+6.1.20+6.1.21+6.2.1+6.2.2+6.2.3+6.3.1+6.3.2+6.3.3+6.4.1+6.4.2+6.4.3+6.4.5+6.4.6+6.5.1+6.5.2+6.5.3+6.5.4'].str.count(
            "Blank Error").sum()

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

        # df = pd.concat([df['4.3 <= 2.1.1.a + 2.1.1.b + 2.2'],
        df = pd.concat([df['1.1 <= 1.1.1'],
                        df['1.3.1.a <= 1.3.1'],
                        # df['1.2.7 <= 1.1'],
                        df['1.5.1.a <= 1.1'],
                        df['1.5.1.b <= 1.5.1.a'],
                        df['2.1.2 <= 2.1.1.a + 2.1.1.b'],
                        # df['2.1.3 <= 2.1.1.a + 2.1.1.b'],
                        # df['2.2.2 <= 2.2'],
                        # df['4.4 <= 2.1.1.a + 2.1.1.b + 2.2'],
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
        # frames = [df_OrgHeaders, df_]
        frames = [df_]
        df = pd.concat(frames, sort=False)
        df = df.dropna(axis=0, subset=['col_2']) 
        df.astype(str)
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
        # convert the list to set, this will fill select state with unique value
        
        list_set = df['col_2'].tolist()
        print(list_set)
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



############################################# Main Function ##############################################
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
