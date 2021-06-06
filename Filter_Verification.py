from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import numpy as np
from PyQt5.QtGui import QPalette, QFontMetrics, QStandardItem
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QPushButton, qApp
import sys, re

class CheckableComboBox(QtWidgets.QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QtWidgets.QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1347, 457)

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 60, 171, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.upload)

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 170, 171, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(50, 120, 171, 22))
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 100, 171, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 250, 171, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 320, 171, 16))
        self.label_3.setObjectName("label_3")

        # 2
        self.comboBox_2 = CheckableComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(40, 270, 181, 22))
        self.comboBox_2.setObjectName("comboBox_2")

        # 3
        self.comboBox_3 = CheckableComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(40, 340, 181, 22))
        self.comboBox_3.setObjectName("comboBox_3")

        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 390, 181, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(320, 60, 981, 361))
        self.tableView.setObjectName("tableView")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "UPLOAD CSV"))
        self.pushButton_2.setText(_translate("Dialog", "VALIDATE BUTTON"))
        self.label.setText(_translate("Dialog", "Select FTYPE from dropdown"))
        self.label_2.setText(_translate("Dialog", "Filter Date"))
        self.label_3.setText(_translate("Dialog", "Filter Month"))
        self.pushButton_3.setText(_translate("Dialog", "Export CSV"))

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

                # df = self.loadFile(df_)
                
                # Signaling HSC_Validate function i.e function where validation checks are present
                self.pushButton_2.clicked.connect(self.HSC_Validate)

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
        global df, flag
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


        '''
        WE HAVE MERGING PROBLEM HERE
        '''
        df['1.1 >= 1.1.1'] = df.apply(res2, axis=1)

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

        self.tableView.setModel(PandasModel(df))
        lst_1 = set(df.col_3.to_list())
        self.comboBox_2.addItems(lst_1)
        self.comboBox_2.activated[str].connect(self.filter_State)

        lst_2 = set(df.col_5.to_list())
        self.comboBox_3.addItems(lst_2)
        self.comboBox_3.activated[str].connect(self.filter_District)
        self.df = df
        
        return self.df

    
    def filter_State(self):
        selected_States = self.comboBox_2.currentData()
        self.df = self.df[self.df['col_3'].isin(selected_States)] 
        print(self.df['col_3'].value_counts)
        print(self.df)
        return self.df    
    
    def filter_District(self):
        selected_Districts = self.comboBox_3.currentData()
        self.df = self.df[self.df['col_5'].isin(selected_Districts)]
        print(self.df['col_5'].value_counts)
        print(self.df)
        return self.df


    





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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
